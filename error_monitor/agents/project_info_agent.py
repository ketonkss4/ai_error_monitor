from utils.langgraph_utils import create_agent_worker_node


def create_project_information_investagor_agent(gpt_model, tools):

    return create_agent_worker_node(
        llm=gpt_model,
        tools=tools,
        system_prompt='''You are an AI bot in an Error Monitoring System provided with tools to retrieve information 
        about a code project. Your responsibility is to use your provided tools to retrieve the information requested
        by the user in order to diagnose errors in a program or application. Your tools will allow you to files, project
        structure, and execute python code to help you with your investigation.
        '''
    )
