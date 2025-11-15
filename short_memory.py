

from langchain_ollama import ChatOllama
from langchain_core.messages import SystemMessage, HumanMessage
from langchain.agents import create_agent
from langgraph.checkpoint.memory import MemorySaver # Short-Term Memory
from financial_tool import TOOLS 


CHAT_MODEL = ChatOllama(base_url="http://localhost:11434", model="llama3.1:8b-instruct", temperature=0)

BASE_SYSTEM_MESSAGE = (
    "You are a professional Financial Analyst and Portfolio Manager. "
    "Your core duty is to monitor tech stocks and provide actionable "
    "investment strategies (Buy, Hold, or Sell recommendation) based on recent news. "
    "You must ALWAYS use the 'get_financial_news' tool to retrieve relevant data before making a recommendation. "
    "Your answer should include: 1. The news snippet(s) you found. 2. A clear recommendation. 3. The rationale."
)

def run_short_memory_agent(initial_query: str, follow_up_query: str):

    checkpointer = MemorySaver() 
    
 
    graph = create_agent(
        model=CHAT_MODEL,
        tools=TOOLS,
        prompt=BASE_SYSTEM_MESSAGE,
        checkpointer=checkpointer 
    )

    cfg = {"configurable": {"thread_id": "short-memory-test"}}

    turn_1_messages = [HumanMessage(content=initial_query)]
    print(f"\n[Turn 1 Human]: {initial_query}")
    state1 = graph.invoke({"messages": turn_1_messages}, config=cfg)
    print(f"\n[Turn 1 Agent Response]:\n{state1['messages'][-1].content}")


    turn_2_messages = [HumanMessage(content=follow_up_query)]
    print(f"\n[Turn 2 Human]: {follow_up_query}")
    state2 = graph.invoke({"messages": turn_2_messages}, config=cfg)
    print(f"\n[Turn 2 Agent Response]:\n{state2['messages'][-1].content}")


if __name__ == "__main__":
    INITIAL_QUERY = "What is the investment recommendation for MSFT based on recent news?"
    FOLLOW_UP_QUERY = "Now, how should I handle the position? And what is the total value of my portfolio?"
    run_short_memory_agent(INITIAL_QUERY, FOLLOW_UP_QUERY)