import http.client
import json
from langchain_community.chat_models import ChatOpenAI
from langchain.agents import AgentType, initialize_agent
from langchain.tools import Tool
from langchain import hub
from langchain.agents import create_structured_chat_agent, AgentExecutor

def fetch_news(query, serper_api_key):
    """使用 Google Serper API 查詢最新新聞"""
    conn = http.client.HTTPSConnection("google.serper.dev")
    payload = json.dumps({"q": query, "hl": "zh-tw"})
    headers = {
        'X-API-KEY': serper_api_key, 
        'Content-Type': 'application/json'
    }
    conn.request("POST", "/news", payload, headers)
    res = conn.getresponse()
    data = res.read()
    return data.decode("utf-8")

def fetch_stock_price(symbol):
    """模擬查詢股票價格"""
    return f"查詢 {symbol} 的股價（模擬結果）"

def decision_making(data):
    """根據新聞與數據給出決策建議"""
    return f"根據分析，建議策略為：{data}（模擬決策）"

def create_ai_agent_team(openai_api_key, serper_api_key, memory):
    """建立 AI Agent 團隊，包含新聞查詢、股票查詢、決策等功能"""
    
    # 初始化 LLM
    llm = ChatOpenAI(model="gpt-3.5-turbo", openai_api_key=openai_api_key)

    # 建立不同的 Agents
    news_tool = Tool(name="新聞查詢",
    func=lambda query: fetch_news(query, serper_api_key),
    description="查詢最新新聞")
    stock_tool = Tool(name="股票查詢", func=fetch_stock_price, description="查詢股價")
    decision_tool = Tool(name="決策建議", func=decision_making, description="提供投資決策建議")

    # 整合 Agent
    tools = [news_tool, stock_tool, decision_tool]
    prompt = hub.pull("hwchase17/structured-chat-agent")
    agent = create_structured_chat_agent(
            llm=llm,
            tools=tools,
            prompt=prompt)   
    
    agent_team = AgentExecutor.from_agent_and_tools(
                agent=agent, 
                tools=tools, 
                memory=memory, 
                verbose=True, 
                handle_parsing_errors=True)

    return agent_team

def get_ai_response(agent_team, prompt):
    """使用 agent_team 處理 prompt 並返回回應"""
    response = agent_team.invoke({"input": prompt})  # 用invoke來調用 AI 回應


    # response = agent_team.invoke({"input": prompt, "chat_history": agent_team.memory['chat_history']})
    return response["output"]  # 返回回應內容


# # streamlit run FinLLM.py


