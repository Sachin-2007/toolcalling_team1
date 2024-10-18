import streamlit as st
import json
from llm import GPT4LLMHandler
from template import PromptTemplate

instructions = '''You are a query solver. You will be given tools. Using those tools, you have to solve the query. 
To solve the query, at each point, you have to ask sub-questions. These sub-questions are "What is the next tool to use, its arguments and argument values?". Look at answers to the previous sub-questions, which will give you context of how the current set of tools have been chosen so far. Compare this to the greater context, which is, how to solve the next question.

Some important points :
1) Tool description and argument description are very important. Read them to understand what exactly a certain tool generates as output or what inputs a tool can get.
2) Output of tools in the previous step is input to tool for current statement. Compare descriptions, types and examples to get a huge clue.
3) Always check if authentication tools like "who_am_i", "team_id", "get_sprint_id", etc. are needed at any point.
4) Take care of "type" argument in "works_list" is issue, ticket or task are explicitly mentioned.
5) You can access the output of the ith task using "$$PREV[i]". i starts from 0.
6) Stop once you feel the task is complete and no further tools are needed to solve the query.
7) To answer the query, you are only allowed to use the tools that we have provided.
8) If the question is simply unsolvable using any tool we have, only return {"tools: []}'''
examples = [{
    "tools":
    [
        {
            "tool_name": "works_list",
            "arguments": [
                {
                    "argument_name": "ticket_severity",
                    "argument_value": [
                        "blocker"
                    ]
                },
                {
                    "argument_name": "type",
                    "argument_value": [
                        "ticket"
                    ]
                }
            ]
        }
    ]
},
        {
    "tools":
        [
            {
                "tool_name": "search_object_by_name",
                "arguments": [
                    {
                        "argument_name": "query",
                        "argument_value": "Globex"
                    }
                ]
            },
            {
                "tool_name": "works_list",
                "arguments": [
                    {
                        "argument_name": "created_by",
                        "argument_value": "$$PREV[0]"
                    },
                    {
                        "argument_name": "ticket_severity",
                        "argument_value": [
                            "high"
                        ]
                    },
                    {
                        "argument_name": "type",
                        "argument_value": [
                            "ticket"
                            ]
                    }
                ]
            }
        ]
}
]
model_params = {}

st.write('# GPT4 tool caller')
query = st.text_input('Enter query here')
st.write('## Model settings')
model_params['temperature'] = st.slider('Temperature', 0.0, 2.0, 1.0)
model_params['max_tokens'] = st.number_input('Max tokens', min_value=0, max_value=10000, value=2500)

file = st.file_uploader('JSON file with tools', 'json')

if file is not None:
    with open('custom_tools.json', "wb") as f:
        f.write(file.read())
    prompt = PromptTemplate(instructions, examples, query, tools_file='custom_tools.json')
else:
    prompt = PromptTemplate(instructions, examples, query)
    

if st.button("Get response"):
    llm = GPT4LLMHandler(temperature=model_params['temperature'], max_tokens=model_params['max_tokens'])
    response = llm.generate_response(prompt.get()['system_message'], prompt.get()['user_message'])
    st.write(json.dumps(json.loads(response['response'])['tools'], sort_keys=False, indent=4))
    st.write(f"Latency: {response['latency']}, secs")
    st.write(f"Cost: {response['cost']} USD")

    
