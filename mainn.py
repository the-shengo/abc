import streamlit as st
import os

PAGES_DIR = "pages"
os.makedirs(PAGES_DIR, exist_ok=True)

st.title("📚 Simple Community Pages")

# Load pages
pages = sorted(os.listdir(PAGES_DIR))

menu = ["Home", "Create Page"] + pages
choice = st.sidebar.selectbox("Menu", menu)

# ---------------- HOME ----------------
if choice == "Home":
    st.write("Welcome! Select a page from the menu or create a new one.")

# ---------------- CREATE ----------------
elif choice == "Create Page":
    title = st.text_input("Page title")
    content = st.text_area("Page content")

    if st.button("Save Page") and title:
        with open(os.path.join(PAGES_DIR, title + ".txt"), "w") as f:
            f.write(content)
        st.success("Page created!")

# ---------------- VIEW / EDIT ----------------
else:
    page_path = os.path.join(PAGES_DIR, choice)

    with open(page_path, "r") as f:
        content = f.read()

    st.subheader(choice.replace(".txt", ""))
    new_content = st.text_area("Edit page", content, height=300)

    if st.button("Save Changes"):
        with open(page_path, "w") as f:
            f.write(new_content)
        st.success("Page updated!")
