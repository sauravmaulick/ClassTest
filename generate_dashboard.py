import json

# Read questions from questions.json
with open('questions.json', 'r') as q_file:
    questions_data = json.load(q_file)
    questions = questions_data["Chapter 1, 2, 12"]

# Read student responses from ddd_20250712_062854_responses.json
with open('ddd_20250712_062854_responses.json', 'r') as r_file:
    responses_data = json.load(r_file)
    responses = responses_data["responses"]

# Initialize dashboard report
dashboard = {
    "student_name": responses_data["student_name"],
    "timestamp": responses_data["timestamp"],
    "total_questions": len(questions),
    "correct_answers": 0,
    "incorrect_answers": 0,
    "questions": []
}

# Compare each question with the corresponding response
for question, response in zip(questions, responses):
    question_text = question["question"]
    correct_answer = question["answer"]
    given_answer = response["answer_given"]
    is_correct = given_answer == correct_answer

    # Update counts
    if is_correct:
        dashboard["correct_answers"] += 1
    else:
        dashboard["incorrect_answers"] += 1

    # Add question details to the report
    dashboard["questions"].append({
        "question": question_text,
        "type": question["type"],
        "correct_answer": correct_answer,
        "given_answer": given_answer,
        "status": "Correct" if is_correct else "Incorrect"
    })

# Calculate percentage
dashboard["percentage"] = (dashboard["correct_answers"] / dashboard["total_questions"]) * 100

# Write the dashboard report to a JSON file
with open('dashboard_report.json', 'w') as d_file:
    json.dump(dashboard, d_file, indent=4)

# Print the dashboard report
print(f"Student Name: {dashboard['student_name']}")
print(f"Timestamp: {dashboard['timestamp']}")
print(f"Total Questions: {dashboard['total_questions']}")
print(f"Correct Answers: {dashboard['correct_answers']}")
print(f"Incorrect Answers: {dashboard['incorrect_answers']}")
print(f"Percentage: {dashboard['percentage']:.2f}%")
print("\nDetailed Report:")
for q in dashboard["questions"]:
    print(f"Question: {q['question']}")
    print(f"Type: {q['type']}")
    print(f"Correct Answer: {q['correct_answer']}")
    print(f"Given Answer: {q['given_answer']}")
    print(f"Status: {q['status']}")
    print("-" * 50)