import streamlit as st
import requests
import pandas as pd
import plotly.express as px

# 1. Configuração da página - Leve e Otimizada
st.set_page_config(
    page_title="Painel Climático Metropolitano",
    page_icon="⛅",
    layout="wide"
)

# CSS Customizado com foco em Alto Contraste, Leveza e Acessibilidade em telas móveis
st.markdown("""
    <style>
    .main {
        background-color: #0e1117;
    }
    .stMetric {
        background-color: #161b22;
        padding: 14px;
        border-radius: 8px;
        border: 1px solid #30363d;
    }
    .resumo-card {
        background-color: #161b22;
        padding: 16px;
        border-radius: 8px;
        border-left: 5px solid #38bdf8;
        margin-bottom: 16px;
        color: #e6edf3;
        font-size: 15px;
        line-height: 1.5;
    }
    .dica-card {
        background-color: #161b22;
        padding: 14px;
        border-radius: 8px;
        border: 1px solid #30363d;
        margin-top: 10px;
    }
    </style>
""", unsafe_allow_html=True)

# 2. Barra Lateral (Sidebar) Minimalista
with st.sidebar:
    st.title("⛅ Clima Metropolitano")
    st.caption("Painel Comunitário de Alta Velocidade")
    st.markdown("---")
    
    cidades = {
        "Eusébio": {"lat": -3.8889, "lon": -38.4556},
        "Fortaleza": {"lat": -3.7172, "lon": -38.5437},
        "Aquiraz": {"lat": -3.9006, "lon": -38.3911},
        "Caucaia": {"lat": -3.7361, "lon": -38.6531}
    }
    
    cidade_selecionada = st.selectbox("📍 Selecione a cidade:", list(cidades.keys()))
    coords = cidades[cidade_selecionada]
    
    st.markdown("---")
    if st.button("🔄 Atualizar Agora", use_container_width=True):
        st.cache_data.clear()
        st.rerun()
        
    st.markdown("---")
    st.caption("Projeto Extensionista • Focado em Acessibilidade e Utilidade Pública para a Região Metropolitana do Ceará.")

# 3. Busca de Dados Otimizada (Com UV Index e Cache Otimizado)
@st.cache_data(ttl=600)
def carregar_dados_climaticos(lat, lon):
    url = (
        f"https://api.open-meteo.com/v1/forecast?"
        f"latitude={lat}&longitude={lon}"
        f"&current=temperature_2m,relative_humidity_2m,apparent_temperature,precipitation,wind_speed_10m,surface_pressure,uv_index"
        f"&hourly=temperature_2m,relative_humidity_2m"
        f"&daily=temperature_2m_max,temperature_2m_min,uv_index_max"
        f"&models=ecmwf_ifs025"
        f"&timezone=America%2FFortaleza"
    )
    try:
        res = requests.get(url, timeout=5)
        if res.status_code == 200:
            return res.json()
    except Exception:
        return None
    return None

dados = carregar_dados_climaticos(coords["lat"], coords["lon"])

# Cabeçalho da Área Principal
st.title(f"⛅ {cidade_selecionada}")
st.caption("Dados meteorológicos em tempo real • Otimizado para consumo em redes móveis")

if dados:
    atual = dados.get("current", {})
    temp_atual = atual.get('temperature_2m')
    sensacao = atual.get('apparent_temperature')
    umidade = atual.get('relative_humidity_2m')
    vento = atual.get('wind_speed_10m')
    chuva = atual.get('precipitation')
    pressao = atual.get('surface_pressure')
    
    # Tratamento seguro caso o UV venha como None
    uv_index = atual.get('uv_index')
    if uv_index is None:
        uv_index = 0.0
    
    # 4. Avaliação das Condições para Dicas Úteis ao Cidadão
    if uv_index >= 8:
        uv_status = "Muito Alto 🟣"
        uv_dica = "Evite exposição direta ao sol. Use protetor solar, óculos e chapéu."
    elif uv_index >= 6:
        uv_status = "Alto 🟠"
        uv_dica = "Proteção solar recomendada se for permanecer ao ar livre."
    elif uv_index >= 3:
        uv_status = "Moderado 🟡"
        uv_dica = "Condições agradáveis, mas use proteção se passar muito tempo ao sol."
    else:
        uv_status = "Baixo 🟢"
        uv_dica = "Nível de radiação seguro para atividades ao ar livre."

    # Classificação de Hidratação/Mormaço
    if temp_atual is not None and (temp_atual > 31 or (sensacao and sensacao > 34)):
        hidrata_dica = "Sensação de mormaço elevada. Beba bastante água ao longo do dia."
    elif umidade is not None and umidade < 50:
        hidrata_dica = "Umidade em declínio. Mantenha a hidratação reforçada."
    else:
        hidrata_dica = "Níveis de umidade e temperatura dentro da faixa normal."

    # Resumo Inteligente do Dia
    resumo_texto = f"""
    <div class="resumo-card">
        <b>💡 Resumo para o morador:</b> Agora faz <b>{temp_atual}°C</b> em {cidade_selecionada} (sensação de <b>{sensacao}°C</b>). 
        Índice UV em <b>{uv_index:.1f} ({uv_status})</b>. Ventos a <b>{vento} km/h</b>.
    </div>
    """
    st.markdown(resumo_texto, unsafe_allow_html=True)

    # 5. Cartões de Saúde & Recomendações Úteis
    c_dica1, c_dica2 = st.columns(2)
    with c_dica1:
        st.markdown(f"""
        <div class="dica-card">
            <b>☀️ Radiação Solar (UV: {uv_index:.1f}):</b><br>
            <span style="color:#93c5fd;">{uv_dica}</span>
        </div>
        """, unsafe_allow_html=True)
    with c_dica2:
        st.markdown(f"""
        <div class="dica-card">
            <b>💧 Recomendação de Saúde:</b><br>
            <span style="color:#93c5fd;">{hidrata_dica}</span>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")

    # 6. Métricas em Grade Limpa (Acessibilidade)
    st.subheader("Condições Meteorológicas Detalhadas")
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Temperatura", f"{temp_atual} °C")
    with col2:
        st.metric("Sensação Térmica", f"{sensacao} °C")
    with col3:
        st.metric("Índice UV", f"{uv_index:.1f}")
    with col4:
        st.metric("Umidade", f"{umidade} %")
        
    col5, col6, col7, col8 = st.columns(4)
    with col5:
        st.metric("Vento", f"{vento} km/h")
    with col6:
        st.metric("Chuva", f"{chuva} mm")
    with col7:
        st.metric("Pressão", f"{pressao} hPa")
    with col8:
        st.metric("Status da Rede", "Online 🟢")
        
    st.divider()

    # 7. Gráficos Leves e Otimizados
    g1, g2 = st.columns(2)

    with g1:
        st.markdown("### Evolução da Temperatura (Próximas 24h)")
        horas_dt = pd.to_datetime(dados["hourly"]["time"][:24])
        df_hourly = pd.DataFrame({
            "Horário": horas_dt.strftime('%H:%M'),
            "Temperatura (°C)": dados["hourly"]["temperature_2m"][:24]
        })
        
        fig_hora = px.line(
            df_hourly, x="Horário", y="Temperatura (°C)",
            markers=True, template="plotly_dark"
        )
        fig_hora.update_traces(line_color="#38bdf8", marker_size=6, line_width=2)
        fig_hora.update_layout(
            xaxis_title="Horário", 
            yaxis_title="°C",
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            margin=dict(l=10, r=10, t=10, b=10)
        )
        st.plotly_chart(fig_hora, use_container_width=True, config={"editable": False, "displayModeBar": False})

    with g2:
        st.markdown("### Previsão para os Próximos Dias")
        dias_dt = pd.to_datetime(dados["daily"]["time"])
        df_daily = pd.DataFrame({
            "Data": dias_dt.strftime('%d/%m'),
            "Mínima": dados["daily"]["temperature_2m_min"],
            "Máxima": dados["daily"]["temperature_2m_max"]
        })
        
        df_daily_melted = df_daily.melt(id_vars="Data", value_vars=["Mínima", "Máxima"],
                                        var_name="Tipo", value_name="°C")
        
        fig_dias = px.bar(
            df_daily_melted, x="Data", y="°C", color="Tipo",
            barmode="group", template="plotly_dark",
            color_discrete_map={"Mínima": "#60a5fa", "Máxima": "#fb923c"}
        )
        fig_dias.update_layout(
            xaxis_title="Data", 
            yaxis_title="°C", 
            legend_title="",
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            margin=dict(l=10, r=10, t=10, b=10)
        )
        st.plotly_chart(fig_dias, use_container_width=True, config={"editable": False, "displayModeBar": False})

else:
    st.error("Erro ao carregar dados da API para esta localidade.")