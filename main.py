# ================= ADMIN =================
elif menu == "Admin":

    st.markdown("<h2>Admin Panel</h2>", unsafe_allow_html=True)

    password = st.text_input("Enter Admin Password", type="password")

    if password == "admin123":   # 🔐 change this password

        st.success("Access Granted")

        c.execute("SELECT * FROM properties ORDER BY id DESC")
        data = c.fetchall()

        for prop in data:

            st.markdown(f"""
            <div class="card">
            <div class="title">{prop[1]}</div>
            <div class="price">₹ {prop[2]}</div>
            <div class="location">{prop[3]}</div>
            </div>
            """, unsafe_allow_html=True)

            col1, col2 = st.columns([3,1])

            with col1:
                st.write("ID:", prop[0])

            with col2:
                if st.button("Delete", key=f"del{prop[0]}"):

                    # DELETE FROM DB
                    c.execute("DELETE FROM properties WHERE id=?", (prop[0],))
                    conn.commit()

                    # DELETE FILES
                    if prop[5]:
                        for img in prop[5].split(","):
                            if os.path.exists(img):
                                os.remove(img)

                    if prop[6] and os.path.exists(prop[6]):
                        os.remove(prop[6])

                    st.success("Deleted Successfully")
                    st.rerun()

    else:
        st.warning("Enter correct admin password")
