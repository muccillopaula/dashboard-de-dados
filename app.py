import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="Dashboard de Dados",
    layout="wide"
)

st.title("Dashboard de Dados - Multas vencidas e não pagas de transportes em Novembro de 2025.")
st.markdown("""**Dados obtidos pelo "Dados Abertos" - Governo do Estado de São Paulo.**""")
st.write("""
Este dashboard tem como objetivo analisar as multas vencidas e não pagas registradas na base de dados, destacando as infrações mais recorrentes e os tipos de veículos com maior participação nas ocorrências.
""")

arquivo = st.file_uploader(
    "Envie um arquivo CSV",
    type=["csv"]
)

if arquivo is not None:

    df = pd.read_csv(arquivo)

    df["CATEGORIA_VEICULO"] = (
        df["CATEGORIA_VEICULO"]
        .fillna("Não Informado")
    )

    st.subheader("Visualização dos dados")
    st.dataframe(df.head())

    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
        "Quantidade de registros",
        df.shape[0]
    )

    col2.metric(
        "Quantidade de colunas",
        df.shape[1]
    )
 
    col3.metric(
        "Total de Multas",
        f"{df['QTDE'].sum():,}"
)

    col4.metric(
        "Tipos de Infração",
        df["DESCRICAO_INFRACAO"].nunique()
)

    st.subheader("Qualidade dos Dados")

    st.write("Valores ausentes:")
    st.dataframe(df.isnull().sum())

    st.write("Registros duplicados:")
    st.write(df.duplicated().sum())

    st.write("Tipos de dados:")
    st.dataframe(df.dtypes.astype(str))

#-----------------------------------------------------------------------------------------------------------------------------------
#GRÁFICOS
#-----------------------------------------------------------------------------------------------------------------------------------
    st.markdown("""
                ### **Quais são as 10 infrações de trânsito mais frequentes no geral?**
                """)
    top10_infracoes = (
        df.groupby("DESCRICAO_INFRACAO")["QTDE"]
        .sum()
        .sort_values(ascending=False)
        .head(10)
        .reset_index()
)

    fig = px.bar(
        top10_infracoes,
        x="QTDE",
        y="DESCRICAO_INFRACAO",
        orientation="h",
        title="Top 10 Infrações Mais Frequentes"
)

    fig.update_layout(yaxis={"categoryorder": "total ascending"})

    st.plotly_chart(fig, use_container_width=True)
    st.write("""
        **O que podemos observar no primeiro gráfico?**
             
        As infrações mais frequentes estão relacionadas à regularização do veículo, principalmente não registrar a transferência de propriedade no prazo e trafegar com veículo não licenciado. Em seguida aparecem infrações de segurança, como não usar cinto, usar celular ao dirigir e dirigir sem habilitação.
        """)

#_----------------------------
    st.markdown("""
                ### **Quais tipos de veículos (motocicletas, reboques, etc.) lideram o ranking de infrações de conservação ou documentação?**
                """)
    ranking_veiculos = (
        df.groupby("TIPO_VEICULO")["QTDE"]
        .sum()
        .sort_values(ascending=False)
        .reset_index()
)

    fig = px.bar(
        ranking_veiculos,
        x="TIPO_VEICULO",
        y="QTDE",
        title="Ranking de Infrações por Tipo de Veículo"
)

    st.plotly_chart(fig, use_container_width=True)
    st.write("""
        **O que podemos observar no segundo gráfico?**
             
        O gráfico mostra que os automóveis concentram a maior quantidade de infrações, seguidos pelas motocicletas. Os demais tipos de veículos apresentam números significativamente menores.
        """)
             
    st.markdown("""
### **Explicação curta sobre os gráficos**
Os gráficos mostram os tipos de infrações e os tipos de veículos que aparecem com maior frequência na base de multas vencidas e não pagas. Entre as infrações, destacam-se aquelas relacionadas à regularização do veículo, como a falta de registro da transferência de propriedade no prazo e a circulação de veículos não licenciados. Também aparecem com frequência infrações ligadas à segurança no trânsito, como não utilizar o cinto de segurança, usar o celular ao dirigir e conduzir veículo sem habilitação.
Em relação aos veículos, os automóveis concentram a maior quantidade de infrações registradas, seguidos pelas motocicletas. Os demais tipos de veículos apresentam participação menor no total de ocorrências. Esses resultados ajudam a identificar quais infrações e quais categorias de veículos são mais representativas dentro do conjunto de dados analisado.
""")
    
st.markdown("""*Trabalho feito com a utilização das Inteligências Artificiais "Gemini" e "Copilot" para verificação, correção e criação de gráficos no código.*""")

st.markdown("""**Feito por: Paula Alves Muccillo e Ana Vitória Teixeira Topa 2CDD01**""")