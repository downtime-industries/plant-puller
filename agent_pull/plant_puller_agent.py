import os

from haystack.agents import Agent, Tool
from haystack.agents.base import ToolsManager
from haystack.nodes import PromptNode, PromptTemplate
from haystack.nodes.retriever.web import WebRetriever
from haystack.pipelines import WebQAPipeline
from agent_pull.zypher_pn import get_prompt_node
import dotenv

dotenv.load_dotenv()

search_key = os.environ.get("SEARCH_KEY")
if not search_key:
    raise ValueError("Please set the SEARCH_KEY environment variable")

pn = get_prompt_node(
    default_prompt_template="question-answering-with-document-scores",
)
web_retriever = WebRetriever(search_engine_provider="GoogleAPI", api_key=search_key)
pipeline = WebQAPipeline(retriever=web_retriever, prompt_node=pn)

few_shot_prompt = """
You are a helpful and knowledgeable agent. Your role is to create data sent entries for the requested data points matching the appropriate schema. To achieve your goal of building this dataset, you have access to the following tools:

Search: useful for when you need to Google questions. You should ask targeted questions, for example, Who is Anthony Dirrell's brother?

To answer questions, you'll need to go through multiple steps involving step-by-step thinking and selecting appropriate tools and their inputs; tools will respond with observations. When you are ready for a final answer, respond with the `Final Answer:`
Examples:
##
Question: How do I care for a alocasia amazonica? Format your answer to fill out this json object and store it: { "plant": "alocasia amazonica", "light_requirements": "", "soil": "", "water_requirements": "", "temperature": "" }
Thought: Let's think step by step. To answer this question, we first need to know what care for the alocasia amazonica is. 
Tool: Search
Tool Input: Care for the alocasia amazonica?
Observation: Light: Bright Indirect, Soil: moisture retaining
Thought: We've learned that alocasia amazonica needs bright indirect light and water retaining soil. Now we need to find it's water requirements and temperature. 
Tool: Search
Tool Input: What are the watering requirements for the alocasia amazonica?
Observation: water requirements: frequent watering
Thought: We've learned that it needs frequent watering. Now, we need to find out what the temperature requirements are.
Tool: Search
Tool Input: What are the temperature requirements for alocasia amazonica?
Observation: 65-85f
Thought: We've now filled in all the fields. Now, we can answer the question with valid JSON.
Final Answer: { "plant": "alocasia amazonica", "light_requirements": "bright indirect", "soil": "moisture retaining", "water_requirements": "frequent", "temperature": "65-85f" }
##
Question: {query}
Thought:
{transcript}
"""

few_shot_agent_template = PromptTemplate(few_shot_prompt)
prompt_node = get_prompt_node(
    max_length=1024, stop_words=["Observation:"]
)

web_qa_tool = Tool(
    name="Search",
    pipeline_or_node=pipeline,
    description="useful for when you need to Google questions.",
    output_variable="results",
)

agent = Agent(
    prompt_node=prompt_node, prompt_template=few_shot_agent_template, tools_manager=ToolsManager([web_qa_tool])
)

hotpot_questions = [
    "How do you care for a ficus elastica ruby?"
]

for question in hotpot_questions:
    result = agent.run(query=question)
    print(f"\n{result}")
