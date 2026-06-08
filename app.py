import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# ---------------------------
# CONFIG
# ---------------------------
st.set_page_config(
    page_title="Dashboard Climat Togo",
    page_icon="🌍",
    layout="wide"
)

# ---------------------------
# CSS (FOND ET SIDEBAR)
# ---------------------------
page_bg_img = """
<style>
/* Fond global */
.stApp {
    background-image: url("https://images.unsplash.com/photo-1500375592092-40eb2168fd21");
    background-size: cover;
    background-position: center;
    background-attachment: fixed;
}

/* Zone de contenu principale */
.block-container {
    background-color: rgba(0, 0, 0, 0.65);
    padding: 2rem;
    border-radius: 15px;
    color: white;
}

/* Barre latérale (Sidebar) */
[data-testid="stSidebar"] {
    background-color: rgba(0, 0, 0, 0.85);
    border-right: 1px solid rgba(255, 255, 255, 0.2);
}

[data-testid="stSidebar"] * {
    color: white !important;
}

/* Style Dataframe */
div[data-testid="stDataFrame"] {
    background-color: rgba(255, 255, 255, 0.9);
    border-radius: 10px;
    padding: 10px;
}

/* Titres et texte */
h1, h2, h3, p, label {
    color: white !important;
}
</style>
"""

st.markdown(page_bg_img, unsafe_allow_html=True)

# ---------------------------
# DATA
# ---------------------------
@st.cache_data
def load_data():
    # Assurez-vous que le fichier est bien présent dans le répertoire
    df = pd.read_csv("ObservationData_wuyikjc.csv")
    df["Date"] = pd.to_datetime(df["Date"], errors="coerce")
    return df

df = load_data()

# ---------------------------
# SIDEBAR (Filtres)
# ---------------------------
with st.sidebar:
    st.header("⚙️ Paramètres")
    ville = st.selectbox("Ville", df["ville"].unique())
    indicateur = st.selectbox("Indicateur", df["indicateur"].unique())

# ---------------------------
# TITRE ET FILTRAGE
# ---------------------------
st.title("🌍 Dashboard Climat du Togo")
df_filtre = df[
    (df["ville"] == ville) &
    (df["indicateur"] == indicateur)
].sort_values("Date")

# ---------------------------
# KPI
# ---------------------------
col1, col2, col3 = st.columns(3)

col1.metric("Moyenne", f"{df_filtre['Value'].mean():.2f}")
col2.metric("Min", f"{df_filtre['Value'].min():.2f}")
col3.metric("Max", f"{df_filtre['Value'].max():.2f}")

# ---------------------------
# GRAPHIQUE
# ---------------------------
st.subheader(f"Graphique : {indicateur} à {ville}")
fig, ax = plt.subplots(facecolor='none') # Fond transparent pour le graphique
ax.plot(df_filtre["Date"], df_filtre["Value"], marker="o", color="white", linewidth=2)
ax.set_facecolor('none')
ax.tick_params(colors='white')
ax.grid(True, linestyle='--', alpha=0.5)

st.pyplot(fig)

# ---------------------------
# TABLEAU
# ---------------------------
st.subheader("📋 Données")
st.dataframe(df_filtre, use_container_width=True)