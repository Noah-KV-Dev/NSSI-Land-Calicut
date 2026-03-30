elif menu == "Browse":

    st.markdown("<h2>Browse Properties</h2>", unsafe_allow_html=True)

    c.execute("SELECT * FROM properties ORDER BY id DESC")
    data = c.fetchall()

    # 4 COLUMN GRID
    cols = st.columns(4)

    for i, prop in enumerate(data):
        with cols[i % 4]:

            st.markdown('<div class="card">', unsafe_allow_html=True)

            # ================= SLIDER =================
            media_list = []

            # ADD IMAGES
            if prop[5]:
                media_list.extend(prop[5].split(","))

            # ADD VIDEO
            if prop[6]:
                media_list.append(prop[6])

            # SLIDER STATE
            slider_key = f"slider_{prop[0]}"
            if slider_key not in st.session_state:
                st.session_state[slider_key] = 0

            idx = st.session_state[slider_key]

            if len(media_list) > 0:
                current = media_list[idx]

                # CHECK VIDEO OR IMAGE
                if current.endswith(".mp4"):
                    if os.path.exists(current):
                        st.video(current)
                else:
                    if os.path.exists(current):
                        st.image(current, use_container_width=True)

                # SLIDER BUTTONS
                c1, c2 = st.columns(2)

                with c1:
                    if st.button("◀", key=f"prev_{prop[0]}"):
                        st.session_state[slider_key] = (idx - 1) % len(media_list)
                        st.rerun()

                with c2:
                    if st.button("▶", key=f"next_{prop[0]}"):
                        st.session_state[slider_key] = (idx + 1) % len(media_list)
                        st.rerun()

            # ================= DETAILS =================
            st.markdown(f'<div class="title">{prop[1]}</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="price">₹ {prop[2]}</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="location">{prop[3]}</div>', unsafe_allow_html=True)

            # SAVE
            if st.button("Save", key=f"s{prop[0]}"):
                if prop[0] not in st.session_state["favorites"]:
                    st.session_state["favorites"].append(prop[0])

            # SHARE
            share = f"{prop[1]} | {prop[2]} | {prop[3]}"
            link = "https://wa.me/?text=" + share.replace(" ", "%20")
            st.markdown(f"[Share on WhatsApp]({link})")

            st.markdown('</div>', unsafe_allow_html=True)
