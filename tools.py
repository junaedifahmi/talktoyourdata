from langchain.agents.agent_types import AgentType
from langchain.chat_models import ChatOpenAI
from langchain.llms import OpenAI
from langchain_experimental.agents.agent_toolkits import create_csv_agent, create_pandas_dataframe_agent

from pydantic import BaseModel, Field
from langchain.tools import tool, StructuredTool

from dotenv import load_dotenv

load_dotenv()

import pandas as pd


def ask_agent(query:str ) -> str:
    """the function will be used to analyze question regarding the dataframe"""
    df = pd.read_csv("./SPOTIFY_REVIEW.csv")
    df_question = create_pandas_dataframe_agent(
        llm=ChatOpenAI(temperature=0, model="gpt-4-1106-preview"),
        df=df,
        verbose=True
    )
    res = df_question.run(
        f"analyze this {query} and put your tought more deeply on review_text columns."
    )
    return res

df_tools = StructuredTool.from_function(
    func=ask_agent,
    name="analyze",
    description="This function will be used to analyze question regarding dataframe"
)
    

if  __name__ == "__main__":
    q = "What are the specific features or aspects that users appreciate the most in our application?"
    q = "In comparison to our application, which music streaming platform are users most likely to compare ours with?"
    q = "What are the primary reasons users express dissatisfaction with this app?"
    df_question = create_csv_agent(
        llm=ChatOpenAI(temperature=0, model="gpt-4-1106-preview"),
        path="./SPOTIFY_REVIEW.csv",
        verbose=True,
        
    )

    while True:
        q = input("your query\t:\t")
        if not q:
            print("invalid")
            continue
        ans = df_question.run(f"analyze this {q} and put your tought more deeply on review_text columns")
        print("bot ans\t\t:\t", ans.strip())
