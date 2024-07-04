from dotenv import load_dotenv
load_dotenv()  # Load environment variables

import streamlit as st
import sqlite3
import google.generativeai as genai
import os


def configure_api_key():
    """
    Configures the Google GenerativeAI API using the environment variable.
    """
    genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))


def get_gemini_response(question, prompt):
    """
    Gets a response from the Gemini model for converting a question to SQL.

    Args:
        question: The user's question in natural language.
        prompt: The prompt guiding the model (defined elsewhere).

    Returns:
        The generated SQL query as a string.
    """
    model = genai.GenerativeModel('gemini-pro')
    response = model.generate_content([prompt[0], question])  # Assuming prompt is a list
    return response.text


def read_sql_query(sql, db):
    """
    Reads data from the SQLite database using the provided SQL query.

    Args:
        sql: The generated SQL query.
        db: The database name (e.g., "student.db").

    Returns:
        A list of rows retrieved from the database.
    """
    conn = sqlite3.connect(db)
    cur = conn.cursor()
    cur.execute(sql)
    rows = cur.fetchall()
    conn.commit()
    conn.close()
    return rows


def define_prompt():
    """
    Defines the prompt for the generative model (consider moving this outside).

    Returns:
        A list containing the prompt text.
    """
    prompt = [
        """
        You are an expert in converting English questions to SQL query!
        The SQL database has the name STUDENT and has the following columns - NAME, CLASS, SECTION and MARKS \n\nFor example, \nExample 1 How many entries of records are present?,
        the SQL command will be something like this SELECT COUNT(*) FROM STUDENT;
        \nExample 2 Tell me all the students studying in Data Science class?,
        the SQL command will be something like this SELECT * FROM STUDENT where CLASS="Data Science";
        also the sql code should not have ``` in beginning or end and sql word in 
        """
    ]
    return prompt


def run_chatbot():
    """
    Handles user interaction for the text-to-SQL chatbot.
    """
    configure_api_key()  # Ensure API key is configured
    prompt = define_prompt()  # Define the prompt (optional to move outside)

    st.subheader("Chatbot To Retrieve SQL Data")
    question = st.text_input("Ask your question about the database:", key="question")
    submit = st.button("Convert to SQL")

    if submit:
        generated_sql = get_gemini_response(question, prompt)
        st.write("Generated SQL Query:")
        st.code(generated_sql)

        try:
            data = read_sql_query(generated_sql, "student.db")
            if data:
                st.write("Retrieved Data:")
                st.dataframe(data)
            else:
                st.write("No data found for the given query.")
        except sqlite3.Error as e:
            st.error(f"Error connecting to database: {e}")


if __name__ == "__main__":
    run_chatbot()  # Run the chatbot if llm.py is executed directly (for testing)
