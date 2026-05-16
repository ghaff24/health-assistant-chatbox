import streamlit as st
from ctransformers import AutoModelForCausalLM

st.set_page_config(page_title="Health Assistant Chatbot")

@st.cache_resource()
def ChatModel():
    return AutoModelForCausalLM.from_pretrained(
        'llama-2-7b-chat.ggmlv3.q2_K.bin',
        model_type='llama',
        temperature=0.1,
        top_p=0.9,
        max_new_tokens=256,
        gpu_layers=50  
    )

with st.sidebar:
    st.title('🏥 Health Assistant Chatbot')
    st.markdown("Ask me anything about health, symptoms, nutrition, or wellness.")
    chat_model = ChatModel()

def clear_chat_history():
    st.session_state.messages = [{"role": "assistant", "content": "Hello! I'm your health assistant. How can I help you today? 🏥"}]

st.sidebar.button('Clear Chat History', on_click=clear_chat_history)

if "messages" not in st.session_state.keys():
    st.session_state.messages = [{"role": "assistant", "content": "Hello! I'm your health assistant. How can I help you today? 🏥"}]

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

def generate_response(prompt_input):
    string_dialogue = """You are a knowledgeable and friendly health assistant.
You provide helpful, accurate, and easy-to-understand information about medical topics,
symptoms, healthy habits, nutrition, and general wellness.
You always remind users to consult a real doctor for serious concerns.
You do not respond as 'User' or pretend to be 'User'. You only respond once as 'Assistant'. Keep answers short and clear."""

    for dict_message in st.session_state.messages:
        if dict_message["role"] == "user":
            string_dialogue += "User: " + dict_message["content"] + "\n\n"
        else:
            string_dialogue += "Assistant: " + dict_message["content"] + "\n\n"

    output = chat_model(f"prompt {string_dialogue} {prompt_input} Assistant: ")
    return output

if prompt := st.chat_input("Ask me anything about health..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

if st.session_state.messages[-1]["role"] != "assistant":
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            response = generate_response(prompt)
            placeholder = st.empty()
            full_response = ''
            for item in response:
                full_response += item
                placeholder.markdown(full_response)
            placeholder.markdown(full_response)
    message = {"role": "assistant", "content": full_response}
    st.session_state.messages.append(message)
