import autogen

# Configuration for the AI system
config_list = [
    {
        "api_type": "open_ai",
        "api_base": "http://localhost:1234/v1",
        "api_key": "NULL"
    }
]

# Language model configuration
llm_config = {
    "request_timeout": 400,
    "seed": 42,
    "config_list": config_list,
    "temperature": 0.7,
    "max_token_count": -1
}

# Create AI agents

# Boss agent has high-level knowledge and can analyze and tweak code.
Boss = autogen.AssistantAgent(
    name="Boss",
    llm_config=llm_config,
    human_input_mode="NEVER",
    max_consecutive_auto_reply=10,
    code_execution_config={"work_dir": "coding"},
    system_message="You are the Boss. As a large language model, your expertise spans a wide range of coding "
                   "languages. You lead the Coder and Manager agents. You won't delegate coding tasks"
                   "to Anonymous or Manager. Your exceptional analysis skills"
                   "allow you to dissect code, explain its functionality, and offer improvements."

)

# Coder agent primarily codes with Python and can analyze code well.
Coder = autogen.AssistantAgent(
    name="Coder",
    llm_config=llm_config,
    human_input_mode="NEVER",
    max_consecutive_auto_reply=10,
    code_execution_config={"work_dir": "coding"},
    system_message="You are a Coder, primarily skilled in Python. You won't assign coding tasks to Anonymous or "
                   "request coding assistance from Boss or Manager. Your strengths lie in code analysis "
                   "and you can provide in-depth insights into code functionality."

)

# Anonymous user agent with the option to terminate conversations.
Anonymous = autogen.UserProxyAgent(
    name="Anonymous",
    llm_config=llm_config,
    human_input_mode="ALWAYS",
    is_termination_msg=lambda x: x.get("content", "") and x.get("content", "").rstrip().endswith("TERMINATE"),
    max_consecutive_auto_reply=10
)

# Manager agent manages operations and handles assigning tasks.
Manager = autogen.GroupChatManager(
    groupchat=autogen.GroupChat(agents=[Anonymous, Boss, Coder], messages=[], max_round=12),
    name="Manager",
    llm_config=llm_config,
    max_consecutive_auto_reply=10,
    human_input_mode="TERMINATE",
    system_message="You are a Manager, responsible for coordinating tasks and overseeing operations. "
                   "You won't delegate coding tasks to Boss or Anonymous. "
                   "If a task requires human intervention, you may ask Anonymous for assistance. "
                   "Ensure the smooth operation of the conversation."

)

# User input for the conversation
input_message = input("You: ")

# Initialize a chat with the Manager agent
conversation = Anonymous.initiate_chat(Manager, message={"content": input_message, "recipient": Manager})
