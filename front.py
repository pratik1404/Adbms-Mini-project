import streamlit as st
from pymongo import MongoClient
import hashlib

# MongoDB Setup
client = MongoClient("mongodb://localhost:27017/")  # Replace with your connection string
db = client['quiz_app']
users_collection = db['users']
quizzes_collection = db['quizzes']

# Hash passwords for security
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# Function to check login credentials
def check_login(email, password):
    hashed_password = hash_password(password)
    user = users_collection.find_one({"email": email, "password": hashed_password})
    return user

# Function to register a new user (with admin option)
def register_user(name, email, password, is_admin=False):
    hashed_password = hash_password(password)
    users_collection.insert_one({"name": name, "email": email, "password": hashed_password, "is_admin": is_admin, "scores": {}})

# Function to check if user is an admin
def is_admin(email):
    user = users_collection.find_one({"email": email})
    return user.get("is_admin", False)

# Function to get all quizzes by subject
def get_quizzes_by_subject(subject):
    return quizzes_collection.find_one({"subject": subject})

# Function to save or edit quiz (Admin CRUD)
def save_quiz(subject, questions):
    quizzes_collection.update_one(
        {"subject": subject},
        {"$set": {"subject": subject, "questions": questions}},
        upsert=True
    )

# Function to delete a quiz
def delete_quiz(subject):
    quizzes_collection.delete_one({"subject": subject})

# Function to update user's quiz score in MongoDB
def update_user_score(email, subject, score):
    users_collection.update_one(
        {"email": email},
        {"$set": {f"scores.{subject}": score}}  # Using dot notation to store scores per subject
    )

# Streamlit App
st.title("Quiz Application")

# Navigation state
if 'current_page' not in st.session_state:
    st.session_state.current_page = "home"

# Function to render the home page
def render_home():
    st.subheader("Welcome to the Quiz Application!")
    st.write("Please log in or register to start.")

# Function to render the login/registration page
def render_login_registration():
    st.subheader("Login or Register")

    with st.form(key="login_form"):
        email = st.text_input("Email")
        password = st.text_input("Password", type="password")
        login_button = st.form_submit_button("Login")

        if login_button:
            user = check_login(email, password)
            if user:
                st.session_state.logged_in = True
                st.session_state.email = user['email']
                st.session_state.name = user['name']
                st.session_state.is_admin = user.get('is_admin', False)
                st.success(f"Welcome back, {user['name']}!")
                st.session_state.current_page = "quiz_selection"
            else:
                st.error("Invalid credentials. Please try again or register.")

    st.write("New user? Register below:")

    with st.form(key="register_form"):
        name = st.text_input("Name")
        reg_email = st.text_input("Registration Email")
        reg_password = st.text_input("Registration Password", type="password")
        is_admin = st.checkbox("Register as Admin")
        register_button = st.form_submit_button("Register")

        if register_button:
            existing_user = users_collection.find_one({"email": reg_email})
            if existing_user:
                st.error("User with this email already exists. Please login.")
            else:
                register_user(name, reg_email, reg_password, is_admin)
                st.success("Registration successful! Please log in.")

# Function to render the quiz selection page
def render_quiz_selection():
    st.write(f"Welcome back, {st.session_state.name}!")

    # Quiz Subject Selection
    subjects = ["Operating Systems", "ADBMS", "Machine Learning", "Data Structures", "Computer Networks"]

    # Select subject for the quiz
    selected_subject = st.selectbox("Select a subject for the quiz:", [""] + subjects)

    if selected_subject:
        # Fetch quizzes for the selected subject
        quiz_data = get_quizzes_by_subject(selected_subject)

        if quiz_data:
            if st.button("Start Quiz"):
                st.session_state.quiz_started = True
                st.session_state.user_answers = [None] * len(quiz_data['questions'])  # Initialize with None
                st.session_state.selected_subject = selected_subject

            if st.session_state.get('quiz_started', False):
                st.write("### Quiz Started! Answer the following questions:")
                for idx, question in enumerate(quiz_data['questions']):
                    # Radio buttons without a pre-selected value
                    user_answer = st.radio(f"**Q{idx + 1}. {question['question']}**", question['choices'], key=f"q{idx}")

                    # Update user answers only if an option is selected
                    if user_answer:
                        st.session_state.user_answers[idx] = user_answer

                if st.button("Submit Answers"):
                    correct_answers = [q['answer'] for q in quiz_data['questions']]
                    score = sum(1 for user_ans, correct_ans in zip(st.session_state.user_answers, correct_answers) if user_ans == correct_ans)
                    total_questions = len(correct_answers)
                    st.success(f"You scored **{score}** out of **{total_questions}**!")

                    # Display correct answers
                    for idx, question in enumerate(quiz_data['questions']):
                        st.write(f"**Q{idx + 1}:** {question['question']}")
                        st.write(f"**Your Answer:** {st.session_state.user_answers[idx] if st.session_state.user_answers[idx] else 'Not answered'}")
                        st.write(f"**Correct Answer:** {question['answer']}")

                    # Update the user's score in MongoDB
                    update_user_score(st.session_state.email, selected_subject, score)
        else:
            st.write("No quiz available for this subject.")

    # Admin Section (CRUD)
    if st.session_state.is_admin:
        st.write("### Admin Section")
        admin_subject = st.selectbox("Select a subject to add/edit quiz:", subjects)
        new_questions = []

        num_questions = st.number_input("Number of Questions", min_value=1, step=1)
        for i in range(num_questions):
            question = st.text_input(f"Question {i+1}")
            choices = st.text_input(f"Choices (comma-separated) for Question {i+1}").split(',')
            answer = st.text_input(f"Correct Answer for Question {i+1}")
            new_questions.append({
                "question": question,
                "choices": [choice.strip() for choice in choices],
                "answer": answer.strip()
            })

        if st.button("Save Quiz"):
            save_quiz(admin_subject, new_questions)
            st.success(f"Quiz for {admin_subject} saved successfully!")

        # Delete Quiz Section
        st.write("### Delete Quiz")
        delete_subject = st.selectbox("Select a subject to delete:", subjects)
        if st.button("Delete Quiz"):
            delete_quiz(delete_subject)
            st.success(f"Quiz for {delete_subject} deleted successfully!")

# Function to navigate back to home or quiz selection
def back_to_page(page):
    st.session_state.current_page = page

# Render pages based on current page state
if st.session_state.current_page == "home":
    render_home()
    if st.button("Go to Login/Register"):
        back_to_page("login_registration")
elif st.session_state.current_page == "login_registration":
    render_login_registration()
    if st.button("Back to Home"):
        back_to_page("home")
elif st.session_state.current_page == "quiz_selection" and st.session_state.get('logged_in', False):
    render_quiz_selection()
    if st.button("Back to Home"):
        back_to_page("home")
