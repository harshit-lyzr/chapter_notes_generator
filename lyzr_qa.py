import os
from lyzr import QABot
from dotenv import load_dotenv; load_dotenv()
from pathlib import Path
import time


os.environ['OPENAI_API_KEY'] = os.getenv('OPENAI_API_KEY')


def question_generation(path):
    unique_index_name = f"IndexName_{int(time.time())}"
    vector_store_params = {"index_name": unique_index_name}
    qa_bot = QABot.pdf_qa(
        input_files=[Path(path)],
        vector_store_params=vector_store_params
    )

    return qa_bot


