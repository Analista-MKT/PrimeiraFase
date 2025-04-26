import duckdb as duckdb

# Conectar ao banco de dados DuckDB (pode ser um arquivo ou em memória)
con = duckdb.connect('faturamento.duckdb')

# Ler o arquivo Excel usando DuckDB
repositorio = r'C:\Users\pereirat\OneDrive - De Sangosse Agroquímica Ltda\Documentos\4.0 - PROGRAMAÇÃO E BANCO DE DADOS\faturamento.xlsx'
con.execute(f"INSTALL 'excel'; LOAD 'excel';")
con.execute(f"CREATE TABLE dados AS SELECT * FROM read_excel('{repositorio}', 'DADOS');")

# Dividir a coluna 'Valor Real' por 2
con.execute("UPDATE dados SET 'Valor Real' = 'Valor Real' / 2;")

# Imprimir informações sobre a tabela
print(con.execute("DESCRIBE dados").fetchall())

# Imprimir os primeiros registros da tabela
print(con.execute("SELECT * FROM dados LIMIT 5").fetchall())

# Salvar a tabela modificada em um novo arquivo Excel
#con.execute(f"EXPORT DATABASE '{repositorio}_MOD.xlsx' (FORMAT 'excel');")
