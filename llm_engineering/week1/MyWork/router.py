
import streamlit as st
from service import LLMService

# Initialize session state for chat history
if 'chat_history' not in st.session_state:
    st.session_state['chat_history'] = []
if 'code_input' not in st.session_state:
    st.session_state['code_input'] = ''

service = LLMService(model_name="llama3.2")

st.set_page_config(layout="wide")
st.title("LLMService Chatbot")

# Custom CSS for scrollable history window
st.markdown("""
    <style>
    .scroll-window {
        height: 600px;
        overflow-y: auto;
        padding: 1em;
        background-color: #0f0f17;
        border-radius: 8px;
        border: 1px solid #ddd;
    }
    </style>
""", unsafe_allow_html=True)

# Layout: left for chat/code input, right for history
input_col, history_col = st.columns([1,2])

with input_col:
   
    st.subheader("Code Chat")
    code_input = st.text_area("Paste your code here:", value=st.session_state['code_input'], key="code_input_box")
    st.session_state['code_input'] = code_input

    # Use equal width columns and custom CSS for tight spacing
    colA, colB = st.columns([1,1], gap="small")
    with colA:
        st.markdown("<div style='margin-right:-10px'>", unsafe_allow_html=True)
        if st.button("Analyze Code"):
            result = service._analyze_code(code_input)
            st.session_state['chat_history'].append(("Analyze Code", code_input, result))
        st.markdown("</div>", unsafe_allow_html=True)
    with colB:
        st.markdown("<div style='margin-left:-10px'>", unsafe_allow_html=True)
        if st.button("Explain Code"):
            result2 = service._explain_code(code_input)
            st.session_state['chat_history'].append(("Explain Code", code_input, result2))
        st.markdown("</div>", unsafe_allow_html=True)

    st.subheader("Normal Chat")
    chat_input = st.text_area("Enter your message:", key="chat_input_box")

    if st.button("Send Chat"):
        code_context = st.session_state['code_input'] if st.session_state['code_input'] else None
        result = service.process_query(chat_input, code=code_context)
        st.session_state['chat_history'].append((chat_input, code_context, result))


with history_col:
    st.subheader("Chat & Code History")
    # All history content inside the scrollable div
    history_html = "<div class='scroll-window'>"
    # Normal Chat History
    history_html += "<h4>Normal Chat History</h4>"
    if st.session_state['chat_history']:
        for query, code, response in st.session_state['chat_history']:
            history_html += f"<b>User:</b> {query}<br>"
            if code:
                history_html += f"<b>Code Context:</b>" + f"<pre>{code}</pre>"
            history_html += f"<b>Response:</b> {response}<hr>"
    else:
        history_html += "<i>No normal chat history yet.</i><br>"

    history_html += "</div>"
    st.markdown(history_html, unsafe_allow_html=True)