import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(layout="wide")

df = pd.read_csv(filepath_or_buffer="queimadas.csv", sep= ",", decimal=".")

print(df)

df["Data"] = pd.to_datetime(df["Data"])
df = df.sort_values("Data")

df["Mês"] = df["Data"].apply(lambda x: str(x.year) + "-" + str(x.month))

month = st.sidebar.selectbox("Mês", df["Mês"].unique())
df_filtered = df[df["Mês"] == month]



estados = st.sidebar.multiselect("Estado", df["Estado"].unique(), default=df["Estado"].unique())

biomas = st.sidebar.multiselect("Bioma", df["Bioma"].unique(), default=df["Bioma"].unique())

st.sidebar.image("fatec_pompeia.jpg", use_container_width=True)

if estados:
    df_filtered = df_filtered[df_filtered["Estado"].isin(estados)]

if biomas:
    df_filtered = df_filtered[df_filtered["Bioma"].isin(biomas)]

st.title("Projeto Integrador 2025 - Incêndios florestais e secas no Brasil")

st.write("Prof. Ronnie Shida Marinho")

st.write("Leonardo, João Victor, Joice e Luana")

st.markdown("## Resumo")


municipio = df_filtered.shape[0]
semchuva = df_filtered["Número de dias sem chuva"].mean()
chuva = df_filtered["Precipitação média"].mean()

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(label= "Dados em Municipios", value= municipio)

with col2:
    st.metric(label= "Precipitação Média", value= f'{chuva:.2f} mm³'. replace(".", ","))

with col3:
    st.metric(label= "Média de dias sem chuva", value= f'{semchuva:.2f}'. replace(".",","))

fig_date = px.bar(df_filtered, x="Data", y="Precipitação média", color="Bioma", title= "Chuva de acordo com o bioma")
#col1.plotly_chart(fig_date, use_container_width=True)
st.plotly_chart(fig_date, use_container_width=True)

col1, col2 = st.columns(2)

fig_pri = px.bar(df_filtered, x='Estado', y="Risco de fogo por período", color= "Estado", title= "Risco de incendio por estado durante o periodo analisado", orientation="v")
col1.plotly_chart(fig_pri, use_container_width=True)

fig_kind = px.pie(df_filtered, values="Risco de fogo médio", names="Bioma", title= "Risco de fogo por bioma")
col2.plotly_chart(fig_kind, use_container_width=True)

fig_seca = px.bar(df_filtered, x='Bioma', y="Número de dias sem chuva", color= "Bioma", title= "Dias sem chuva totais por bioma", orientation="v")
st.plotly_chart(fig_seca, use_container_width=True)

st.markdown("  Este projeto foi desenvolvido por alunos da Faculdade de Tecnologia Pompeia Shunji Nishimura do curso Tecnologia em Sistemas Inteligentes.")