# -*- coding: utf-8 -*-
import streamlit as st
import sqlite3
import os
import uuid

# -------------------- CONFIG --------------------
st.set_page_config(page_title="NSSI Land", layout="wide")

# -------------------- DATABASE --------------------
conn = sqlite3.connect("nssi.db", check_same_thread=False)
c = conn.cursor()

c.execute("""
CREATE TABLE IF NOT EXISTS properties (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    owner TEXT,
    location TEXT,
    price TEXT,
    details TEXT,
    images TEXT
)
""")

# Fix old DB
try:
    c.execute("ALTER TABLE properties ADD COLUMN images TEXT")
except:
    pass

conn.commit()

# -------------------- STYLE --------------------
st.markdown("""
<style>
[data-testid="stAppViewContainer"] {
    background-image: url("https://images.unsplash.com/photo-1600607687939-ce8a6c25118c");
    background-size: cover;
    background-position: center;
    background-attachment: fixed;
}

[data-testid="stAppViewContainer"]::before {
    content: "";
    position: fixed;
    width: 100%;
    height: 100%;
    background: rgba(0,0,0,0.6);
    z-index: -1;
}

html, body, [class*="css"] {
    color: white !important;
}

.card {
    background: rgba(255,255,255,0.08);
    padding: 15px;
    border-radius: 15px;
    margin-bottom: 20px;
}
</style>
""", unsafe_allow_html=True)

st.title("NSSI Land Promoters - Calicut")

# -------------------- UPLOAD FOLDER --------------------
UPLOAD_DIR = "uploads"
if not os.path.exists(UPLOAD_DIR):
    os.makedirs(UPLOAD_DIR)

# -------------------- PAGE SWITCH --------------------
page = st.sidebar.radio("Menu", ["Post Property", "Browse Properties"])

# ==================== POST PAGE ====================
if page == "Post Property":
    st.header("Post Property")

    owner = st.text_input("Owner Name")
    location = st.text_input("Location")
    price = st.text_input("Price")
    details = st.text_area("Details")
    images = st.file_uploader("Upload Images", accept_multiple_files=True)

    if st.button("Submit"):
        if owner and location and price:
            image_paths = []

            if images:
                for img in images:
                    ext = img.name.split(".")[-1]
                    filename = f"{uuid.uuid4()}.{ext}"
                    filepath = os.path.join(UPLOAD_DIR, filename)

                    # Save image correctly
                    with open(filepath, "wb") as f:
                        f.write(img.getbuffer())

                    image_paths.append(filepath)

            c.execute(
                "INSERT INTO properties (owner, location, price, details, images) VALUES (?, ?, ?, ?, ?)",
                (owner, location, price, details, ",".join(image_paths))
            )
            conn.commit()

            st.success("Property added successfully")
            st.rerun()
        else:
            st.warning("Please fill required fields")

# ==================== BROWSE PAGE ====================
elif page == "Browse Properties":
    st.header("Browse Properties")

    c.execute("SELECT * FROM properties ORDER BY id DESC")
    data = c.fetchall()

    if not data:
        st.info("No properties added yet")

    for prop in data:
        st.markdown('<div class="card">', unsafe_allow_html=True)

        st.subheader(prop[2])
        st.write(f"Owner: {prop[1]}")
        st.write(f"Price: {prop[3]}")
        st.write(prop[4])

        # FIX: Correct image display
        if prop[5]:
            image_list = prop[5].split(",")

            for img_path in image_list:
                if os.path.exists(img_path):
                    st.image(img_path, use_column_width=True)
                else:
                    st.warning(f"Image not found: {img_path}")

        whatsapp_url = f"https://wa.me/918590304889?text=Interested in property at {prop[2]}"
        st.markdown(f"[Contact on WhatsApp]({whatsapp_url})")

        st.markdown("</div>", unsafe_allow_html=True)
