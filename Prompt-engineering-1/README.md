# IMC via CSV

Script Python para calcular IMC a partir de um arquivo CSV, adicionando as colunas `imc` e `categoria_imc`.

## Uso rápido

```
python imc_csv.py exemplo_entrada.csv -o saida.csv
```

- Detecta delimitador (`,` ou `;`) e separador decimal automaticamente.
- Tenta descobrir colunas de peso/altura por nomes comuns (ex.: `peso`, `altura`).
- Aceita `--peso-col` e `--altura-col` para definir explicitamente.

## Opções principais

- `--delimiter` `,` `;` `\t`
- `--decimal` `,` `.` (entrada)
- `--saida-decimal` `,` `.` (saída; padrão `.`)
- `--encoding` (padrão `utf-8-sig`)

## Observações

- Se a altura parecer estar em cm (valor > 3), o script converte para metros automaticamente.
- Linhas inválidas são mantidas; o IMC fica vazio e o total de erros é exibido ao final.
