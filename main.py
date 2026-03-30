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

# ================= SESSION =================
if "favorites" not in st.session_state:
    st.session_state["favorites"] = []

# ================= FOLDER =================
UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

# ================= STYLE =================
st.markdown("""
<style>
[data-testid="stAppViewContainer"] {
    background: linear-gradient(135deg, #0f2027, #203a43, #2c5364);
}
h1,h2,h3,h4,h5,h6,p,label {
    color:white !important;
}
.card {
    background: rgba(255,255,255,0.05);
    padding:15px;
    border-radius:15px;
    margin-bottom:15px;
}
.title {font-weight:bold;}
.price {color:#00ffcc;}
.location {color:#ccc;}
.stButton>button {
    background:#0072ff;
    color:white;
}
[data-testid="stSidebar"] {
    background:#111;
}
[data-testid="stSidebar"] * {
    color:white !important;
}
</style>
""", unsafe_allow_html=True)

# ================= HEADER =================
st.markdown("<h1 style='text-align:center;'>NSSI Land - Calicut</h1>", unsafe_allow_html=True)

# ================= MENU =================
menu = st.sidebar.radio("Menu", ["Browse", "Post Property", "Saved", "Admin"])

# ================= POST =================
if menu == "Post Property":

    st.markdown("<h2>Post Property</h2>", unsafe_allow_html=True)

    title = st.text_input("Title")
    price = st.text_input("Price")
    location = st.text_input("Location")
    details = st.text_area("Details")

    images = st.file_uploader("Upload Images", accept_multiple_files=True)
    video = st.file_uploader("Upload Video", type=["mp4"])

    if st.button("Submit"):

        image_paths = []

        if images:
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
        """, (
            title, price, location, details,
            ",".join(image_paths), video_path, str(time.time())
        ))

        conn.commit()
        st.success("Posted Successfully")
        st.rerun()

# ================= BROWSE =================
elif menu == "Browse":

    st.markdown("<h2>Browse Properties</h2>", unsafe_allow_html=True)

    c.execute("SELECT * FROM properties ORDER BY id DESC")
    data = c.fetchall()

    cols = st.columns(2)

    for i, prop in enumerate(data):
        with cols[i % 2]:

            st.markdown('<div class="card">', unsafe_allow_html=True)

            images = prop[5].split(",") if prop[5] else []
            video = prop[6]

            tab1, tab2, tab3 = st.tabs(["Images", "Video", "Details"])

            with tab1:
                for img in images:
                    if os.path.exists(img):
                        st.image(img, use_container_width=True)

            with tab2:
                if video and os.path.exists(video):
                    st.video(video)

            with tab3:
                st.markdown(f"<div class='title'>{prop[1]}</div>", unsafe_allow_html=True)
                st.markdown(f"<div class='price'>₹ {prop[2]}</div>", unsafe_allow_html=True)
                st.markdown(f"<div class='location'>{prop[3]}</div>", unsafe_allow_html=True)
                st.write(prop[4])

                if st.button("❤️ Save", key=f"s{prop[0]}"):
                    st.session_state["favorites"].append(prop[0])

                share = f"{prop[1]} ₹{prop[2]} {prop[3]}"
                link = "https://wa.me/?text=" + share.replace(" ", "%20")
                st.markdown(f"[📤 WhatsApp]({link})")

            st.markdown('</div>', unsafe_allow_html=True)

# ================= SAVED =================
elif menu == "Saved":

    st.markdown("<h2>Saved Properties</h2>", unsafe_allow_html=True)

    c.execute("SELECT * FROM properties")
    data = c.fetchall()

    for prop in data:
        if prop[0] in st.session_state["favorites"]:
            st.write(f"{prop[1]} - ₹{prop[2]} - {prop[3]}")

# ================= ADMIN =================
elif menu == "Admin":

    st.markdown("<h2>Admin Panel</h2>", unsafe_allow_html=True)

    password = st.text_input("Enter Password", type="password")

    if password == "admin123":

        st.success("Login Success")

        c.execute("SELECT * FROM properties ORDER BY id DESC")
        data = c.fetchall()

        for prop in data:

            st.markdown(f"""
            <div class="card">
            <b>{prop[1]}</b><br>
            ₹ {prop[2]}<br>
            {prop[3]}
            </div>
            """, unsafe_allow_html=True)

            if st.button("Delete", key=f"d{prop[0]}"):

                # delete db
                c.execute("DELETE FROM properties WHERE id=?", (prop[0],))
                conn.commit()

                # delete files
                if prop[5]:
                    for img in prop[5].split(","):
                        if os.path.exists(img):
                            os.remove(img)

                if prop[6] and os.path.exists(prop[6]):
                    os.remove(prop[6])

                st.success("Deleted")
                st.rerun()

    else:
        st.warning("Wrong password")
