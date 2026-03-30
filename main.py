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

# ================= STYLE =================
st.markdown("""
<style>
[data-testid="stAppViewContainer"] {
    background: linear-gradient(rgba(0,0,0,0.6), rgba(0,0,0,0.6)),
    url("https://images.unsplash.com/photo-1599423300746-b62533397364");
    background-size: cover;
}

h1,h2,h3,h4,h5,h6,p,span,label {
    color: white !important;
}

.block-container {
    background: rgba(0,0,0,0.5);
    border-radius: 10px;
}

.stButton>button {
    background-color: #1f77b4;
    color: white;
}

</style>
""", unsafe_allow_html=True)

# ================= HEADER =================
st.title("NSSI Land - Calicut")

# ================= MENU =================
menu = st.sidebar.radio("Menu", ["Browse Properties", "Post Property", "Saved"])

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

# ================= POST PROPERTY =================
if menu == "Post Property":
    st.markdown("<h2 style='color:black;'>Post Property</h2>", unsafe_allow_html=True)

    colA, colB = st.columns(2)

    with colA:
        title = st.text_input("Title")
        price = st.text_input("Price")

    with colB:
        location = st.text_input("Location")

    details = st.text_area("Details")

    images = st.file_uploader("Upload Images", accept_multiple_files=True)
    video = st.file_uploader("Upload Video", type=["mp4"])

    if st.button("Submit Property"):
        image_paths = []

        for img in images:
            file_path = os.path.join(UPLOAD_DIR, f"{int(time.time())}_{img.name}")
            with open(file_path, "wb") as f:
                f.write(img.getbuffer())
            image_paths.append(file_path)

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
        st.success("Property Added")
        st.rerun()

# ================= BROWSE (DEFAULT) =================
elif menu == "Browse Properties":

    st.header("Browse Properties")

    c.execute("SELECT * FROM properties ORDER BY id DESC")
    properties = c.fetchall()

    # GRID VIEW (4 COLUMNS)
    cols = st.columns(4)

    for i, prop in enumerate(properties):
        with cols[i % 4]:

            # IMAGE
            if prop[5]:
                img = prop[5].split(",")[0]
                if os.path.exists(img):
                    st.image(img, use_container_width=True)

            # DETAILS
            st.subheader(prop[1])
            st.write(prop[2])
            st.write(prop[3])

            # SAVE
            if st.button("Save", key=f"fav_{prop[0]}"):
                st.session_state["favorites"].append(prop[0])

            # WHATSAPP SHARE
            share_text = f"{prop[1]} | {prop[2]} | {prop[3]}"
            share_url = "https://wa.me/?text=" + share_text.replace(" ", "%20")
            st.markdown(f"[Share]({share_url})")

# ================= FAVORITES =================
elif menu == "Saved":

    st.header("Saved Properties")

    c.execute("SELECT * FROM properties")
    properties = c.fetchall()

    for prop in properties:
        if prop[0] in st.session_state["favorites"]:
            st.write(f"{prop[1]} - {prop[2]} - {prop[3]}")
