## **User Story: Calculadora de IMC para Nutricionista**

### **Contexto**

Como nutricionista, preciso de uma ferramenta para calcular o IMC de meus pacientes a partir de uma planilha de dados, para que eu possa analisar rapidamente o perfil de peso de um grupo de pacientes e identificar a classificação de cada um. Isso me permitirá ter uma visão geral e mais estratégica de seus casos.

### **ESCOPO:**

**O que é parte dessa história:**

* Desenvolvimento de um script ou programa que leia um arquivo CSV contendo os dados de pacientes (altura e peso).  
* Cálculo do Índice de Massa Corporal (IMC) para cada paciente.  
* Classificação do IMC de cada paciente de acordo com as faixas da Organização Mundial da Saúde (OMS).  
* Geração de um novo arquivo CSV com as informações originais dos pacientes, o valor do IMC calculado e a sua respectiva classificação.

**O que não é parte dessa história:**

* Criação de uma interface gráfica (GUI) para a ferramenta. O processo será via linha de comando ou script.  
* Tratamento de erros para dados ausentes ou inválidos (ex: peso ou altura igual a zero, valores negativos ou texto).  
* Geração de gráficos ou relatórios visuais.  
* Análise estatística ou cruzamento de dados que vá além da simples classificação.

### **OBSERVAÇÕES / DICAS / PERGUNTAS**

* O arquivo de entrada CSV terá as colunas "paciente", "peso" (em kg) e "altura" (em metros).  
* O arquivo de saída CSV deve incluir as colunas originais mais "IMC" e "Classificação".  
* O cálculo do IMC é:   
  IMC = peso / alturaˆ2  
* As classificações a serem utilizadas são as da OMS:  
  * Abaixo do peso: IMC <= 18,5  
  * Peso normal: 18,5 <= IMC <= 25  
  * Sobrepeso: 25 <= IMC <= 30  
  * Obesidade Grau I: 30 <= IMC <= 35  
  * Obesidade Grau II: 35 <= IMC <= 40  
  * Obesidade Grau III (Obesidade Mórbida): IMC >= 40

---

### **CRITÉRIOS DE ACEITE**

#### Cenário 1: Classificação "Abaixo do peso"

DADO um arquivo CSV com um paciente cujo peso seja 60 kg e a altura 1,81 m.

QUANDO o script de cálculo de IMC for executado.

ENTÃO a linha do paciente no arquivo de saída CSV deve ter o IMC de 18,3 e a classificação "Abaixo do peso".

#### Cenário 2: Classificação "Peso normal"

DADO um arquivo CSV com um paciente cujo peso seja 75 kg e a altura 1,75 m.

QUANDO o script de cálculo de IMC for executado.

ENTÃO a linha do paciente no arquivo de saída CSV deve ter o IMC de 24,5 e a classificação "Peso normal".

#### Cenário 3: Classificação "Sobrepeso"

DADO um arquivo CSV com um paciente cujo peso seja 85 kg e a altura 1,78 m.

QUANDO o script de cálculo de IMC for executado.

ENTÃO a linha do paciente no arquivo de saída CSV deve ter o IMC de 26,8 e a classificação "Sobrepeso".

#### Cenário 4: Classificação "Obesidade Grau I"

DADO um arquivo CSV com um paciente cujo peso seja 105 kg e a altura 1,80 m.

QUANDO o script de cálculo de IMC for executado.

ENTÃO a linha do paciente no arquivo de saída CSV deve ter o IMC de 32,4 e a classificação "Obesidade Grau I".

#### Cenário 5: Classificação "Obesidade Grau II"

DADO um arquivo CSV com um paciente cujo peso seja 115 kg e a altura 1,70 m.

QUANDO o script de cálculo de IMC for executado.

ENTÃO a linha do paciente no arquivo de saída CSV deve ter o IMC de 39,8 e a classificação "Obesidade Grau II".

#### Cenário 6: Classificação "Obesidade Grau III"

DADO um arquivo CSV com um paciente cujo peso seja 120 kg e a altura 1,65 m.

QUANDO o script de cálculo de IMC for executado.

ENTÃO a linha do paciente no arquivo de saída CSV deve ter o IMC de 44,1 e a classificação "Obesidade Grau III".

