import streamlit as st
from transformers import AutoTokenizer, AutoModelForCausalLM

# App title
st.set_page_config(page_title="🦙💬 Llama 2 Chatbot")

@st.cache(allow_output_mutation=True)
def ChatModel(tokenizer_name, model_name, temperature, top_p):
    tokenizer = AutoTokenizer.from_pretrained(tokenizer_name)
    model = AutoModelForCausalLM.from_pretrained(model_name)
    model.config.temperature = temperature
    model.config.top_p = top_p
    return tokenizer, model

# Replicate Credentials
with st.sidebar:
    st.title('🦙💬 Llama 2 Chatbot')

    # Refactored from <https://github.com/a16z-infra/llama2-chatbot>
    st.subheader('Models and parameters')
    
    temperature = st.sidebar.slider('temperature', min_value=0.01, max_value=2.0, value=0.1, step=0.01)
    top_p = st.sidebar.slider('top_p', min_value=0.01, max_value=1.0, value=0.9, step=0.01)
    # Add tokenizer and model names here
    tokenizer_name = 'tokenizer_name'
    model_name = 'model_name'
    chat_tokenizer, chat_model = ChatModel(tokenizer_name, model_name, temperature, top_p)

# Store LLM generated responses
if "messages" not in st.session_state.keys():
    st.session_state.messages = [{"role": "assistant", "content": "How may I assist you today?"}]

# Display or clear chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

def clear_chat_history():
    st.session_state.messages = [{"role": "assistant", "content": "How may I assist you today?"}]
st.sidebar.button('Clear Chat History', on_click=clear_chat_history)

# Function for generating LLaMA2 response
def generate_llama2_response(prompt_input):
    # Generate tokens from prompt input
    input_ids = chat_tokenizer.encode(prompt_input, return_tensors="pt")
    # Generate response
    output = chat_model.generate(input_ids, max_length=150, pad_token_id=chat_tokenizer.eos_token_id)
    # Decode response tokens to text
    response = chat_tokenizer.decode(output[0], skip_special_tokens=True)
    return response

# User-provided prompt
if prompt := st.chat_input():
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

# Generate a new response if last message is not from assistant
if st.session_state.messages[-1]["role"] != "assistant":
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            response = generate_llama2_response(prompt)
            st.write(response)
    message = {"role": "assistant", "content": response}
    st.session_state.messages.append(message)
