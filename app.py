import pandas as pd
import streamlit as st
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
import locale

# Configurar o locale para formatação de valores em Real brasileiro
try:
    locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')
except:
    try:
        locale.setlocale(locale.LC_ALL, 'Portuguese_Brazil.1252')
    except:
        st.warning("Não foi possível configurar o locale para português do Brasil. A formatação de moeda pode não aparecer corretamente.")

# Título da aplicação
st.title('Dashboard de Análise de Vendas')

# Upload de arquivo
st.sidebar.header('Upload de Dados')
uploaded_file = st.sidebar.file_uploader("Faça upload do arquivo CSV de vendas", type=['csv'])

# Função para carregar e processar os dados
def load_data(file):
    df = pd.read_csv(file)
    
    # Renomeando colunas para garantir consistência
    df.columns = ['Data', 'Cliente', 'Valor'] if len(df.columns) >= 3 else df.columns
    
    # Convertendo a coluna de data para o formato datetime
    df['Data'] = pd.to_datetime(df['Data'])
    
    # Criando colunas úteis para análises
    df['Mês'] = df['Data'].dt.month_name()
    df['Ano'] = df['Data'].dt.year
    df['Dia da Semana'] = df['Data'].dt.day_name()
    
    return df

# Se o arquivo foi carregado
if uploaded_file is not None:
    # Carregar dados
    df = load_data(uploaded_file)
    
    # Exibir dados brutos em uma aba expandível
    with st.expander("Ver dados brutos"):
        st.dataframe(df)
    
    # Informações gerais
    st.header('Resumo de Vendas')
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total de Vendas", f"R$ {df['Valor'].sum():,.2f}".replace(",", "X").replace(".", ",").replace("X", "."))
    with col2:
        st.metric("Média por Venda", f"R$ {df['Valor'].mean():,.2f}".replace(",", "X").replace(".", ",").replace("X", "."))
    with col3:
        st.metric("Total de Clientes", df['Cliente'].nunique())
    
    # Análises temporais
    st.header('Análise Temporal')
    
    # Vendas ao longo do tempo
    st.subheader('Vendas ao Longo do Tempo')
    vendas_por_data = df.groupby('Data')['Valor'].sum().reset_index()
    fig_timeline = px.line(vendas_por_data, x='Data', y='Valor',
                         title='Vendas Diárias')
    st.plotly_chart(fig_timeline)
    
    # Análise por mês
    st.subheader('Vendas por Mês')
    vendas_por_mes = df.groupby(['Ano', 'Mês'])['Valor'].sum().reset_index()
    fig_month = px.bar(vendas_por_mes, x='Mês', y='Valor', color='Ano',
                     title='Vendas Mensais')
    st.plotly_chart(fig_month)
    
    # Análise por dia da semana
    st.subheader('Vendas por Dia da Semana')
    order_days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    vendas_por_dia_semana = df.groupby('Dia da Semana')['Valor'].sum().reset_index()
    
    # Criar um mapeamento para os dias da semana em português
    dias_semana_pt = {
        'Monday': 'Segunda-feira',
        'Tuesday': 'Terça-feira',
        'Wednesday': 'Quarta-feira',
        'Thursday': 'Quinta-feira',
        'Friday': 'Sexta-feira',
        'Saturday': 'Sábado',
        'Sunday': 'Domingo'
    }
    
    # Tentar traduzir os dias da semana se estiverem em inglês
    if vendas_por_dia_semana['Dia da Semana'].iloc[0] in dias_semana_pt:
        vendas_por_dia_semana['Dia da Semana'] = vendas_por_dia_semana['Dia da Semana'].map(dias_semana_pt)
        order_days = [dias_semana_pt[day] for day in order_days]
    
    fig_weekday = px.bar(vendas_por_dia_semana, x='Dia da Semana', y='Valor',
                        title='Vendas por Dia da Semana',
                        category_orders={"Dia da Semana": order_days})
    st.plotly_chart(fig_weekday)
    
    # Análise por cliente
    st.header('Análise por Cliente')
    
    # Top 10 clientes
    st.subheader('Top 10 Clientes por Valor de Venda')
    top_clientes = df.groupby('Cliente')['Valor'].sum().sort_values(ascending=False).head(10).reset_index()
    fig_top_clients = px.bar(top_clientes, x='Cliente', y='Valor',
                           title='Top 10 Clientes')
    st.plotly_chart(fig_top_clients)
    
    # Frequência de compra por cliente
    st.subheader('Frequência de Compra por Cliente')
    freq_clientes = df['Cliente'].value_counts().head(10).reset_index()
    freq_clientes.columns = ['Cliente', 'Frequência']
    fig_freq = px.bar(freq_clientes, x='Cliente', y='Frequência',
                    title='Frequência de Compra por Cliente')
    st.plotly_chart(fig_freq)
    
    # Valor médio de compra por cliente
    st.subheader('Valor Médio de Compra por Cliente')
    avg_cliente = df.groupby('Cliente')['Valor'].mean().sort_values(ascending=False).head(10).reset_index()
    fig_avg = px.bar(avg_cliente, x='Cliente', y='Valor',
                   title='Valor Médio de Compra por Cliente')
    st.plotly_chart(fig_avg)
    
    # Análises adicionais
    st.header('Análises Adicionais')
    
    # Distribuição de valores de venda
    st.subheader('Distribuição de Valores de Venda')
    fig_dist = px.histogram(df, x='Valor', nbins=20,
                          title='Distribuição de Valores de Venda')
    st.plotly_chart(fig_dist)
    
    # Filtros para análises personalizadas
    st.header('Análises Personalizadas')
    
    # Filtro de período
    st.subheader('Filtrar por Período')
    col1, col2 = st.columns(2)
    with col1:
        start_date = st.date_input('Data Inicial', df['Data'].min())
    with col2:
        end_date = st.date_input('Data Final', df['Data'].max())
    
    # Filtro de cliente
    selected_clients = st.multiselect('Selecionar Clientes', options=df['Cliente'].unique())
    
    # Aplicar filtros
    filtered_df = df.copy()
    filtered_df = filtered_df[(filtered_df['Data'].dt.date >= start_date) & 
                              (filtered_df['Data'].dt.date <= end_date)]
    
    if selected_clients:
        filtered_df = filtered_df[filtered_df['Cliente'].isin(selected_clients)]
    
    # Exibir dados filtrados
    st.subheader('Dados Filtrados')
    st.dataframe(filtered_df)
    
    # Gráfico de barras para clientes filtrados
    if not filtered_df.empty:
        st.subheader('Vendas por Cliente (Dados Filtrados)')
        vendas_filtradas = filtered_df.groupby('Cliente')['Valor'].sum().reset_index()
        fig_filtered = px.bar(vendas_filtradas, x='Cliente', y='Valor',
                            title='Vendas por Cliente no Período Selecionado')
        st.plotly_chart(fig_filtered)
        
        # Resumo estatístico dos dados filtrados
        st.subheader('Resumo Estatístico (Dados Filtrados)')
        st.write(f"Total de Vendas: R$ {filtered_df['Valor'].sum():,.2f}".replace(",", "X").replace(".", ",").replace("X", "."))
        st.write(f"Média por Venda: R$ {filtered_df['Valor'].mean():,.2f}".replace(",", "X").replace(".", ",").replace("X", "."))
        st.write(f"Maior Venda: R$ {filtered_df['Valor'].max():,.2f}".replace(",", "X").replace(".", ",").replace("X", "."))
        st.write(f"Menor Venda: R$ {filtered_df['Valor'].min():,.2f}".replace(",", "X").replace(".", ",").replace("X", "."))
    
else:
    st.info('Faça o upload de um arquivo CSV para começar a análise.')
    st.markdown("""
    ### Formato esperado do arquivo CSV:
    - **Coluna A**: Data (no formato dd/mm/aaaa ou semelhante)
    - **Coluna B**: Cliente (nome ou identificador do cliente)
    - **Coluna C**: Valor (valor da venda, numérico)
    
    ### Exemplo de conteúdo:
    ```
    Data,Cliente,Valor
    01/01/2023,Cliente A,1500.00
    02/01/2023,Cliente B,2300.50
    03/01/2023,Cliente A,750.25
    ```
    """)