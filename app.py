import streamlit as st
import os
from PIL import Image
from utils import utils
from lyzr import Summarizer
from dotenv import load_dotenv
from lyzr_qa import question_generation

load_dotenv()
api = os.getenv("OPENAI_API_KEY")
utils.page_config()
summarizer = Summarizer(api_key=api)

data = "data"
os.makedirs(data, exist_ok=True)

image = Image.open("./logo/lyzr-logo.png")
st.image(image, width=150)
st.title('Lyzr Chapter Notes Generator📚')
st.markdown('Welcome to the lyzr Chapter Notes Generator, this app will help you to generate Summaries from given file !!!')

@st.cache_resource(show_spinner=False)
def rag_default():
    with st.spinner("Generating Embeddings..."):
        path = './lech201.pdf'
        agent = question_generation(path)
    return agent


@st.cache_resource(show_spinner=False)
def rag_upload(path):
    with st.spinner("Generating Embeddings..."):
        agent = question_generation(path)
    return agent


@st.cache_resource(show_spinner=False)
def rag_def_question(_agent):
    with st.spinner("Generating Questions..."):
        response = _agent.query("Generate 5 Questions")
    return response.response


def rag_response(question,agent):
    response = agent.query(question)
    return response.response


def gpt_summary(response):
    style = "Summary with bullet points and subheading font is bold"
    summary = summarizer.summarize(response, style=style)
    return summary

def rag_notes(agent,user_topic):
    metric = f""" You are an expert of this {user_topic}. Tell me everything you know about this {user_topic}, Provide a detailed reponse on this {user_topic} from the given file"""
    with st.spinner("Generating Notes..."):
        rag_generated_response = rag_response(question=metric,
                                              agent=agent)  # getting reponse from rag about the subject/topic
        gpt_response = gpt_summary(response=rag_generated_response)
    return gpt_response

def default():
    st.info('Default file: Haloalkanes and Haloarenes')
    agent = rag_default()
    def_question = rag_def_question(agent)
    st.markdown("### Questions:")
    st.markdown(def_question)
    user_topic = st.text_input('Enter the topic according to subject')
    if user_topic is not None:
        if st.button('Submit'):
            gpt_response=rag_notes(agent,user_topic) # create n number of question on rag response
            st.subheader('Notes')
            st.write(gpt_response)


def upload():
    file = st.file_uploader("Upload a Subject Book Pdf", type=["pdf"])
    if file:
        utils.save_uploaded_file(file, directory_name=data)
        path = utils.get_files_in_directory(directory=data)
        filepath = path[0]
        agent = rag_upload(filepath)
        def_question = rag_def_question(agent)
        st.markdown("### Questions:")
        st.markdown(def_question)
        user_topic = st.text_input('Enter the topic according to subject')
        if user_topic is not None:
            if st.button('Submit'):
                gpt_response = rag_notes(agent, user_topic)  # create n number of question on rag response
                st.subheader('Summary')
                st.write(gpt_response)
    else:
        st.warning('Please Upload subject pdf file!!!')


def main(): 
    image = Image.open("./logo/lyzr-logo.png")
    st.sidebar.image(image, width=150)
    st.sidebar.subheader('Lyzr Chapter Notes Generator')

    # session state for default button
    if 'default_button' not in st.session_state:
        st.session_state.default_button = False


    # session state for upload button
    if 'upload_button' not in st.session_state:
        st.session_state.upload_button = False


    def default_button():
        st.session_state.default_button = True
        st.session_state.upload_button = False
        st.session_state.show_questions = True

    def upload_button():
        st.session_state.upload_button = True
        st.session_state.default_button = False


    st.sidebar.button('Default File', on_click=default_button)
    st.sidebar.button('Upload File', on_click=upload_button)


    if st.session_state.default_button:
        default()

    if st.session_state.upload_button:
        upload()
        
        

if __name__ == "__main__":
    utils.style_app()
    main()
    utils.template_end()
