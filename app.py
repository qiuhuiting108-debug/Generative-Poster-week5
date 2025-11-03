import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import io, random, os

# ---------- Page Config ----------
st.set_page_config(page_title="Generative Poster Studio", layout="wide")

PALETTE_FILE = "palette.csv"

# ---------- Palette Manager ----------
def load_palette():
    if not os.path.exists(PALETTE_FILE):
        df = pd.DataFrame({
            "name": ["sky", "sun", "forest"],
            "r": [0.4, 1.0, 0.2],
            "g": [0.7, 0.8, 0.6],
            "b": [1.0, 0.2, 0.2],
        })
        df.to_csv(PALETTE_FILE, index=False)
    return pd.read_csv(PALETTE_FILE)

def save_palette(df):
    df.to_csv(PALETTE_FILE, index=False)

# ---------- Blob Function ----------
def spiky_blob(cx, cy, r=1.0, wobble=0.2, n=150):
    ang = np.linspace(0, 2 * np.pi, n)
    rad = r * (1 + wobble * np.random.randn(n))
    x = cx + rad * np.cos(ang)
    y = cy + rad * np.sin(ang)
    return x, y

# ---------- Poster Generation ----------
def generate_poster(df, layers=8, wobble=0.15, seed=0, edge=False, edge_color=(0, 0, 0, 0.4)):
    if seed:
        np.random.seed(seed)
        random.seed(seed)
    fig, ax = plt.subplots(figsize=(6, 8))
    ax.axis("off")

    colors = df[["r", "g", "b"]].values
    for _ in range(layers):
        color = random.choice(colors)
        rgba = (*color, 0.5)
        cx, cy = random.uniform(-2, 2), random.uniform(-2, 2)
        r = random.uniform(1.0, 3.0)
        x, y = spiky_blob(cx, cy, r, wobble)
        ax.fill(x, y, color=rgba, ec=edge_color if edge else None, lw=0.7)

    ax.text(0, 3.7, "Generative Poster • CSV", fontsize=18, weight="bold", ha="center")
    ax.set_xlim(-4, 4)
    ax.set_ylim(-4, 4)
    return fig

# ---------- Sidebar UI ----------
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

# ---------- Poster Settings ----------
st.sidebar.header("⚙️ Poster Settings")
palette_mode = st.sidebar.selectbox("Palette Mode", ["CSV"])
layers = st.sidebar.slider("Number of Layers", 3, 20, 8)
wobble = st.sidebar.slider("Wobble Intensity", 0.05, 0.5, 0.15)
seed = st.sidebar.number_input("Seed (for randomness)", min_value=0, step=1, value=0)

st.sidebar.subheader("Edge Color Option")
edge_mode = st.sidebar.radio("", ["No Edge", "Custom Color"], index=0)
edge_color = st.sidebar.color_picker("Pick Edge Color", "#000000") if edge_mode == "Custom Color" else "#000000"

# ---------- Main Content ----------
st.title("🎨 Generative Poster Studio")
st.write("Generate algorithmic art using CSV palettes or extracted image palettes!")

st.subheader("🎨 Current Palette Preview")
cols = st.columns(len(df))
for i, row in df.iterrows():
    cols[i].markdown(f"<div style='background-color: rgb({int(row.r*255)}, {int(row.g*255)}, {int(row.b*255)}); height: 100px'></div>", unsafe_allow_html=True)

if st.button("🎨 Generate Poster"):
    edge_bool = edge_mode == "Custom Color"
    ec_rgba = tuple(int(edge_color.lstrip("#")[i:i+2], 16)/255 for i in (0, 2, 4)) + (0.5,)
    fig = generate_poster(df, layers, wobble, seed, edge_bool, ec_rgba)
    st.pyplot(fig)

    buf = io.BytesIO()
    fig.savefig(buf, format="png", dpi=300, bbox_inches="tight")
    st.download_button("💾 Download Poster (PNG)", data=buf.getvalue(), file_name="GenerativePosterStudio.png", mime="image/png")
else:
    st.info("Adjust sliders and click **Generate Poster** to create your art.")
