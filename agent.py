from langchain.agents.agent_types import AgentType
from langchain.chat_models import ChatOpenAI
from langchain.llms import OpenAI
from langchain_experimental.agents.agent_toolkits import create_csv_agent, create_pandas_dataframe_agent

from langchain.agents.output_parsers import OpenAIFunctionsAgentOutputParser
from langchain.prompts import MessagesPlaceholder
from langchain.prompts import ChatPromptTemplate
from langchain.schema.runnable import RunnablePassthrough
from langchain.memory import ConversationBufferMemory
from langchain.agents import AgentExecutor
from langchain.agents.format_scratchpad import format_to_openai_functions
from langchain.tools.render import format_tool_to_openai_function

import pandas as pd

from dotenv import load_dotenv

load_dotenv()

from tools import df_tools

class AgenPintarUpdate:
    def __init__(self, system_prompt: str = "You are helpful but sassy assistant", tools: list = [], verbose=False) -> None:
        self.functions = [format_tool_to_openai_function(f) for f in tools]
        self.model = ChatOpenAI(temperature=0, model="gpt-4-1106-preview").bind(functions=self.functions)
        self.memory = ConversationBufferMemory(return_messages=True,memory_key="chat_history")
        self.prompt = ChatPromptTemplate.from_messages([
            ("system", system_prompt),
            MessagesPlaceholder(variable_name="chat_history"),
            ("user", "{input}"),
            MessagesPlaceholder(variable_name="agent_scratchpad")
        ])
        self.chain = RunnablePassthrough.assign(
            agent_scratchpad = lambda x: format_to_openai_functions(x["intermediate_steps"])
        ) | self.prompt | self.model | OpenAIFunctionsAgentOutputParser()
        self.qa = AgentExecutor(agent=self.chain, tools=tools, verbose=verbose, memory=self.memory)

    def convchain(self, query):
        if not query:
            return
        result = self.qa.invoke({"input": query})
        self.answer = result['output']
        return result["output"]

    def clr_history(self, count=0):
        self.chat_history = []
        return 
    
    def __call__(self, query):
        return self.convchain(query)


if __name__ == "__main__":
    system_prompt = """
        use provided tools to answer the question.
"""
    agen = AgenPintarUpdate(system_prompt=system_prompt, tools=[df_tools], verbose=True)
    while True:
        q = input("your query\t:\t")
        if not q:
            print("invalid")
            continue
        ans = agen(q)
        print("bot ans\t\t:\t", ans.strip())
