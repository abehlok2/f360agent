import autogen
import os
from autogen import *
from autogen.agentchat.contrib.multimodal_conversable_agent import MultimodalConversableAgent
from autogen.agentchat.contrib.teachable_agent import TeachableAgent
from autogen.agentchat.contrib.gpt_assistant_agent import GPTAssistantAgent
from config.prompts import script_generator_system_message

user = autogen.UserProxyAgent(
    name="user",
    code_execution_config={"work_dir": r"C:\Users\abehl\f360" },
    max_consecutive_auto_reply=1   
)


class Fusion360Agent(TeachableAgent):
    super().__init__(
        name="Fusion 360 Scripting Agent",
        system_message=script_generator_system_message,
        llm_config = {
            "api_key": os.getenv("OPENAI_API_KEY"),
            "model": "gpt-4-1106-preview",
            "temperature": 0,
            "max_tokens": 200,
        },
        analyzer_llm_config={
            "api_key": os.getenv("OPENAI_API_KEY"),
            "model": "gpt-4-1106-preview",
            "temperature": 0,
            "max_tokens": 200,
        },
        


    )






