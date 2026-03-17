from src.genAI.services import *
from src.genAI.dtos import *



# def get_llm(model_choice: str):
#     if model_choice not in models:
#         raise ValueError("Invalid model choice")
#     details = models[model_choice]

#     llm = init_chat_model(
#         model=details["model_name"],
#         model_provider=details["provider"]
#     )

#     return llm

# def ask_ai(prompt: str, model_choice: str):
#     llm = get_llm(model_choice)
#     response = llm.invoke(prompt)
#     return response.content


# def generate_ai_chat(body:genAISchema):
#     result=ask_ai(
#         prompt=body.prompt,
#         model_choice=body.model
#     )
#     return {
#         "status":"ok",
#         "data":result
#     }



import os
from dotenv import load_dotenv
from langchain.chat_models import init_chat_model
from langchain_community.utilities import SQLDatabase
from langchain_community.agent_toolkits import SQLDatabaseToolkit
from langchain.agents import create_agent
import json


load_dotenv()

db = SQLDatabase.from_uri(
    "postgresql://postgres:Ayushsql@localhost:5433/institutemanagementsystem"
)

def generate_ai_chat(body):
    print("prompt")
    llm = init_chat_model(
        model="qwen/qwen3-32b",
        model_provider="groq"
    )

    toolkit = SQLDatabaseToolkit(db=db, llm=llm)
    tools = toolkit.get_tools()

    system_prompt = """
    You are an agent designed to interact with a SQL database.
    Given an input question, create a syntactically correct {dialect} query to run,
    then look at the results of the query and return the answer. Unless the user
    specifies a specific number of examples they wish to obtain, always limit your
    query to at most {top_k} results.

    You can order the results by a relevant column to return the most interesting
    examples in the database. Never query for all the columns from a specific table,
    only ask for the relevant columns given the question.

    You MUST double check your query before executing it. If you get an error while
    executing a query, rewrite the query and try again.

    DO Not make any DML statements (INSERT, UPDATE, DELETE, DROP etc.) to the
    database.

    To start you should ALWAYS look at the tables in the database to see what you
    can query. Do NOT skip this step.

    Then you should query the schema of the most relevant tables.
    """.format(
       dialect=db.dialect,
       top_k=5,
    )
    agent = create_agent(llm, tools, system_prompt=system_prompt)

    prompt = body.prompt
    print("prompt")

    response = agent.invoke({
        "messages": [
            {"role": "user", "content": prompt}
        ]
    })
    
    return {
        "status": "ok",
        "answer": response["messages"][-1].content.split("\n")
    }