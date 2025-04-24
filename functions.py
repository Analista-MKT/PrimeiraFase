import pandas as pd

def import_file(repositorio,arquivo,planilha):
    df = pd.read_excel(r'repositorio\arquivo.xlsx', sheet_name= "planilha")
    return df