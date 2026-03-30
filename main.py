# -*- coding: utf-8 -*-
import streamlit as st
import sqlite3
import os

# -------------------- CONFIG --------------------
st.set_page_config(page_title="NSSI Land", layout="centered")
# -------------------- BACKGROUND IMAGE --------------------
page_bg_img = """
<style>
[data-testid="stAppViewContainer"] {
    background-image: url("https://images.unsplash.com/photo-1600585154340-be6161a56a0c");
    background-size: cover;
    background-position: center;
    background-repeat: no-repeat;
    background-attachment: fixed;
}

/* Make content readable */
[data-testid="stHeader"], [data-testid="stToolbar"] {
    background: rgba(0,0,0,0);
}

.main {
    background-color: rgba(255, 255, 255, 0.85);
    padding: 20px;
    border-radius: 10px;
}
</style>
"""

st.markdown(page_bg_img, unsafe_allow_html=True)


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
    image TEXT
)
""")

c.execute("""
CREATE TABLE IF NOT EXISTS leads (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    phone TEXT
)
""")

conn.commit()

# -------------------- TITLE --------------------
st.title("🏡 NSSI Land Promoters - Calicut")

# Create uploads folder
if not os.path.exists("uploads"):
    os.makedirs("uploads")

# -------------------- POST PROPERTY --------------------
st.header("📢 Post Property")

owner = st.text_input("Owner Name")
location = st.text_input("Location")
price = st.text_input("Price")
details = st.text_area("Details")
image = st.file_uploader("Upload Image", type=["jpg", "png", "jpeg"])

if st.button("Submit Property"):
    if owner and location and price:
        image_path = ""

        if image:
            image_path = f"uploads/{image.name}"
            with open(image_path, "wb") as f:
                f.write(image.getbuffer())

        c.execute("INSERT INTO properties (owner, location, price, details, image) VALUES (?, ?, ?, ?, ?)",
                  (owner, location, price, details, image_path))
        conn.commit()

        st.success("Property Saved ✅")
        st.rerun()
    else:
        st.warning("Fill required fields")

st.divider()

# -------------------- SEARCH --------------------
st.header("🔍 Search Property")
search = st.text_input("Search by location")

# -------------------- SHOW PROPERTIES --------------------
st.header("🏘️ Available Properties")

if search:
    c.execute("SELECT * FROM properties WHERE location LIKE ?", ('%' + search + '%',))
else:
    c.execute("SELECT * FROM properties")

data = c.fetchall()

for prop in data:
    st.subheader(f"📍 {prop[2]}")
    st.write(f"👤 Owner: {prop[1]}")
    st.write(f"💰 Price: ₹{prop[3]}")
    st.write(f"📝 {prop[4]}")

    if prop[5]:
        st.image(prop[5], use_column_width=True)

    # WhatsApp button
    whatsapp_url = f"https://wa.me/918590304889?text=Hi, I'm interested in property at {prop[2]}"
    st.markdown(f"[📲 Enquire on WhatsApp]({whatsapp_url})")

    st.divider()

# -------------------- LEADS --------------------
st.header("📞 Get Buyer Leads")

name = st.text_input("Your Name")
phone = st.text_input("Phone")

if st.button("Save Lead"):
    if name and phone:
        c.execute("INSERT INTO leads (name, phone) VALUES (?, ?)", (name, phone))
        conn.commit()
        st.success("Lead Saved ✅")
    else:
        st.warning("Fill all fields")

# -------------------- VIEW LEADS --------------------
with st.expander("📋 View Leads"):
    c.execute("SELECT * FROM leads")
    leads = c.fetchall()
    for lead in leads:
        st.write(f"{lead[1]} - {lead[2]}")
