import streamlit as st
import sqlite3
import os
import shutil
import base64

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
    video TEXT
)
""")

# ================= FAVORITES =================
if "favorites" not in st.session_state:
    st.session_state["favorites"] = []

# ================= STYLE =================
st.markdown("""
<style>
body {background-color:#0e1117;}
h1,h2,h3,h4,h5,h6,p,span,label {color:white !important;}
</style>
""", unsafe_allow_html=True)

# ================= HEADER =================
st.title("NSSI Land - Buy & Sell Properties")

# ================= ADD PROPERTY =================
st.header("Post Property")

title = st.text_input("Title")
price = st.text_input("Price")
location = st.text_input("Location")
details = st.text_area("Details")

images = st.file_uploader("Upload Images", accept_multiple_files=True)
video = st.file_uploader("Upload Video", type=["mp4"])

if st.button("Submit Property"):
    image_paths = []
    os.makedirs("uploads", exist_ok=True)

    for img in images:
        path = os.path.join("uploads", img.name)
        with open(path, "wb") as f:
            f.write(img.getbuffer())
        image_paths.append(path)

    video_path = ""
    if video:
        video_path = os.path.join("uploads", video.name)
        with open(video_path, "wb") as f:
            f.write(video.getbuffer())

    c.execute("INSERT INTO properties (title, price, location, details, images, video) VALUES (?,?,?,?,?,?)",
              (title, price, location, details, ",".join(image_paths), video_path))
    conn.commit()

    st.success("Property Added Successfully")
    st.rerun()

# ================= BROWSE =================
st.header("Browse Properties")

c.execute("SELECT * FROM properties ORDER BY id DESC")
data = c.fetchall()

for prop in data:
    st.markdown("---")
    col1, col2 = st.columns([1,2])

    # LEFT SIDE MEDIA
    with col1:
        # IMAGE SLIDER
        if prop[5]:
            imgs = prop[5].split(",")

            key = f"slider_{prop[0]}"
            if key not in st.session_state:
                st.session_state[key] = 0

            idx = st.session_state[key]

            if os.path.exists(imgs[idx]):
                st.image(imgs[idx], use_container_width=True)

            c1, c2 = st.columns(2)
            with c1:
                if st.button("Prev", key=f"p{prop[0]}"):
                    st.session_state[key] = (idx-1) % len(imgs)
                    st.rerun()
            with c2:
                if st.button("Next", key=f"n{prop[0]}"):
                    st.session_state[key] = (idx+1) % len(imgs)
                    st.rerun()

        # VIDEO
        if prop[6]:
            if os.path.exists(prop[6]):
                st.video(prop[6])

    # RIGHT SIDE DETAILS
    with col2:
        st.subheader(prop[1])
        st.write("Price:", prop[2])
        st.write("Location:", prop[3])
        st.write(prop[4])

        # ❤️ FAVORITE
        fav_key = f"fav_{prop[0]}"
        if st.button("❤️ Save", key=fav_key):
            if prop[0] not in st.session_state["favorites"]:
                st.session_state["favorites"].append(prop[0])
                st.success("Saved to Favorites")

        # 📤 WHATSAPP SHARE
        share_text = f"""Check this property:
{prop[1]}
Price: {prop[2]}
Location: {prop[3]}
"""

        share_link = f"https://wa.me/?text={share_text.replace(' ', '%20')}"
        st.markdown(f"[Share on WhatsApp]({share_link})")

# ================= FAVORITES SECTION =================
st.header("Saved Properties ❤️")

for prop in data:
    if prop[0] in st.session_state["favorites"]:
        st.markdown(f"✔ {prop[1]} - {prop[2]} - {prop[3]}")

