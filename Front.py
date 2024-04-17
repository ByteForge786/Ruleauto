import streamlit as st
from transformers import AutoModelForCausalLM, AutoTokenizer

# App title
st.set_page_config(page_title="🦙💬 Llama 2 Chatbot")

@st.cache(allow_output_mutation=True)
def ChatModel(temperature, top_p):
    tokenizer = AutoTokenizer.from_pretrained("your-model-name-or-path")
    model = AutoModelForCausalLM.from_pretrained("your-model-name-or-path")
    return tokenizer, model

# Replicate Credentials
with st.sidebar:
    st.title('🦙💬 Llama 2 Chatbot')

    st.subheader('Models and parameters')
    
    temperature = st.sidebar.slider('temperature', min_value=0.01, max_value=2.0, value=0.1, step=0.01)
    top_p = st.sidebar.slider('top_p', min_value=0.01, max_value=1.0, value=0.9, step=0.01)

    chat_tokenizer, chat_model = ChatModel(temperature, top_p)

if "messages" not in st.session_state.keys():
    st.session_state.messages = [{"role": "assistant", "content": "How may I assist you today?"}]

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

def clear_chat_history():
    st.session_state.messages = [{"role": "assistant", "content": "How may I assist you today?"}]
st.sidebar.button('Clear Chat History', on_click=clear_chat_history)

def generate_llama2_response(prompt_input):
    string_dialogue = "You are a helpful assistant. You do not respond as 'User' or pretend to be 'User'. You only respond once as 'Assistant'."
    for dict_message in st.session_state.messages:
        if dict_message["role"] == "user":
            string_dialogue += "User: " + dict_message["content"] + "\\n\\n"
        else:
            string_dialogue += "Assistant: " + dict_message["content"] + "\\n\\n"
    input_ids = chat_tokenizer.encode(string_dialogue + prompt_input, return_tensors="pt")
    output = chat_model.generate(input_ids, do_sample=True, temperature=temperature, top_p=top_p, max_length=50)
    return chat_tokenizer.decode(output[0], skip_special_tokens=True)

if prompt := st.chat_input():
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

if st.session_state.messages[-1]["role"] != "assistant":
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            response = generate_llama2_response(prompt)
            st.write(response)
            st.session_state.messages.append({"role": "assistant", "content": response})
