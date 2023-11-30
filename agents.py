import autogen
import os
from autogen import *
from autogen.agentchat.contrib.teachable_agent import TeachableAgent
from autogen import ChatCompletion, GroupChat, GroupChatManager
from config.prompts import script_checker_system_message, script_generator_system_message, mechanical_engineer_system_message

class Fusion360Agent(TeachableAgent):
    def __init__(self, is_script: bool , **kwargs):

        """
        Initializes a Fusion 360 Scripting / Add-on Agent

        This agent creates Fusion 360 scripts using the Fusion 360 API to carry out operations for the user.

        Parameters:
            -max_rounds (int): The maximum number of rounds of conversation to carry out
            -script_or_add_on (bool): True if the agent is creating a script, False if the agent is creating an add-on
        """
        self.is_script = is_script,
        super().__init__(
            name="Fusion 360 Scripting Agent",
            system_message=script_generator_system_message,
            llm_config = {
                "api_key": os.getenv("OPENAI_API_KEY"),
                "model": "gpt-4-1106-preview",
                "temperature": 0,
                "max_tokens": 200,
                },
            )

    def generate_model(self, user_input: str):
            # Create agents 
            user = autogen.UserProxyAgent(
                name="user",
                code_execution_config={"work_dir": r"C:\Users\abehl\AppData\Local\Autodesk\webdeploy\production\3167d85f5fd4280287d8295f20592fa13b977617\Python\Samples" },
                max_consecutive_auto_reply=1
                )

            script_checker = autogen.AssistantAgent(
                name="script_checker",
                llm_config={
                    "api_key": os.getenv("OPENAI_API_KEY"),
                    "model": "gpt-4-1106-preview",
                    "temperature": 0,
                    "max_tokens": 200,
                },
                system_message=script_checker_system_message,
            )    
            
            mechanical_engineer = autogen.AssistantAgent(
                name="mechanical_engineer",
                llm_config = {
                    "api_key": os.getenv("OPENAI_API_KEY"),
                    "model": "gpt-4-1106-preview",
                    "temperature": 0,
                    "max_tokens": 500,
                },
                human_input_mode="NEVER",
                system_message=mechanical_engineer_system_message,
            )

            scripting_group_chat = GroupChat(
                agents=[user, script_checker, mechanical_engineer],
                max_round=5,
                admin_name="user",
                messages=[],
                speaker_selection_method="auto",
                allow_repeat_speaker=False,
            )

            scripting_groupchat_manager = GroupChatManager(
                groupchat=scripting_group_chat,
            )
            
            user.initiate_chat(scripting_groupchat_manager, message=user_input)
       


f360agent = Fusion360Agent(
    is_script=True
)

model_script = f360agent.generate_model("Please write a script to create a 40mm cube centered on the origin point.")
print(model_script)


