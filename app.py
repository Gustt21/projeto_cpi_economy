import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import os
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler

# --- 1. CONFIGURAÇÃO ---
st.set_page_config(page_title="Global Corruption Tracker", page_icon="🌍", layout="wide")

# --- 2. CARREGAMENTO ---
@st.cache_data
def carregar_dados():
    caminhos = ['datasets/dataset_dashboard.csv', '../datasets/dataset_dashboard.csv', 'dataset_dashboard.csv']
    for caminho in caminhos:
        if os.path.exists(caminho):
            return pd.read_csv(caminho)
    return None

df_full = carregar_dados()

if df_full is None:
    st.error("❌ Erro: Base de dados não encontrada.")
    st.stop()

# Criar dataframe apenas com o ano mais recente para os mapas e rankings
ano_max = df_full['ano'].max()
df_recente = df_full[df_full['ano'] == ano_max].copy()

# --- 3. SIDEBAR ---
st.sidebar.title("🌍 Filtros Globais")

# Filtro de Continente
todos_continentes = sorted(df_recente['Continente'].unique())
sel_continentes = st.sidebar.multiselect("Continentes:", todos_continentes, default=todos_continentes)
df_filtrado = df_recente[df_recente['Continente'].isin(sel_continentes)]

st.sidebar.markdown("---")
st.sidebar.caption(f"Dados até: {ano_max}")

# --- 4. LAYOUT PRINCIPAL ---
st.title("🛡️ A Geografia da Honestidade")
st.markdown("Monitoramento global da relação entre Riqueza, Imprensa e Corrupção.")

# Abas
tab1, tab2, tab3, tab4 = st.tabs(["🗺️ Visão Global", "🔍 Perfil do País (Drill-down)", "📰 Imprensa & Correlações", "🤖 IA Clusters"])

# --- ABA 1: VISÃO GLOBAL ---
with tab1:
    # KPIs
    c1, c2, c3 = st.columns(3)
    c1.metric("Países na Amostra", len(df_filtrado))
    c2.metric("Média Global CPI", f"{df_filtrado['CPI_Score'].mean():.1f}")
    c3.metric("Média Imprensa", f"{df_filtrado.get('Press_Freedom_Score', pd.Series([0])).mean():.1f}")

    # Mapa
    fig_map = px.choropleth(
        df_filtrado, locations="Country", locationmode="country names",
        color="CPI_Score", hover_name="Country", color_continuous_scale="RdBu",
        title="Mapa de Calor: Corrupção (Azul = Honesto, Vermelho = Corrupto)"
    )
    st.plotly_chart(fig_map, use_container_width=True)

    # Ranking
    st.subheader("🏆 Top 10 Melhores vs Piores (Região Selecionada)")
    col_melhor, col_pior = st.columns(2)
    with col_melhor:
        st.dataframe(df_filtrado.nlargest(10, 'CPI_Score')[['Country', 'CPI_Score']].set_index('Country'))
    with col_pior:
        st.dataframe(df_filtrado.nsmallest(10, 'CPI_Score')[['Country', 'CPI_Score']].set_index('Country'))

# --- ABA 2: PERFIL DO PAÍS (NOVIDADE!) ---
with tab2:
    st.header("📊 Boletim do País")
    
    # Seletor de País
    lista_paises = sorted(df_full['Country'].unique())
    # Tenta colocar o Brasil como padrão se existir
    idx_padrao = lista_paises.index('Brazil') if 'Brazil' in lista_paises else 0
    pais_selecionado = st.selectbox("Selecione um País para ver o histórico:", lista_paises, index=idx_padrao)
    
    # Dados do País
    df_pais = df_full[df_full['Country'] == pais_selecionado].sort_values('ano')
    
    if not df_pais.empty:
        # Pega valores atuais e anteriores
        atual = df_pais.iloc[-1]
        score_atual = atual['CPI_Score']
        
        # Delta (Variação desde o primeiro ano registrado)
        score_inicial = df_pais.iloc[0]['CPI_Score']
        delta = score_atual - score_inicial
        
        # KPIs do País
        k1, k2, k3 = st.columns(3)
        k1.metric("CPI Score (Atual)", f"{score_atual:.1f}", delta=f"{delta:.1f} (vs {df_pais.iloc[0]['ano']})")
        k2.metric("PIB per Capita", f"US$ {atual['PIB_per_Capita']:,.0f}" if pd.notnull(atual['PIB_per_Capita']) else "N/A")
        k3.metric("Liberdade Imprensa", f"{atual['Press_Freedom_Score']:.1f}" if pd.notnull(atual.get('Press_Freedom_Score')) else "N/A")
        
        # Gráfico de Linha (Histórico)
        fig_hist = go.Figure()
        
        # Linha do País
        fig_hist.add_trace(go.Scatter(
            x=df_pais['ano'], y=df_pais['CPI_Score'],
            mode='lines+markers', name=pais_selecionado,
            line=dict(color='blue', width=4)
        ))
        
        # Média da Região (Contexto)
        continente_pais = atual['Continente']
        df_regiao = df_full[df_full['Continente'] == continente_pais].groupby('ano')['CPI_Score'].mean().reset_index()
        
        fig_hist.add_trace(go.Scatter(
            x=df_regiao['ano'], y=df_regiao['CPI_Score'],
            mode='lines', name=f"Média {continente_pais}",
            line=dict(color='gray', dash='dot')
        ))
        
        fig_hist.update_layout(title=f"Evolução Histórica: {pais_selecionado} vs Região", xaxis_title="Ano", yaxis_title="CPI Score")
        st.plotly_chart(fig_hist, use_container_width=True)
        
    else:
        st.warning("Sem dados históricos para este país.")

# --- ABA 3: IMPRENSA (Scatter) ---
with tab3:
    st.header("Análise de Correlação")
    
    cols = ['Press_Freedom_Score', 'CPI_Score', 'PIB_per_Capita', 'IDH_2023']
    df_chart = df_filtrado.dropna(subset=[c for c in cols if c in df_filtrado.columns])
    
    if not df_chart.empty:
        fig_imp = px.scatter(
            df_chart, x="Press_Freedom_Score", y="CPI_Score",
            size="PIB_per_Capita", color="IDH_2023",
            hover_name="Country", size_max=60,
            title="Liberdade de Imprensa vs Corrupção"
        )
        st.plotly_chart(fig_imp, use_container_width=True)
    else:
        st.info("Dados insuficientes para correlação.")

# --- ABA 4: IA (K-Means) ---
with tab4:
    st.header("Agrupamento Inteligente")
    k = st.slider("Grupos", 2, 5, 3)
    
    if st.button("Rodar Clusterização"):
        cols_ml = ['CPI_Score', 'Press_Freedom_Score', 'IDH_2023', 'PIB_per_Capita']
        cols_validas = [c for c in cols_ml if c in df_filtrado.columns]
        df_ml = df_filtrado.dropna(subset=cols_validas).copy()
        
        if len(df_ml) > 10:
            scaler = StandardScaler()
            X_scaled = scaler.fit_transform(df_ml[cols_validas])
            kmeans = KMeans(n_clusters=k, random_state=42, n_init=10)
            df_ml['Cluster'] = kmeans.fit_predict(X_scaled).astype(str)
            
            fig_clus = px.scatter(
                df_ml, x=cols_validas[1], y=cols_validas[0],
                color="Cluster", hover_name="Country",
                title=f"K-Means: {k} Clusters"
            )
            st.plotly_chart(fig_clus, use_container_width=True)