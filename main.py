# -*- coding: utf-8 -*-
import streamlit as st
import sqlite3
import os

# -------------------- CONFIG --------------------
st.set_page_config(page_title="NSSI Land", layout="centered")

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

# -------------------- ADMIN LOGIN --------------------
ADMIN_USER = "admin"
ADMIN_PASS = "1234"

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    st.title("🔐 Admin Login")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        if username == ADMIN_USER and password == ADMIN_PASS:
            st.session_state.logged_in = True
            st.success("Login Successful ✅")
            st.rerun()
        else:
            st.error("Invalid Login ❌")

    st.stop()

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

    col1, col2 = st.columns(2)

    # DELETE
    with col1:
        if st.button(f"❌ Delete {prop[0]}"):
            c.execute("DELETE FROM properties WHERE id=?", (prop[0],))
            conn.commit()
            st.warning("Deleted!")
            st.rerun()

    # EDIT
    with col2:
        if st.button(f"✏️ Edit {prop[0]}"):
            st.session_state.edit_id = prop[0]

    st.divider()

# -------------------- EDIT PROPERTY --------------------
if "edit_id" in st.session_state:
    st.header("✏️ Edit Property")

    prop_id = st.session_state.edit_id
    c.execute("SELECT * FROM properties WHERE id=?", (prop_id,))
    prop = c.fetchone()

    new_owner = st.text_input("Owner", value=prop[1])
    new_location = st.text_input("Location", value=prop[2])
    new_price = st.text_input("Price", value=prop[3])
    new_details = st.text_area("Details", value=prop[4])

    if st.button("Update Property"):
        c.execute("""
        UPDATE properties
        SET owner=?, location=?, price=?, details=?
        WHERE id=?
        """, (new_owner, new_location, new_price, new_details, prop_id))

        conn.commit()
        st.success("Updated ✅")

        del st.session_state.edit_id
        st.rerun()

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
