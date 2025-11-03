import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import random, io

# ---------- PAGE CONFIG ----------
st.set_page_config(page_title="Interactive Poster • CSV", layout="centered")

# ---------- READ PALETTE ----------
@st.cache_data
def read_palette_from_csv():
    df = pd.read_csv("palette.csv")
    return df[["r", "g", "b"]].values.tolist()

# ---------- GENERATIVE FUNCTION ----------
def generate_spiky_blob(xc, yc, radius=1.0, wobble=0.2, spikes=150):
    ang = np.linspace(0, 2*np.pi, spikes)
    r = radius * (1 + wobble * np.random.randn(spikes))
    x = xc + r * np.cos(ang)
    y = yc + r * np.sin(ang)
    return x, y

def generate_poster(layers, wobble, palette, seed=None):
    if seed:
        np.random.seed(seed)
        random.seed(seed)

    fig, ax = plt.subplots(figsize=(6, 8))
    ax.axis("off")

    # 绘制层叠花瓣
    for _ in range(layers):
        color = random.choice(palette)
        rgba = (*color, 0.4)
        ec = (0, 0, 0, 0.5)
        cx, cy = random.uniform(-2, 2), random.uniform(-2, 2)
        r = random.uniform(1.2, 3.0)
        x, y = generate_spiky_blob(cx, cy, r, wobble)
        ax.fill(x, y, color=rgba, ec=ec, lw=0.7)

    ax.text(0, 3.7, "Interactive Poster • csv",
            fontsize=18, weight="bold", ha="center")
    ax.set_xlim(-4, 4)
    ax.set_ylim(-4, 4)
    return fig

# ---------- SIDEBAR CONTROLS ----------
st.title("🎨 Interactive Poster • csv")

palette_mode = st.selectbox("Palette Mode", ["CSV"])
layers = st.slider("Layers", 5, 30, 14)
wobble = st.slider("Wobble", 0.05, 0.6, 0.43)
seed = st.slider("Seed", 0, 100, 42)
generate = st.button("🎨 Generate Poster")

palette = read_palette_from_csv()

if generate:
    fig = generate_poster(layers, wobble, palette, seed)
    st.pyplot(fig)
    buf = io.BytesIO()
    fig.savefig(buf, format="png", dpi=300, bbox_inches="tight")
    st.download_button("💾 Download Poster (PNG)",
                       data=buf.getvalue(),
                       file_name="InteractivePoster_csv.png",
                       mime="image/png")
else:
    st.info("Adjust sliders and click **Generate Poster** to create your art.")
