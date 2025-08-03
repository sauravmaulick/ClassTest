import streamlit as st
import json
import pandas as pd

# Set Streamlit page configuration
st.set_page_config(page_title="ICSC Robotics and AI Dashboard", layout="wide")

# Title of the app
st.title("ICSC Robotics and AI Exam Dashboard")

# Read questions from questions.json
try:
    with open('questions.json', 'r') as q_file:
        questions_data = json.load(q_file)
        questions = questions_data["Chapter 1, 2, 12"]
except FileNotFoundError:
    st.error("Error: questions.json file not found!")
    st.stop()

# Read student responses from Yash_20250713_072223_responses.json
try:
    with open('Yash_20250713_072223_responses.json', 'r') as r_file:
        responses_data = json.load(r_file)
        responses = responses_data["responses"]
except FileNotFoundError:
    st.error("Error: Yash_20250713_072223_responses.json file not found!")
    st.stop()

# Initialize lists for the dashboard
dashboard_data = []
correct_count = 0
total_questions = len(questions)

# Compare each question with the corresponding response
for question, response in zip(questions, responses):
    question_text = question["question"]
    q_type = question["type"]
    correct_answer = question["answer"]
    given_answer = response["answer_given"]
    is_correct = given_answer == correct_answer

    # Update correct count
    if is_correct:
        correct_count += 1

    # Append to dashboard data
    dashboard_data.append({
        "Question": question_text,
        "Type": q_type,
        "Correct Answer": correct_answer,
        "Given Answer": given_answer,
        "Status": "Correct" if is_correct else "Incorrect"
    })

# Calculate percentage
percentage = (correct_count / total_questions) * 100

# Display summary
st.header("Summary")
st.write(f"**Student Name:** {responses_data['student_name']}")
st.write(f"**Timestamp:** {responses_data['timestamp']}")
st.write(f"**Total Questions:** {total_questions}")
st.write(f"**Correct Answers:** {correct_count}")
st.write(f"**Incorrect Answers:** {total_questions - correct_count}")
st.write(f"**Percentage:** {percentage:.2f}%")

# Create DataFrame for tabular display
df = pd.DataFrame(dashboard_data)

# Display detailed report in a table
st.header("Detailed Report")
st.dataframe(
    df,
    column_config={
        "Question": st.column_config.TextColumn("Question", width="large"),
        "Type": st.column_config.TextColumn("Type", width="medium"),
        "Correct Answer": st.column_config.TextColumn("Correct Answer", width="medium"),
        "Given Answer": st.column_config.TextColumn("Given Answer", width="medium"),
        "Status": st.column_config.TextColumn("Status", width="medium")
    },
    use_container_width=True,
    height=600
)

# Save the dashboard data to a JSON file
dashboard = {
    "student_name": responses_data["student_name"],
    "timestamp": responses_data["timestamp"],
    "total_questions": total_questions,
    "correct_answers": correct_count,
    "incorrect_answers": total_questions - correct_count,
    "percentage": percentage,
    "questions": dashboard_data
}
with open('dashboard_report.json', 'w') as d_file:
    json.dump(dashboard, d_file, indent=4)