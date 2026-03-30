import streamlit as st
import sqlite3
import os
import time

# ================= CONFIG =================
st.set_page_config(layout="wide")

# ================= DATABASE =================
conn = sqlite3.connect("properties.db", check_same_thread=False)
c = conn.cursor()

c.execute("""
CREATE TABLE IF NOT EXISTS properties (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT,
    price TEXT,
    location TEXT,
    details TEXT,
    images TEXT,
    video TEXT,
    created_at TEXT
)
""")

# FIX OLD DB
try:
    c.execute("ALTER TABLE properties ADD COLUMN video TEXT")
except:
    pass

try:
    c.execute("ALTER TABLE properties ADD COLUMN created_at TEXT")
except:
    pass

# ================= SESSION =================
if "favorites" not in st.session_state:
    st.session_state["favorites"] = []

# ================= PREMIUM STYLE =================
st.markdown("""
<style>

/* BACKGROUND */
[data-testid="stAppViewContainer"] {
    background: linear-gradient(135deg, #0f2027, #203a43, #2c5364);
}

/* GLOBAL TEXT */
h1,h2,h3,h4,h5,h6,p,span,label {
    color: #ffffff !important;
}

/* CARD STYLE */
.card {
    background: rgba(255,255,255,0.05);
    padding: 15px;
    border-radius: 15px;
    backdrop-filter: blur(10px);
    box-shadow: 0 8px 32px rgba(0,0,0,0.3);
    margin-bottom: 20px;
}

/* TITLE */
.title {
    font-size: 20px;
    font-weight: bold;
    color: #ffffff;
}

/* PRICE HIGHLIGHT */
.price {
    color: #00ffcc;
    font-size: 18px;
    font-weight: bold;
}

/* LOCATION */
.location {
    color: #cccccc;
    font-size: 14px;
}

/* BUTTON */
.stButton>button {
    background: linear-gradient(45deg, #00c6ff, #0072ff);
    color: white;
    border-radius: 8px;
}

</style>
""", unsafe_allow_html=True)

# ================= HEADER =================
st.markdown("<h1 style='text-align:center;'>NSSI Land - Calicut</h1>", unsafe_allow_html=True)

# ================= MENU =================
menu = st.sidebar.radio("Menu", ["Browse", "Post Property", "Saved"])

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

# ================= POST PROPERTY =================
if menu == "Post Property":
    st.markdown("<h2 style='color:white;'>Post Property</h2>", unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        title = st.text_input("Title")
        price = st.text_input("Price")

    with col2:
        location = st.text_input("Location")

    details = st.text_area("Details")

    images = st.file_uploader("Upload Images", accept_multiple_files=True)
    video = st.file_uploader("Upload Video", type=["mp4"])

    if st.button("Submit"):
        image_paths = []

        for img in images:
            path = os.path.join(UPLOAD_DIR, f"{int(time.time())}_{img.name}")
            with open(path, "wb") as f:
                f.write(img.getbuffer())
            image_paths.append(path)

        video_path = ""
        if video:
            video_path = os.path.join(UPLOAD_DIR, f"{int(time.time())}_{video.name}")
            with open(video_path, "wb") as f:
                f.write(video.getbuffer())

        c.execute("""
        INSERT INTO properties (title, price, location, details, images, video, created_at)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (title, price, location, details, ",".join(image_paths), video_path, str(time.time())))

        conn.commit()
        st.success("Property Added Successfully")
        st.rerun()

# ================= BROWSE =================
elif menu == "Browse":

    st.markdown("<h2>Browse Properties</h2>", unsafe_allow_html=True)

    c.execute("SELECT * FROM properties ORDER BY id DESC")
    data = c.fetchall()

    # 2x2 GRID
    cols = st.columns(2)

    for i, prop in enumerate(data):
        with cols[i % 2]:

            st.markdown('<div class="card">', unsafe_allow_html=True)

            # IMAGE
            if prop[5]:
                img = prop[5].split(",")[0]
                if os.path.exists(img):
                    st.image(img, use_container_width=True)

            # TEXT
            st.markdown(f'<div class="title">{prop[1]}</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="price">₹ {prop[2]}</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="location">{prop[3]}</div>', unsafe_allow_html=True)

            # BUTTONS
            if st.button("Save", key=f"s{prop[0]}"):
                st.session_state["favorites"].append(prop[0])

            share = f"{prop[1]} | {prop[2]} | {prop[3]}"
            link = "https://wa.me/?text=" + share.replace(" ", "%20")
            st.markdown(f"[Share on WhatsApp]({link})")

            st.markdown('</div>', unsafe_allow_html=True)

# ================= SAVED =================
elif menu == "Saved":

    st.markdown("<h2>Saved Properties</h2>", unsafe_allow_html=True)

    c.execute("SELECT * FROM properties")
    data = c.fetchall()

    for prop in data:
        if prop[0] in st.session_state["favorites"]:
            st.write(f"{prop[1]} - ₹{prop[2]} - {prop[3]}")
