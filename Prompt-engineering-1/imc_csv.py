#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script: imc_csv.py

Calcula o IMC (Índice de Massa Corporal) a partir de um arquivo CSV e salva um novo CSV
com as colunas adicionais "imc" e "categoria_imc".

- Detecta automaticamente o delimitador ("," ou ";") quando possível.
- Tenta detectar automaticamente o separador decimal ("," ou ".") dos campos numéricos.
- Identifica colunas de peso e altura mesmo com variações comuns de nomes (ex.: "Peso (kg)", "Altura em m").
- Lida com números com separador de milhar.

Uso básico:
    python imc_csv.py entrada.csv -o saida.csv

Opções:
    --peso-col       Nome da coluna de peso (kg). Se omitido, tenta detectar.
    --altura-col     Nome da coluna de altura (m). Se omitido, tenta detectar.
    --delimiter      Delimitador do CSV ("," ou ";"). Se omitido, tenta detectar.
    --decimal        Separador decimal de entrada ("," ou "."). Se omitido, tenta detectar.
    --saida-decimal  Separador decimal para o valor de IMC na saída ("." padrão ou ",").
    --encoding       Encoding do arquivo (padrão: utf-8-sig).

Notas:
- Se a altura parecer estar em centímetros (valor > 3), será convertida para metros automaticamente.
- Linhas com dados inválidos são mantidas com IMC vazio e um aviso é exibido ao final.
"""
from __future__ import annotations

import argparse
import csv
import math
import re
import sys
import unicodedata
from pathlib import Path
from typing import Dict, Iterable, List, Optional, Tuple


def normalize_name(s: str) -> str:
    """Normaliza nomes de colunas: minúsculas, sem acentos e apenas letras/números/_.
    Ex.: "Peso (kg)" -> "peso_kg"
    """
    s = s.strip().lower()
    s = unicodedata.normalize("NFKD", s)
    s = "".join(ch for ch in s if not unicodedata.combining(ch))
    s = re.sub(r"[^a-z0-9]+", "_", s)
    s = re.sub(r"_+", "_", s).strip("_")
    return s


def detect_delimiter(sample: str) -> str:
    """Tenta detectar delimitador com csv.Sniffer; fallback para ";" se muitas ocorrências."""
    try:
        dialect = csv.Sniffer().sniff(sample, delimiters=[",", ";", "\t"])  # pragma: no cover
        return dialect.delimiter
    except Exception:
        # Heurística simples
        commas = sample.count(",")
        semis = sample.count(";")
        if semis > commas:
            return ";"
        return ","


def detect_decimal_from_values(values: Iterable[str]) -> str:
    """Detecta separador decimal observando padrões 123,45 vs 123.45 nos valores."""
    comma_hits = 0
    dot_hits = 0
    pattern_comma = re.compile(r"\d+,\d+")
    pattern_dot = re.compile(r"\d+\.\d+")
    for v in values:
        if not isinstance(v, str):
            continue
        if pattern_comma.search(v):
            comma_hits += 1
        if pattern_dot.search(v):
            dot_hits += 1
    return "," if comma_hits > dot_hits else "."


def parse_number(text: str, decimal: str) -> Optional[float]:
    """Converte string numérica para float respeitando separador decimal.
    Trata separadores de milhar ("." ou ","). Retorna None se vazio/ inválido.
    """
    if text is None:
        return None
    if isinstance(text, (int, float)):
        return float(text)
    s = str(text).strip()
    if s == "":
        return None
    # Remove espaços e símbolos não numéricos exceto dígitos, separador decimal e sinal
    s = s.replace("\u00A0", " ").strip()

    # Normaliza separadores: remove milhares e converte decimal para ponto
    if decimal == ",":
        # Formatos possíveis: 1.234,56 (pt-BR) ou 1234,56
        s = s.replace(".", "")
        s = s.replace(",", ".")
    else:
        # decimal == ".": formatos 1,234.56 (en) ou 1234.56
        s = s.replace(",", "")
    try:
        return float(s)
    except ValueError:
        return None


def categorize_bmi(bmi: float) -> str:
    if math.isnan(bmi) or math.isinf(bmi):
        return ""
    if bmi < 18.5:
        return "Abaixo do peso"
    if bmi < 25:
        return "Peso normal"
    if bmi < 30:
        return "Sobrepeso"
    if bmi < 35:
        return "Obesidade grau I"
    if bmi < 40:
        return "Obesidade grau II"
    return "Obesidade grau III"


def find_weight_height_columns(fieldnames: List[str]) -> Tuple[Optional[str], Optional[str]]:
    weight_keys = {
        "peso",
        "peso_kg",
        "massa",
        "massa_kg",
        "weight",
        "weight_kg",
        "mass",
        "mass_kg",
    }
    height_keys = {
        "altura",
        "altura_m",
        "estatura",
        "height",
        "height_m",
        "tamanho",
    }
    norm_to_orig: Dict[str, str] = {normalize_name(h): h for h in fieldnames}
    weight_col = next((norm_to_orig[n] for n in norm_to_orig if n in weight_keys), None)
    height_col = next((norm_to_orig[n] for n in norm_to_orig if n in height_keys), None)
    return weight_col, height_col


def compute_bmi_for_rows(
    rows: List[Dict[str, str]],
    weight_col: str,
    height_col: str,
    decimal_in: str,
) -> Tuple[List[Dict[str, str]], int]:
    """Enriquece as linhas com IMC e categoria. Retorna (linhas, erros)."""
    errors = 0
    enriched: List[Dict[str, str]] = []
    for row in rows:
        weight_raw = row.get(weight_col)
        height_raw = row.get(height_col)
        w = parse_number(weight_raw, decimal_in)
        h = parse_number(height_raw, decimal_in)
        bmi_value: Optional[float] = None
        category = ""
        if w is None or h is None or h == 0:
            errors += 1
        else:
            # Se altura parecer estar em cm, converte para m
            if h > 3:  # heurística simples
                h = h / 100.0
            try:
                bmi_value = w / (h * h)
            except Exception:
                errors += 1
        if bmi_value is not None and bmi_value > 0 and math.isfinite(bmi_value):
            category = categorize_bmi(bmi_value)
            row["imc"] = f"{bmi_value:.2f}"
        else:
            row["imc"] = ""
        row["categoria_imc"] = category
        enriched.append(row)
    return enriched, errors


def decide_decimal(rows: List[Dict[str, str]], candidates: List[str]) -> str:
    # Coleta uma amostra de valores das colunas relevantes para detecção
    values: List[str] = []
    for row in rows[:200]:
        for c in candidates:
            v = row.get(c)
            if v:
                values.append(str(v))
    if not values:
        return "."
    return detect_decimal_from_values(values)


def main(argv: Optional[List[str]] = None) -> int:
    parser = argparse.ArgumentParser(description="Calcula IMC a partir de um CSV.")
    parser.add_argument("input", help="Caminho do CSV de entrada")
    parser.add_argument("-o", "--output", help="Caminho do CSV de saída (padrão: <input>_com_imc.csv)")
    parser.add_argument("--peso-col", help="Nome exato da coluna de peso (kg)")
    parser.add_argument("--altura-col", help="Nome exato da coluna de altura (m)")
    parser.add_argument("--delimiter", choices=[",", ";", "\t"], help="Delimitador do CSV")
    parser.add_argument("--decimal", choices=[",", "."], help="Separador decimal de entrada")
    parser.add_argument("--saida-decimal", choices=[",", "."], default=".", help="Separador decimal para IMC na saída")
    parser.add_argument("--encoding", default="utf-8-sig", help="Encoding do arquivo (padrão: utf-8-sig)")

    args = parser.parse_args(argv)

    in_path = Path(args.input)
    if not in_path.exists():
        print(f"Arquivo de entrada não encontrado: {in_path}", file=sys.stderr)
        return 2

    out_path = Path(args.output) if args.output else in_path.with_name(in_path.stem + "_com_imc.csv")

    # Lê cabeçalho e amostra para detecção
    sample_text = in_path.read_text(encoding=args.encoding, errors="ignore")[:5000]

    delimiter = args.delimiter or detect_delimiter(sample_text)

    # Lê todas as linhas em memória para facilitar detecções e processamento
    with in_path.open("r", encoding=args.encoding, newline="") as f:
        # restkey evita chaves None quando há colunas extras em alguma linha
        reader = csv.DictReader(f, delimiter=delimiter, restkey="_rest")
        rows = list(reader)
        fieldnames = reader.fieldnames or []

    if not fieldnames:
        print("Não foi possível ler o cabeçalho do CSV.", file=sys.stderr)
        return 2

    # Determina colunas de peso/altura
    weight_col = args.peso_col
    height_col = args.altura_col
    if not weight_col or not height_col:
        auto_w, auto_h = find_weight_height_columns(fieldnames)
        weight_col = weight_col or auto_w
        height_col = height_col or auto_h

    if not weight_col or not height_col:
        print(
            "Não foi possível identificar as colunas de peso e altura. "
            "Informe-as com --peso-col e --altura-col.",
            file=sys.stderr,
        )
        print(f"Colunas disponíveis: {fieldnames}")
        return 2

    # Detecta separador decimal se não fornecido
    decimal_in = args.decimal or decide_decimal(rows, [weight_col, height_col])

    # Calcula IMC
    enriched_rows, error_count = compute_bmi_for_rows(rows, weight_col, height_col, decimal_in)

    # Prepara cabeçalho de saída: mantém ordem original + novas colunas (se não existirem)
    out_fields = list(fieldnames)
    for extra in ("imc", "categoria_imc"):
        if extra not in out_fields:
            out_fields.append(extra)

    # Escreve saída
    with out_path.open("w", encoding=args.encoding, newline="") as f:
        # extrasaction='ignore' garante que chaves desconhecidas (ex.: '_rest') não causem erro
        writer = csv.DictWriter(
            f, fieldnames=out_fields, delimiter=delimiter, extrasaction="ignore"
        )
        writer.writeheader()
        for row in enriched_rows:
            # Ajusta decimal de saída, se necessário
            if args.saida_decimal == "," and row.get("imc"):
                row = dict(row)
                row["imc"] = row["imc"].replace(".", ",")
            writer.writerow(row)

    total = len(enriched_rows)
    ok = total - error_count
    print(
        f"Processadas {total} linhas. Sucesso: {ok}. Com dados inválidos: {error_count}.\n"
        f"Arquivo gerado: {out_path} (delimitador='{delimiter}', decimal_in='{decimal_in}', decimal_out='{args.saida_decimal}')."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
