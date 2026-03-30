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

# ================= STYLE =================
st.markdown("""
<style>
/* FULL PAGE BACKGROUND */
[data-testid="stAppViewContainer"] {
    background: linear-gradient(rgba(0,0,0,0.6), rgba(0,0,0,0.6)),
    url("https://images.unsplash.com/photo-1600585154340-be6161a56a0c");
    background-size: cover;
    background-position: center;
    background-attachment: fixed;
}

/* TEXT WHITE */
h1,h2,h3,h4,h5,h6,p,span,label {
    color: white !important;
}

/* CARD EFFECT */
.block-container {
    background: rgba(0,0,0,0.5);
    padding: 20px;
    border-radius: 10px;
}

/* BUTTON STYLE */
.stButton>button {
    background-color: #1f77b4;
    color: white;
    border-radius: 8px;
}

/* INPUT FIELDS */
input, textarea {
    background-color: rgba(255,255,255,0.1) !important;
    color: white !important;
}
</style>
""", unsafe_allow_html=True)
st.markdown("""
<style>

/* POST PROPERTY SECTION TEXT BLACK */
section[data-testid="stSidebar"] * {
    color: black !important;
}

/* MAIN FORM AREA (POST PROPERTY) */
div[data-testid="stForm"], 
div[data-testid="stVerticalBlock"] div:has(label:contains("Title")) {
    color: black !important;
}

/* INPUT LABELS BLACK */
label {
    color: black !important;
}

/* INPUT TEXT BLACK */
input, textarea {
    color: black !important;
}

</style>
""", unsafe_allow_html=True)


# ================= HEADER =================
st.title("NSSI Land - Buy & Sell Properties")

# ================= UPLOAD FOLDER =================
UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

# ================= ADD PROPERTY =================
st.header("Post Property")

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

    st.success("Property Added Successfully")
    st.rerun()

# ================= BROWSE =================
st.header("Browse Properties")

c.execute("SELECT * FROM properties ORDER BY id DESC")
properties = c.fetchall()

for prop in properties:
    st.markdown("---")

    col1, col2 = st.columns([1,2])

    # ================= LEFT SIDE (MEDIA) =================
    with col1:
        # IMAGE SLIDER
        if prop[5]:
            image_list = prop[5].split(",")

            slider_key = f"slider_{prop[0]}"
            if slider_key not in st.session_state:
                st.session_state[slider_key] = 0

            idx = st.session_state[slider_key]

            if os.path.exists(image_list[idx]):
                st.image(image_list[idx], use_container_width=True)

            c1, c2 = st.columns(2)

            with c1:
                if st.button("Prev", key=f"prev_{prop[0]}"):
                    st.session_state[slider_key] = (idx - 1) % len(image_list)
                    st.rerun()

            with c2:
                if st.button("Next", key=f"next_{prop[0]}"):
                    st.session_state[slider_key] = (idx + 1) % len(image_list)
                    st.rerun()

        # VIDEO DISPLAY
        if prop[6]:
            if os.path.exists(prop[6]):
                st.video(prop[6])

    # ================= RIGHT SIDE (DETAILS) =================
    with col2:
        st.subheader(prop[1])
        st.write(f"Price: {prop[2]}")
        st.write(f"Location: {prop[3]}")
        st.write(prop[4])

        # FAVORITE BUTTON
        if st.button("Save Property", key=f"fav_{prop[0]}"):
            if prop[0] not in st.session_state["favorites"]:
                st.session_state["favorites"].append(prop[0])
                st.success("Saved")

        # WHATSAPP SHARE
        share_text = f"Check this property:\n{prop[1]}\nPrice: {prop[2]}\nLocation: {prop[3]}"
        share_url = "https://wa.me/?text=" + share_text.replace(" ", "%20")
        st.markdown(f"[Share on WhatsApp]({share_url})")

# ================= FAVORITES =================
st.header("Saved Properties")

for prop in properties:
    if prop[0] in st.session_state["favorites"]:
        st.markdown(f"{prop[1]} | {prop[2]} | {prop[3]}")
