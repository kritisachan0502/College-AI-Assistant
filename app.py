from dotenv import load_dotenv
import os
import streamlit as st
from openai import OpenAI

# .env file se environment variables load karein
load_dotenv()

# OpenAI API key fetch karein
api_key = os.getenv("OPENAI_API_KEY")

if not api_key:
  st.error("⚠️ OPENAI_API_KEY nahi mili! Kripya .env file check karein.")
  st.stop()

# OpenAI Client Initialize Karein
client = OpenAI(api_key=api_key)

# Streamlit Page Config
st.set_page_config(page_title="College AI Assistant", page_icon="🎓")
st.title("🎓 College AI Assistant")
st.caption("College se Jude Sawal Pucho Aur AI Se Help Lo!")

# Session State Mein Chat History Maintain Karein
if "messages" not in st.session_state:
  st.session_state.messages = []

# Purani Chat Screen Par Dikhayein
for msg in st.session_state.messages:
  with st.chat_message(msg["role"]):
    st.markdown(msg["content"])

# User Input Lena
if prompt := st.chat_input("Apna sawal yahan puchein..."):
  # User ka message session state me add karein aur display karein
  st.session_state.messages.append({"role": "user", "content": prompt})
  with st.chat_message("user"):
    st.markdown(prompt)

  # OpenAI se response generate karna
  try:
    with st.chat_message("assistant"):
      with st.spinner("Soch rahe hain..."):
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",  # Aap yahan "gpt-4o" ya koi aur model bhi use kar sakte hain
            messages=[
                {
                    "role": "system",
                    "content": (
                        "Aap ek helpful college AI assistant hain jo college"
                        " ke baare mein sawalon ke jawab deta hai."
                    ),
                }
            ]
            + st.session_state.messages,
        )
        bot_reply = response.choices[0].message.content
        st.markdown(bot_reply)

    # Assistant ka reply session state me save karein
    st.session_state.messages.append({"role": "assistant", "content": bot_reply})

  except Exception as e:
    st.error(f"Error aa gaya: {e}")
