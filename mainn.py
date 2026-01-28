import streamlit as st
import os

PAGES_DIR = "pages"
FILES_DIR = "files"

os.makedirs(PAGES_DIR, exist_ok=True)
os.makedirs(FILES_DIR, exist_ok=True)

st.title("📚 Simple Community Pages")

pages = sorted(os.listdir(PAGES_DIR))
menu = ["Home", "Create Page"] + pages
choice = st.sidebar.selectbox("Menu", menu)

# ---------------- HOME ----------------
if choice == "Home":
    st.write("Select a page or create a new one.")

# ---------------- CREATE PAGE ----------------
elif choice == "Create Page":
    title = st.text_input("Page title")
    content = st.text_area("Page content")

    if st.button("Save Page") and title:
        with open(os.path.join(PAGES_DIR, title + ".txt"), "w") as f:
            f.write(content)
        os.makedirs(os.path.join(FILES_DIR, title), exist_ok=True)
        st.success("Page created!")

# ---------------- VIEW / EDIT PAGE ----------------
else:
    page_name = choice.replace(".txt", "")
    page_path = os.path.join(PAGES_DIR, choice)
    page_files_dir = os.path.join(FILES_DIR, page_name)

    os.makedirs(page_files_dir, exist_ok=True)

    with open(page_path, "r") as f:
        content = f.read()

    st.subheader(page_name)

    new_content = st.text_area("Edit page", content, height=250)

    if st.button("Save Changes"):
        with open(page_path, "w") as f:
            f.write(new_content)
        st.success("Page updated!")

    st.markdown("---")
    st.subheader("📎 Attach files")

    uploaded_files = st.file_uploader(
        "Upload files",
        accept_multiple_files=True
    )

    if uploaded_files:
        for file in uploaded_files:
            with open(os.path.join(page_files_dir, file.name), "wb") as f:
                f.write(file.getbuffer())
        st.success("Files uploaded!")

    st.subheader("📂 Files on this page")

    for filename in os.listdir(page_files_dir):
        with open(os.path.join(page_files_dir, filename), "rb") as f:
            st.download_button(
                label=filename,
                data=f,
                file_name=filename
            )
