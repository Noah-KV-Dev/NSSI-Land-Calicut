import streamlit as st
import sqlite3
import os
import time

st.set_page_config(layout="wide")

# ---------- DATABASE ----------
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

# ---------- FOLDERS ----------
if not os.path.exists("uploads"):
    os.makedirs("uploads")

# ---------- STYLES ----------
st.markdown("""
<style>
body {
    color: white;
}

[data-testid="stAppViewContainer"] {
    background-image: url("https://images.unsplash.com/photo-1600585154340-be6161a56a0c");
    background-size: cover;
    background-position: center;
}

section[data-testid="stSidebar"] {
    background-color: #111;
    color: white;
}

/* CARD STYLE */
.card {
    background: rgba(0,0,0,0.7);
    padding: 10px;
    border-radius: 10px;
    margin-bottom: 15px;
}

.card img, .card video {
    width: 100%;
    border-radius: 8px;
}

.title {
    font-size: 18px;
    font-weight: bold;
}

.highlight {
    color: #00ffcc;
    font-weight: bold;
}
</style>
""", unsafe_allow_html=True)

# ---------- MENU ----------
menu = st.sidebar.radio("Menu", ["Browse", "Post Property", "Saved"])

# ---------- POST PROPERTY ----------
if menu == "Post Property":

    st.markdown("<h3 style='color:black;'>Post Property</h3>", unsafe_allow_html=True)

    title = st.text_input("Title")
    price = st.text_input("Price")
    location = st.text_input("Location")
    details = st.text_area("Details")

    images = st.file_uploader("Upload Images", accept_multiple_files=True)
    video = st.file_uploader("Upload Video")

    if st.button("Submit"):

        image_paths = []

        if images:
            for img in images:
                path = f"uploads/{time.time()}_{img.name}"
                with open(path, "wb") as f:
                    f.write(img.getbuffer())
                image_paths.append(path)

        video_path = ""
        if video:
            video_path = f"uploads/{time.time()}_{video.name}"
            with open(video_path, "wb") as f:
                f.write(video.getbuffer())

        c.execute("""
        INSERT INTO properties (title, price, location, details, images, video, created_at)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            title,
            price,
            location,
            details,
            ",".join(image_paths),
            video_path,
            str(time.time())
        ))

        conn.commit()
        st.success("Property Posted Successfully!")

# ---------- BROWSE ----------
elif menu == "Browse":

    st.title("Browse Properties")

    c.execute("SELECT * FROM properties ORDER BY created_at DESC")
    data = c.fetchall()

    # 2x2 grid (mobile friendly)
    cols = st.columns(2)

    for i, row in enumerate(data):
        col = cols[i % 2]

        with col:
            st.markdown('<div class="card">', unsafe_allow_html=True)

            images = row[5].split(",") if row[5] else []
            video = row[6]

            # IMAGE
            if images and os.path.exists(images[0]):
                st.image(images[0])

            # VIDEO
            if video and os.path.exists(video):
                st.video(video)

            st.markdown(f"<div class='title'>{row[1]}</div>", unsafe_allow_html=True)
            st.markdown(f"<div class='highlight'>₹ {row[2]}</div>", unsafe_allow_html=True)
            st.write(row[3])
            st.write(row[4])

            # WHATSAPP SHARE
            msg = f"{row[1]} | ₹{row[2]} | {row[3]}"
            wa_link = f"https://wa.me/?text={msg}"
            st.markdown(f"[📤 Share WhatsApp]({wa_link})")

            # SAVE BUTTON
            if st.button("❤️ Save", key=f"save_{row[0]}"):
                st.success("Saved!")

            st.markdown('</div>', unsafe_allow_html=True)

# ---------- SAVED ----------
elif menu == "Saved":
    st.title("Saved Properties (Coming Soon)")
