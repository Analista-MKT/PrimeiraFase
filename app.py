import pandas as pd
from functions import import_file

repositorio = 'C:\Users\pereirat\OneDrive - De Sangosse Agroquímica Ltda\Documentos\4.0 - PROGRAMAÇÃO E BANCO DE DADOS'
arquivo = 'faturamento.xlsx'
planilha = 'DADOS'

df_vendas = import_file(repositorio, arquivo, planilha)

print(df_vendas.head())

faturamento_total = df_vendas['Valor Real'].sum()
Volume_total = df_vendas['Quantidade'].sum()


print(format(faturamento_total, '.2f'))



#print(Vendas.head())
#print(Vendas.info())