import streamlit as st
from ollama import chat as ollama_chat
from banking_intellect import banking_query

# PAGE SETUP 
st.set_page_config(page_title="🤖 BankSense AI", layout="wide")

#  STATES 
if "all_chats" not in st.session_state:
    st.session_state.all_chats = []

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if "selected_chat_idx" not in st.session_state:
    st.session_state.selected_chat_idx = None

#  OLLAMA BOT 
BANKING_ANSWER_PROMPT = """
You are BankSense AI, a strict banking-domain assistant.

Rules:
- Answer ONLY banking and finance related questions.
- If the question is NOT related to banking or finance, respond with:
  "Sorry ⚠️ I can answer only banking-related questions."
- If a term has multiple meanings, explain ONLY the banking meaning.
- Do NOT answer questions related to science, electronics, physics, medicine, coding, or general knowledge.
- Keep answers simple, clear, and user-friendly.
"""





def ask_ollama(prompt):
    messages = [
        {"role": "system", "content": BANKING_ANSWER_PROMPT},
        {"role": "user", "content": prompt}
    ]

    with st.spinner("🤖 BankSense is processing..."):
        response = ollama_chat(
            model="llama3",
            messages=messages,
            stream=False
        )

    return response["message"]["content"]

# CHAT TITLE 
def generate_chat_title(chat_list):
    """
    Generates a meaningful chat title based on banking topic
    """

    topic_map = {
        "emi": "EMI Query",
        "loan": "Loan Related Query",
        "interest": "Interest Rate Information",
        "account": "Account Information",
        "balance": "Account Balance Issue",
        "deposit": "Deposit Related Query",
        "fd": "Fixed Deposit Query",
        "rd": "Recurring Deposit Query",
        "credit": "Credit Card Query",
        "debit": "Debit Card Query",
        "atm": "ATM Related Query",
        "transaction": "Transaction Query",
        "statement": "Bank Statement Query",
        "kyc": "KYC Related Query",
        "net banking": "Net Banking Query",
        "upi": "UPI / Payment Query"
    }

    for msg in chat_list:
        if msg["role"] == "user":
            text = msg["content"].lower()

            # Ignore greetings
            if text.strip() in ["hi", "hello", "hii", "hey", "haiii"]:
                continue

            # Topic detection
            for keyword, title in topic_map.items():
                if keyword in text:
                    return title

            # Fallback: short cleaned sentence
            return text[:30].title()

    return "New Chat"


#  BANK BOT LOGIC 
def bankbot_reply(message):
    greetings = ["hi", "hello", "hii", "hey", "haiii"]
    
    if message.lower().strip() in greetings:
        return "Hello! 👋 Please ask me about banking-related queries."
    
    # AI-based banking detection
    is_banking = banking_query(message, ollama_chat)
    
    if is_banking:
        return ask_ollama(message)
    
    return "Sorry ⚠️ I can answer only banking-related questions."





#  SIDEBAR 
with st.sidebar:
    st.markdown("## 💬 Your Chats")

    if st.session_state.all_chats:
        for idx, chat_set in enumerate(st.session_state.all_chats):
            col1, col2 = st.columns([4, 1])

            title = generate_chat_title(chat_set)

            # Open chat
            with col1:
                if st.button(title, key=f"open_{idx}"):
                    st.session_state.selected_chat_idx = idx

            # Delete chat
            with col2:
                if st.button("🗑️", key=f"delete_{idx}"):
                    st.session_state.all_chats.pop(idx)
                    if st.session_state.selected_chat_idx == idx:
                        st.session_state.selected_chat_idx = None
                    st.rerun()
    else:
        st.write("No saved chats.")

    st.write("---")

    # New Chat
    if st.button("🆕 New Chat"):
        if st.session_state.chat_history:
            st.session_state.all_chats.append(
                st.session_state.chat_history.copy()
            )
        st.session_state.chat_history = []
        st.session_state.selected_chat_idx = None
        st.rerun()

# LOAD SELECTED CHAT 
if st.session_state.selected_chat_idx is not None:
    st.session_state.chat_history = st.session_state.all_chats[
        st.session_state.selected_chat_idx
    ].copy()

# MAIN UI 
st.title("🤖 BankSense AI — Banking Assistant")

for chat in st.session_state.chat_history:
    with st.chat_message(chat["role"]):
        st.write(chat["content"])

user_input = st.chat_input("Ask your banking question...")

if user_input:
    st.session_state.chat_history.append(
        {"role": "user", "content": user_input}
    )

    reply = bankbot_reply(user_input)

    st.session_state.chat_history.append(
        {"role": "assistant", "content": reply}
    )

    st.rerun()
