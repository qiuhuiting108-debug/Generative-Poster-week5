import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import random, io

# ---------- PAGE CONFIG ----------
st.set_page_config(page_title="Interactive Poster • CSV", layout="centered")

# ---------- LOAD PALETTE ----------
@st.cache_data
def read_palette():
    df = pd.read_csv("palette.csv")
    return df[["r", "g", "b"]].values.tolist()

# ---------- SPIKY BLOB ----------
def spiky_blob(cx, cy, radius=1.0, wobble=0.2, spikes=150):
    ang = np.linspace(0, 2 * np.pi, spikes)
    rad = radius * (1 + wobble * np.random.randn(spikes))
    x = cx + rad * np.cos(ang)
    y = cy + rad * np.sin(ang)
    return x, y

# ---------- POSTER FUNCTION ----------
def generate_poster(palette, layers, wobble, seed):
    if seed:
        np.random.seed(seed)
        random.seed(seed)
    fig, ax = plt.subplots(figsize=(6, 8))
    ax.axis("off")

    # 绘制多层 spiky 花瓣
    for _ in range(layers):
        color = random.choice(palette)
        rgba = (*color, 0.45)   # 半透明填充
        ec = (0, 0, 0, 0.55)    # 黑色描边
        cx, cy = random.uniform(-2, 2), random.uniform(-2, 2)
        r = random.uniform(1.3, 3.2)
        x, y = spiky_blob(cx, cy, r, wobble)
        ax.fill(x, y, color=rgba, ec=ec, lw=0.8)

    ax.text(0, 3.8, "Interactive Poster • csv",
            fontsize=18, weight="bold", ha="center")
    ax.set_xlim(-4, 4)
    ax.set_ylim(-4, 4)
    return fig

# ---------- UI ----------
st.title("🎨 Interactive Poster • CSV")

# Controls
layers = st.slider("Layers", 5, 30, 14)
wobble = st.slider("Wobble", 0.05, 0.6, 0.43)
palette_mode = st.selectbox("Palette Mode", ["csv"])
seed = st.slider("Seed", 0, 100, 42)

generate = st.button("🎨 Generate Poster")

# ---------- Generate and Show ----------
palette = read_palette()

if generate:
    fig = generate_poster(palette, layers, wobble, seed)
    st.pyplot(fig)
    buf = io.BytesIO()
    fig.savefig(buf, format="png", dpi=300, bbox_inches="tight")
    st.download_button("💾 Download Poster", data=buf.getvalue(),
                       file_name="InteractivePoster_csv.png", mime="image/png")
else:
    st.info("Adjust sliders and click **Generate Poster** to create your art.")
