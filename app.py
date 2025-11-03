import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import random, io, os

# ---------- PAGE CONFIG ----------
st.set_page_config(page_title="Generative Poster Studio", layout="wide")

PALETTE_FILE = "palette.csv"

# ---------- PALETTE ----------
def load_palette():
    if not os.path.exists(PALETTE_FILE):
        df = pd.DataFrame({
            "name": ["sky", "sun", "forest"],
            "r": [0.4, 1.0, 0.2],
            "g": [0.7, 0.8, 0.6],
            "b": [1.0, 0.2, 0.2]
        })
        df.to_csv(PALETTE_FILE, index=False)
    return pd.read_csv(PALETTE_FILE)

def save_palette(df):
    df.to_csv(PALETTE_FILE, index=False)

# ---------- GENERATIVE BLOB ----------
def spiky_blob(cx, cy, r=1.0, wobble=0.2, n=150):
    ang = np.linspace(0, 2*np.pi, n)
    rad = r * (1 + wobble * np.random.randn(n))
    x = cx + rad * np.cos(ang)
    y = cy + rad * np.sin(ang)
    return x, y

# ---------- GENERATE POSTER ----------
def generate_poster(df, layers=8, wobble=0.15, seed=0, edge_color=(0, 0, 0, 0.55)):
    if seed:
        np.random.seed(seed)
        random.seed(seed)

    fig, ax = plt.subplots(figsize=(6, 8))
    ax.axis("off")

    colors = df[["r", "g", "b"]].values
    for _ in range(layers):
        color = random.choice(colors)
        rgba = (*color, 0.45)
        cx, cy = random.uniform(-2, 2), random.uniform(-2, 2)
        r = random.uniform(1.2, 3.0)
        x, y = spiky_blob(cx, cy, r, wobble)
        ax.fill(x, y, color=rgba, ec=edge_color, lw=0.7)

    ax.text(0, 3.8, "Interactive Poster • csv", fontsize=18, weight="bold", ha="center")
    ax.set_xlim(-4, 4)
    ax.set_ylim(-4, 4)
    return fig

# ---------- SIDEBAR ----------
st.sidebar.header("🎨 Manage Palette (palette.csv)")
df = load_palette()
edited_df = st.sidebar.data_editor(df, num_rows="dynamic")
if not edited_df.equals(df):
    save_palette(edited_df)
    st.sidebar.success("Palette updated!")

if st.sidebar.button("➕ Add New Color"):
    new_row = pd.DataFrame({"name": ["new"], "r": [0.5], "g": [0.5], "b": [0.5]})
    df = pd.concat([df, new_row], ignore_index=True)
    save_palette(df)
    st.sidebar.experimental_rerun()

if st.sidebar.button("❌ Delete Color"):
    if len(df) > 0:
        df = df.iloc[:-1]
        save_palette(df)
        st.sidebar.experimental_rerun()

st.sidebar.header("⚙️ Poster Settings")
palette_mode = st.sidebar.selectbox("Palette Mode", ["CSV"])
layers = st.sidebar.slider("Number of Layers", 5, 30, 14)
wobble = st.sidebar.slider("Wobble Intensity", 0.05, 0.6, 0.43)
seed = st.sidebar.slider("Seed (for randomness)", 0, 100, 42)

# ---------- MAIN ----------
st.title("🎨 Generative Poster Studio")
st.write("Generate algorithmic art using CSV palettes or extracted image palettes!")

st.subheader("🎨 Current Palette Preview")
cols = st.columns(len(df))
for i, row in df.iterrows():
    cols[i].markdown(
        f"<div style='background-color: rgb({int(row.r*255)}, {int(row.g*255)}, {int(row.b*255)}); height: 100px;'></div>",
        unsafe_allow_html=True
    )

if st.button("🎨 Generate Poster"):
    fig = generate_poster(df, layers, wobble, seed)
    st.pyplot(fig)

    buf = io.BytesIO()
    fig.savefig(buf, format="png", dpi=300, bbox_inches="tight")
    st.download_button("💾 Download Poster (PNG)", data=buf.getvalue(),
                       file_name="InteractivePoster_csv.png", mime="image/png")
else:
    st.info("Adjust sliders and click **Generate Poster** to create your art.")
