# Interview Testing Chatbot

## Overview

This repository contains a Streamlit-based application designed for interview testing. The application utilizes a chatbot named **Jamie** to interact with users and evaluate their responses based on their uploaded CVs. The bot helps assess candidates for different roles, such as Data Scientist and Python Developer, by asking relevant questions and scoring their answers based on similarity to correct responses.

## Features

- **File Upload**: Users can upload their CVs in PDF or DOCX format.
- **Interview Simulation**: Depending on the predicted job role, the chatbot asks relevant questions.
- **Response Evaluation**: The bot evaluates user responses and provides a similarity score.
- **Data Export**: Interview scores and details are saved to an Excel file.
- **Chat History**: Keeps track of the conversation and allows users to interact with the chatbot.

## Installation

1. **Clone the Repository**:
    ```bash
    git clone https://github.com/your-username/interview-testing-chatbot.git
    cd interview-testing-chatbot
    ```

2. **Install Dependencies**:
    It is recommended to create a virtual environment before installing the dependencies.
    ```bash
    pip install -r requirements.txt
    ```

3. **Create `requirements.txt`**:
    Create a `requirements.txt` file with the following content:
    ```text
    pandas
    numpy
    streamlit
    PyPDF2
    python-docx
    langchain_community
    ```

## Usage

1. **Run the Application**:
    ```bash
    streamlit run app.py
    ```

2. **Interact with the Chatbot**:
    - Upload your CV (PDF or DOCX format) via the sidebar.
    - The chatbot will process your CV and ask questions based on the predicted job role.
    - Provide answers to the questions, and the bot will evaluate your responses.
    - Your interview score and details will be saved to `result_HR.xlsx`.

## Code Overview

- **Preprocessing Functions**: Functions for cleaning and tokenizing text, and extracting features from resumes.
- **`ChatBot` Function**: Manages the conversation, processes user input, and evaluates responses.
- **`show_data` & `details_interview` Functions**: Handle the data aggregation and export it to an Excel file.
- **Streamlit App**: Provides the user interface for uploading CVs and interacting with the chatbot.

## Contributing

Feel free to submit pull requests or issues. Contributions to improve the chatbot's functionality or enhance the user experience are welcome.

## Contact

For any inquiries, please contact [your-email@example.com](mahmoudibrahimabdelfattah48@gmail.com).

