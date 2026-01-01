# banking_lib.py

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





def banking_query(user_query, ollama_chat):
    response = ollama_chat(
        model="llama3",
        messages=[
            {"role": "system", "content": BANKING_SYSTEM_PROMPT},
            {"role": "user", "content": user_query}
        ],
        stream=False
    )

    answer = response["message"]["content"].strip()

    if answer == "NOT_BANKING":
        return False
    return True
