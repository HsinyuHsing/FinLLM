import streamlit as st
from langchain.memory import ConversationBufferMemory
from FinLLM import create_ai_agent_team, get_ai_response


# 終端機: streamlit run main.py  呈現網頁
st.title("AI Investment Assistant")

with st.sidebar:
    openai_api_key = st.text_input("請輸入OpenAI API Key：", type="password")
    st.markdown("[獲取OpenAI API key](https://platform.openai.com/account/api-keys)")
    serper_api_key = st.text_input("請輸入Serper API Key：", type="password")
    st.markdown("[獲取Serper API Key](https://serper.dev/)")
   

# 如果"memory"不再會話狀態裡，則運行ConversationBufferMemory(return_messages=True)
# ConversationBufferMemory(return_messages=True) 初始化記憶
if "memory" not in st.session_state:
    # st.session_state["memory"] = ConversationBufferMemory(return_messages=True)

    st.session_state["memory"] = ConversationBufferMemory(memory_key="chat_history", return_messages=True)

    st.session_state["messages"] = [{"role": "ai",
                                     "content": "Hello, I am your AI Investment Assistant. How can I assist you today？"}]

# 針對繪畫的每一條挑息，都要在頁面上進行展式 st.chat_message
for message in st.session_state["messages"]:
    st.chat_message(message["role"]).write(message["content"])

# 輸入對話消息
prompt = st.chat_input()
if prompt:
    if not openai_api_key:
        st.info("請輸入OpenAI API Key")
        st.stop()
    if not serper_api_key:
        st.info("請輸入Serper API Key")
        st.stop()
    st.session_state["messages"].append({"role": "human", "content": prompt})
    st.chat_message("human").write(prompt)

    with st.spinner("AI正在思考中，请稍等..."):
        # 傳遞 memory 和 prompt 给 create_ai_agent_team
        response = create_ai_agent_team(openai_api_key, serper_api_key, st.session_state["memory"])
        
        # 使用 get_ai_response 函数獲取 AI 回應
        ai_response = get_ai_response(response, prompt)

    msg = {"role": "ai", "content": ai_response}
    st.session_state["messages"].append(msg)
    st.chat_message("ai").write(ai_response)
