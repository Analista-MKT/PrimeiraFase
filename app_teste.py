import pandas as pd
import numpy as np

repositorio_faturamento = r'C:\Users\pereirat\OneDrive - De Sangosse Agroquímica Ltda\Documentos\4.0 - PROGRAMAÇÃO E BANCO DE DADOS\faturamento.xlsx'

repositorio_clientes = r'C:\Users\pereirat\OneDrive - De Sangosse Agroquímica Ltda\Documentos\1.0 - INDICADORES\1.6 - Banco de Dados\1.6.10 - CLIENTES\BASE CLIENTES.xlsx'

repositorio_coordenadas = r'C:\Users\pereirat\OneDrive - De Sangosse Agroquímica Ltda\Documentos\4.0 - PROGRAMAÇÃO E BANCO DE DADOS\Projeto_01\Base planilhas\1.6.3 - LOCALIZAÇÃO E ESTRUTURA MUNICIPIOS\coordenadas.xlsx'

repositorio_municipios = r'C:\Users\pereirat\OneDrive - De Sangosse Agroquímica Ltda\Documentos\4.0 - PROGRAMAÇÃO E BANCO DE DADOS\Projeto_01\Base planilhas\1.6.3 - LOCALIZAÇÃO E ESTRUTURA MUNICIPIOS\estrutura_municipios.xlsx'


df_faturamento = pd.read_excel(repositorio_faturamento, sheet_name='DADOS')
df_clientes = pd.read_excel(repositorio_clientes, sheet_name='Planilha1')
df_coordenadas = pd.read_excel(repositorio_coordenadas, sheet_name='dados')
df_municipios = pd.read_excel(repositorio_municipios, sheet_name='dados')


# Adicionando duas colunas de coordenadas para relacionar aos nomes dos municipios
Localizacao = pd.merge(df_municipios,df_coordenadas, left_on='codigo_municipio_completo', right_on='GEOCODIGO_MUNICIPIO',how='left')
# Retirando coluna com informação repetida
Localizacao = Localizacao.drop(columns=['codigo_municipio_completo'])
# Salvando em excel
Localizacao.to_excel(r'C:\Users\pereirat\OneDrive - De Sangosse Agroquímica Ltda\Documentos\4.0 - PROGRAMAÇÃO E BANCO DE DADOS\Projeto_01\Planilhas_teste\localizacao_teste.xlsx', index=False)



# Aqui estamos dividindo os valores da coluna por 2
df_faturamento['Valor Real/2'] = df_faturamento['Valor Real']/2
# Aqui estamos dividindo uma coluna de texte em duas partes utilizando '-' como separador
df_faturamento[['tag', 'Responsável']] = df_faturamento['Responsável'].str.split('-', expand=True)

df_produto = df_faturamento[['SKU', 'Quantidade', 'Valor Real']]

df_agrupado = df_produto.groupby('SKU').sum().reset_index()



#df_agrupado = df.groupby('categoria').sum().reset_index()

#df[['nome', 'sobrenome']] = df['coluna_texto'].str.split(' ', expand=True)


#print(df.info())
#print(df[['Quantidade', 'Valor Real','Valor Real/2', 'tag', 'Responsável']].head())
#print(df_agrupado)
#print(df_clientes.info())
print(Localizacao.head())


#df.to_excel(r'C:\Users\pereirat\OneDrive - De Sangosse Agroquímica Ltda\Documentos\4.0 - PROGRAMAÇÃO E BANCO DE DADOS\faturamento_MOD.xlsx', index=False)
#df_agrupado.to_excel(r'C:\Users\pereirat\OneDrive - De Sangosse Agroquímica Ltda\Documentos\4.0 - PROGRAMAÇÃO E BANCO DE DADOS\faturamento_Agrupado.xlsx', index=False)




#for i in df['SKU']:
 #   i+8
