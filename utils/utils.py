import os
import shutil
import streamlit as st
from dotenv import load_dotenv; load_dotenv()

def remove_existing_files(directory):
    for filename in os.listdir(directory):
        file_path = os.path.join(directory, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            st.error(f"Error while removing existing files: {e}")


def get_files_in_directory(directory):
    # This function help us to get the file path along with filename.
    files_list = []

    if os.path.exists(directory) and os.path.isdir(directory):
        for filename in os.listdir(directory):
            file_path = os.path.join(directory, filename)
            
            if os.path.isfile(file_path):
                files_list.append(file_path)

    return files_list

def save_uploaded_file(uploaded_file, directory_name):
    # Function to save uploaded file
    remove_existing_files(directory_name)

    file_path = os.path.join(directory_name, uploaded_file.name)
    with open(file_path, "wb") as file:
        file.write(uploaded_file.read())
    st.success("File uploaded successfully")


def style_app():
    # You can put your CSS styles here
    st.markdown("""
    <style>
    .app-header { visibility: hidden; }
    .css-18e3th9 { padding-top: 0; padding-bottom: 0; }
    .css-1d391kg { padding-top: 1rem; padding-right: 1rem; padding-bottom: 1rem; padding-left: 1rem; }
    [data-testid="stSidebar"][aria-expanded="true"]{
           min-width: 450px;
           max-width: 450px;
       }
    </style>
    """, unsafe_allow_html=True)

def page_config(layout = "centered"):
    st.set_page_config(
        page_title="Lyzr Chapter Notes Generator",
        layout=layout,  # or "wide" 
        initial_sidebar_state="auto",
        page_icon="./logo/lyzr-logo-cut.png"
    )

def template_end():
    with st.sidebar.expander("ℹ️ - About this App"):
        st.sidebar.markdown("This app uses Lyzr's PDF QABot and summarizer to generate summaries from file")
        st.sidebar.link_button("Lyzr", url='https://www.lyzr.ai/', use_container_width = True)
        st.sidebar.link_button("Book a Demo", url='https://www.lyzr.ai/book-demo/', use_container_width = True)
        st.sidebar.link_button("Discord", url='https://discord.gg/nm7zSyEFA2', use_container_width = True)
        st.sidebar.link_button("Slack", url='https://join.slack.com/t/genaiforenterprise/shared_invite/zt-2a7fr38f7-_QDOY1W1WSlSiYNAEncLGw', use_container_width = True)