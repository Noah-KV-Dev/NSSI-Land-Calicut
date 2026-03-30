# -*- coding: utf-8 -*-
import streamlit as st
import sqlite3
import os

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

.property-card {
    background: rgba(255,255,255,0.08);
    padding: 15px;
    border-radius: 15px;
    margin-bottom: 15px;
}
</style>
""", unsafe_allow_html=True)

st.title("NSSI Land Promoters - Calicut")

# Create uploads folder
if not os.path.exists("uploads"):
    os.makedirs("uploads")
# -------------------- WHITE TEXT STYLE --------------------
st.markdown("""
<style>

/* All text white */
html, body, [class*="css"] {
    color: white !important;
}

/* Labels & headings */
label, .stMarkdown, .stText, h1, h2, h3, h4, h5, h6 {
    color: white !important;
}

/* Input fields text */
input, textarea {
    color: white !important;
    background-color: rgba(0,0,0,0.4) !important;
}

/* Placeholder text */
::placeholder {
    color: #ddd !important;
}

/* Buttons */
.stButton>button {
    background-color: rgba(0,0,0,0.6);
    color: white !important;
    border: 1px solid white;
}

/* Sidebar (if used) */
[data-testid="stSidebar"] {
    color: white !important;
}

/* Expander */
details {
    color: white !important;
}

</style>
""", unsafe_allow_html=True)

# -------------------- LAYOUT --------------------
left, right = st.columns([1, 2])

# -------------------- ADD PROPERTY --------------------
with left:
    st.header("Post Property")

    owner = st.text_input("Owner Name")
    location = st.text_input("Location")
    price = st.text_input("Price")
    details = st.text_area("Details")
    images = st.file_uploader("Upload Images", accept_multiple_files=True)

    if st.button("Submit"):
        if owner and location and price:
            image_paths = []

            for img in images:
                path = f"uploads/{img.name}"
                with open(path, "wb") as f:
                    f.write(img.getbuffer())
                image_paths.append(path)

            c.execute("INSERT INTO properties (owner, location, price, details, images) VALUES (?, ?, ?, ?, ?)",
                      (owner, location, price, details, ",".join(image_paths)))
            conn.commit()

            st.success("Property added")
            st.rerun()
        else:
            st.warning("Fill required fields")

# -------------------- FILTERS --------------------
with right:
    st.header("Browse Properties")

    colf1, colf2 = st.columns(2)

    with colf1:
        search = st.text_input("Search location")

    with colf2:
        max_price = st.text_input("Max price")

    # Query
    query = "SELECT * FROM properties WHERE 1=1"
    params = []

    if search:
        query += " AND location LIKE ?"
        params.append(f"%{search}%")

    if max_price:
        query += " AND price <= ?"
        params.append(max_price)

    c.execute(query, params)
    data = c.fetchall()

    # -------------------- GRID VIEW --------------------
    cols = st.columns(2)

    for i, prop in enumerate(data):
        with cols[i % 2]:
            st.markdown('<div class="property-card">', unsafe_allow_html=True)

            st.subheader(prop[2])
            st.write(f"Owner: {prop[1]}")
            st.write(f"Price: {prop[3]}")
            st.write(prop[4])

            # Multiple images
            if prop[5]:
                imgs = prop[5].split(",")
                for img in imgs:
                    if os.path.exists(img):
                        st.image(img, use_column_width=True)

            whatsapp_url = f"https://wa.me/918590304889?text=Interested in property at {prop[2]}"
            st.markdown(f"[Contact on WhatsApp]({whatsapp_url})")

            st.markdown("</div>", unsafe_allow_html=True)
