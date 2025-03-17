import streamlit as st
import google.generativeai as genai  # Using Gemini API
import os
from dotenv import load_dotenv  # Import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get API key from environment variables
api_key = os.getenv("GEMINI_API_KEY")

if api_key:
    genai.configure(api_key=api_key)
else:
    raise ValueError("GEMINI_API_KEY is not set. Please check your .env file.")


# Function to fetch AI-generated answers from Gemini 1.5 Flash
def generate_answer(question):
    response = genai.GenerativeModel("gemini-1.5-flash").generate_content(question)
    return response.text if response and hasattr(response, "text") else "No answer available."

# Generate unlimited questions
def generate_questions(topic, difficulty):
    sample_questions = {
        "Beginner": [
            f"What is {topic} in simple terms?",
            f"How is {topic} used in real life?",
            f"Give an example of {topic} in action.",
            f"What are the benefits of using {topic}?",
            f"How does {topic} compare to traditional methods?"
        ],
        "Intermediate": [
            f"Explain the working of {topic} with a practical example.",
            f"What are the key challenges in {topic}?",
            f"How does {topic} compare to similar technologies?",
            f"What are some advanced use cases of {topic}?",
            f"What is the role of {topic} in modern AI?"
        ],
        "Advanced": [
            f"Discuss the mathematical foundations behind {topic}.",
            f"What are the latest advancements in {topic}?",
            f"How can {topic} be optimized for better performance?",
            f"Explain the limitations of {topic}.",
            f"What are the research trends in {topic}?"
        ]
    }
    return sample_questions.get(difficulty, [])

# Generate additional questions for deep learning
def generate_extra_questions(topic):
    return [
        f"What are the ethical concerns of {topic}?",
        f"How does {topic} impact the future of technology?",
        f"What are some case studies on {topic}?",
        f"How does {topic} interact with other AI technologies?",
        f"What are the biggest misconceptions about {topic}?"
    ]

# Pagination function
def paginate_list(items, page, items_per_page=5):
    """Splits a list into pages and returns the items for the requested page."""
    start = (page - 1) * items_per_page
    end = start + items_per_page
    return items[start:end]

# Initialize session state
if "questions" not in st.session_state:
    st.session_state.questions = []
if "answers" not in st.session_state:
    st.session_state.answers = []
if "extra_questions" not in st.session_state:
    st.session_state.extra_questions = []
if "extra_answers" not in st.session_state:
    st.session_state.extra_answers = []
if "page" not in st.session_state:
    st.session_state.page = 1

# Streamlit UI - Sidebar for Topic Selection
st.sidebar.title("Personalized Learning Mentor")
topic = st.sidebar.text_input("Enter a topic to learn about:", "Neural Networks")
difficulty = st.sidebar.selectbox("Select difficulty level:", ["Beginner", "Intermediate", "Advanced"])

# Start Learning Button
if st.sidebar.button("Start Learning"):
    st.session_state.questions = generate_questions(topic, difficulty)
    st.session_state.answers = [(q, generate_answer(q)) for q in st.session_state.questions]
    st.session_state.extra_questions = generate_extra_questions(topic)  # Generate new extra questions
    st.session_state.extra_answers = [(q, generate_answer(q)) for q in st.session_state.extra_questions]  # Get answers for extra questions
    st.session_state.page = 1  # Reset to first page

# Pagination Controls
items_per_page = 5
total_pages = max(1, (len(st.session_state.questions) // items_per_page) + (1 if len(st.session_state.questions) % items_per_page != 0 else 0))
current_page = st.session_state.page

# Display Questions & Answers (Paginated)
if st.session_state.questions:
    st.header(f"📚 Learning {topic} - {difficulty} Level (Page {current_page})")
    
    # Get current page's questions
    paginated_qna = paginate_list(st.session_state.answers, current_page, items_per_page)

    for question, answer in paginated_qna:
        with st.expander(f"🔍 {question}"):
            st.write(answer if answer.strip() else "**No answer available for this question.**")

    # Pagination Buttons
    col1, col2, col3 = st.columns([1, 5, 1])
    
    with col1:
        if current_page > 1:
            if st.button("⬅️ Previous"):
                st.session_state.page -= 1
                st.rerun()

    with col3:
        if current_page < total_pages:
            if st.button("Next ➡️"):
                st.session_state.page += 1
                st.rerun()

    # Show numbered page buttons
    st.write("📄 Pages:")
    pagination_buttons = st.columns(total_pages)
    for i in range(total_pages):
        with pagination_buttons[i]:
            if st.button(str(i + 1)):
                st.session_state.page = i + 1
                st.rerun()

# Expand to Learn More Section with Unique Extra Questions
st.subheader("📖 Expand to Learn More")

if st.session_state.extra_answers:
    for question, answer in st.session_state.extra_answers:
        with st.expander(f"📌 {question}"):
            st.write(answer)
else:
    st.write("No additional explanations are available at the moment.")



           
            



    
    
