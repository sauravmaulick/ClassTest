import streamlit as st
import json
import os
from datetime import datetime
import io

# Load questions
def load_questions():
    with open("questions.json", "r") as f:
        return json.load(f)

# Save student response
def save_response(student_name, chapter, responses):
    record = {
        "student_name": student_name,
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "chapter": chapter,
        "responses": responses
    }

    if os.path.exists("responses.json"):
        with open("responses.json", "r") as f:
            data = json.load(f)
    else:
        data = []

    data.append(record)

    with open("responses.json", "w") as f:
        json.dump(data, f, indent=4)

# App title
st.title("📚 Class Test App")

# Student info
student_name = st.text_input("Enter your name")
chapter = st.selectbox("Select Chapter", list(load_questions().keys()))

if student_name and chapter:
    st.subheader(f"Chapter: {chapter}")
    questions = load_questions()[chapter]
    responses = []

    for idx, q in enumerate(questions):
        st.markdown(f"**Q{idx + 1}:** {q['question']}")

        if q["type"] == "fill":
            ans = st.text_input(
                    f"Your answer (Q{idx + 1})", 
                    key=f"fill_{idx}"
                )
        elif q["type"] == "true_false":
            ans = st.radio(
                    f"Select (Q{idx + 1})", 
                    ["True", "False"], 
                    index=None,
                    key=f"tf_{idx}"
                )
        elif q["type"] == "mcq":
            ans = st.radio(
                    f"Select (Q{idx + 1})", 
                    q["options"], 
                    index=None,
                    key=f"mcq_{idx}"
                )
        elif q["type"] == "qa":
            ans = st.text_area(
                    f"Write your answer (Q{idx + 1})", 
                    key=f"qa_{idx}"
                )
        else:
            ans = st.text_area(
                    f"Write your answer (Q{idx + 1})", 
                    key=f"qa_{idx}"
            )
            

        responses.append({
            "question": q["question"],
            "type": q["type"],
            "answer_given": ans
        })

    if st.button("Submit"):
        # save_response(student_name, chapter, responses)
        # st.success("✅ Your responses have been submitted successfully!")
        if any(r["answer_given"] in [None, ""] for r in responses):
            st.error("❌ Please answer all the questions before submitting.")
        else:
            # save_response(student_name, chapter, responses)
            # st.success("✅ Your responses have been submitted successfully!")
            # ✅ Prepare JSON response in memory
            record = {
                "student_name": student_name,
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "chapter": chapter,
                "responses": responses
            }

            # ✅ Convert to JSON and bytes
            response_json_str = json.dumps(record, indent=4)
            response_bytes = io.BytesIO(response_json_str.encode("utf-8"))

            st.success("✅ Your responses have been recorded!")
            st.download_button(
                label="📥 Download Your Responses",
                data=response_bytes,
                # file_name=f"{student_name.replace(' ', '_')}_responses.json",
                file_name = f"{student_name.replace(' ', '_')}_{datetime.now().strftime('%Y%m%d_%H%M%S')}_responses.json",
                mime="application/json"
            )

