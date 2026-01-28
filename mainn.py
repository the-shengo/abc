import streamlit as st
import os

PAGES_DIR = "pages"
MEDIA_DIR = "media"

ADMIN_USER = "admin"
ADMIN_PASS = "password123"

os.makedirs(PAGES_DIR, exist_ok=True)
os.makedirs(MEDIA_DIR, exist_ok=True)

# ---------------- SESSION ----------------
if "admin" not in st.session_state:
    st.session_state.admin = False

# ---------------- LOGIN ----------------
with st.sidebar:
    st.title("🔐 Admin Login")
    if not st.session_state.admin:
        user = st.text_input("Username")
        pwd = st.text_input("Password", type="password")
        if st.button("Login"):
            if user == ADMIN_USER and pwd == ADMIN_PASS:
                st.session_state.admin = True
                st.success("Logged in as admin")
            else:
                st.error("Wrong credentials")
    else:
        st.success("Admin mode")
        if st.button("Logout"):
            st.session_state.admin = False

# ---------------- MENU ----------------
st.title("📰 Simple Blog")

pages = sorted(os.listdir(PAGES_DIR))
menu = ["Home"] + pages

if st.session_state.admin:
    menu.insert(1, "Create Page")

choice = st.sidebar.selectbox("Menu", menu)

# ---------------- HOME ----------------
if choice == "Home":
    st.write("Welcome! Select a page from the menu.")

# ---------------- CREATE PAGE (ADMIN) ----------------
elif choice == "Create Page" and st.session_state.admin:
    title = st.text_input("Page title")
    content = st.text_area(
        "Markdown content",
        height=300,
        help="Use **bold**, *italic*, ![img](media/file.png)"
    )

    uploaded = st.file_uploader("Upload media", accept_multiple_files=True)

    if st.button("Save Page") and title:
        with open(os.path.join(PAGES_DIR, title + ".md"), "w") as f:
            f.write(content)

        if uploaded:
            for file in uploaded:
                with open(os.path.join(MEDIA_DIR, file.name), "wb") as f:
                    f.write(file.getbuffer())

        st.success("Page created")

# ---------------- VIEW PAGE ----------------
else:
    page_path = os.path.join(PAGES_DIR, choice)

    with open(page_path, "r") as f:
        content = f.read()

    st.markdown(content, unsafe_allow_html=True)

    # ---------------- EDIT (ADMIN ONLY) ----------------
    if st.session_state.admin:
        st.markdown("---")
        st.subheader("✏️ Edit page")

        new_content = st.text_area("Edit Markdown", content, height=300)

        uploaded = st.file_uploader(
            "Upload media",
            accept_multiple_files=True,
            key="edit_upload"
        )

        col1, col2 = st.columns(2)

        with col1:
            if st.button("Save Changes"):
                with open(page_path, "w") as f:
                    f.write(new_content)

                if uploaded:
                    for file in uploaded:
                        with open(os.path.join(MEDIA_DIR, file.name), "wb") as f:
                            f.write(file.getbuffer())

                st.success("Page updated")

        with col2:
            if st.button("Delete Page"):
                os.remove(page_path)
                st.warning("Page deleted")
