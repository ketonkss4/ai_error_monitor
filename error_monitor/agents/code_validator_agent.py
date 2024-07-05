from langchain_core.tools import Tool
from langchain_experimental.utilities import PythonREPL

from error_monitor.tools.tools import get_file_at_absolute_path
from utils.langgraph_utils import create_agent_worker_node


def create_code_validator_agent(gpt_model):
    python_repl = PythonREPL()
    repl_tool = Tool(
        name="python_repl",
        description="A Python shell. Use this to execute python commands. Input should be a valid python command. If "
                    "you want to see the output of a value, you should print it out with `print(...)`.",
        func=python_repl.run,
    )
    return create_agent_worker_node(
        llm=gpt_model,
        tools=[get_file_at_absolute_path],
        system_prompt='''You are an AI error correction validation bot in an application monitoring system. Your
                        responsibility is to use the provided tools to determine whether the code corrections made by
                        the previous agent has been made correctly and there are no syntax or logic errors. 
                        
                        If there is any errors you must create a list of correction instructions for the previous agent to
                        amend its mistakes. 
                        '''
    )
