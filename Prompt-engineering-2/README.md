# Calculadora de IMC (CSV)

Script em Python que lê um CSV com pacientes (paciente, peso, altura), calcula o IMC e a classificação segundo a OMS, e salva em `resultados_imc.csv`.

## Requisitos
- Python 3.9+
- pandas (veja `requirements.txt`)

## Arquivos
- `dados_pacientes.csv` — exemplo com casos dos critérios de aceite.
- `calculadora_imc.py` — script principal.
- `resultados_imc.csv` — será gerado após a execução.

## Como executar
1) (Opcional) criar ambiente virtual:
```
python3 -m venv .venv
source .venv/bin/activate
```
2) Instalar dependências:
```
pip install -r requirements.txt
```
3) Executar o script:
```
python calculadora_imc.py
```
Ao final, o script imprime uma mensagem de sucesso e mostra as 5 primeiras linhas do arquivo de saída.

## Observações
- O IMC é arredondado para 1 casa decimal (facilita conferência com a user story).
- Tratamento simples para arquivo de entrada ausente e para colunas obrigatórias.
