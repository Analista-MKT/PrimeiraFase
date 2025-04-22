import pandas as pd


df = r'C:\Users\pereirat\OneDrive - De Sangosse Agroquímica Ltda\Documentos\1.0 - INDICADORES\1.6 - Banco de Dados\1.6.7 - DADOS QLIK SENSE\1.6.7.1 - VENDAS\Vendas 2024 até 25-11.xlsx'

Vendas = pd.read_excel(df, sheet_name='DADOS')

print(Vendas.head())
print(Vendas.info())

#Test