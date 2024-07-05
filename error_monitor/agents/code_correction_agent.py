from error_monitor.tools.tools import get_content_heirarchy_at_path, overwrite_file_at_path, get_file_at_absolute_path
from utils.langgraph_utils import create_agent_worker_node


def create_code_correction_agent(gpt_model):
    return create_agent_worker_node(
        llm=gpt_model,
        tools=[get_content_heirarchy_at_path, overwrite_file_at_path, get_file_at_absolute_path],
        system_prompt='''You are an AI error correction bot in an application monitoring system. Your
                        responsibility is to use the provided tools to implement the code corrections plan 
                        provided by the user.
                        
                        Once you have completed your work, report back a summary of the changes you made
                        that are different from the original code.
                        
                        IMPORTANT: **Remember when implementing changes its best to rewrite the entire file as to not 
                        make whitespace errors always overwrite the entire file to include your changes**
    
                        '''
    )
