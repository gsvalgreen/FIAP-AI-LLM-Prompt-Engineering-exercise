#!/usr/bin/env python3
"""
Script: calculadora_imc.py
Descrição: Calcula o IMC (Índice de Massa Corporal) para pacientes a partir de um arquivo CSV
             e gera um novo arquivo com o IMC e a classificação segundo a OMS.

Uso esperado:
- Entrada:  'dados_pacientes.csv' no mesmo diretório, com as colunas: paciente, peso, altura
- Saída:    'resultados_imc.csv' contendo as colunas originais + imc + classificacao
- Exibição: Imprime uma mensagem de sucesso e as 5 primeiras linhas do arquivo de saída

Requisitos: pandas

Notas:
- Tratamento simples para o caso do arquivo de entrada não existir.
- Valores serão arredondados para uma casa decimal para facilitar conferência com a user story.
"""
from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd

# Constantes de nomes de arquivos
INPUT_FILE = Path(__file__).with_name("dados_pacientes.csv")
OUTPUT_FILE = Path(__file__).with_name("resultados_imc.csv")


def calcular_imc(peso: float, altura: float) -> float:
    """Calcula o IMC = peso / (altura ** 2).

    Arredonda para 1 casa decimal para alinhar com os critérios de aceite.
    """
    if altura == 0:
        return float("nan")
    imc = peso / (altura ** 2)
    return round(imc, 1)


def classificar_imc(imc: float) -> str:
    """Classifica o IMC de acordo com as faixas da OMS.

    Faixas:
    - Abaixo do peso: IMC <= 18,5
    - Peso normal: 18,5 <= IMC <= 25
    - Sobrepeso: 25 <= IMC <= 30
    - Obesidade Grau I: 30 <= IMC <= 35
    - Obesidade Grau II: 35 <= IMC <= 40
    - Obesidade Grau III: IMC >= 40
    """
    if pd.isna(imc):
        return "Indefinido"

    if imc <= 18.5:
        return "Abaixo do peso"
    if 18.5 <= imc <= 25:
        return "Peso normal"
    if 25 <= imc <= 30:
        return "Sobrepeso"
    if 30 <= imc <= 35:
        return "Obesidade Grau I"
    if 35 <= imc <= 40:
        return "Obesidade Grau II"
    return "Obesidade Grau III"


def main() -> int:
    # 1) Ler arquivo de entrada com tratamento simples para arquivo não encontrado
    if not INPUT_FILE.exists():
        print(
            f"Erro: arquivo de entrada '{INPUT_FILE.name}' não encontrado.\n"
            "Certifique-se de que o arquivo existe neste diretório ou gere o arquivo de exemplo."
        )
        return 1

    # 2) Carregar dados com pandas
    df = pd.read_csv(INPUT_FILE)

    # 3) Garantir que as colunas esperadas existem
    colunas_esperadas = {"paciente", "peso", "altura"}
    ausentes = colunas_esperadas - set(df.columns)
    if ausentes:
        print(f"Erro: colunas ausentes no CSV de entrada: {sorted(ausentes)}")
        return 2

    # 4) Calcular IMC e classificação
    df["imc"] = df.apply(lambda r: calcular_imc(r["peso"], r["altura"]), axis=1)
    df["classificacao"] = df["imc"].apply(classificar_imc)

    # 5) Salvar o resultado em CSV
    df.to_csv(OUTPUT_FILE, index=False)

    # 6) Exibir mensagem de sucesso e as 5 primeiras linhas
    print("Processamento concluído com sucesso. Saída salva em 'resultados_imc.csv'.\n")
    print("Prévia das 5 primeiras linhas:")
    print(pd.read_csv(OUTPUT_FILE).head())

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
