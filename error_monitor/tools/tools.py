import os
from langchain_core.tools import tool
from typing import Annotated

from error_monitor.agents.project_info_agent import create_project_information_investagor_agent
from utils.file_tools import retrieve_directory_contents_hierarchy, get_file_at_path
from utils.gpt_models import GptModels
from langchain_core.messages import HumanMessage
from langchain_experimental.utilities import PythonREPL
from langchain_core.tools import Tool


@tool
def get_file_at_absolute_path(
        absolute_file_path: Annotated[str, 'This is the absolute path to the file you want to read']):
    """
    Get the contents of a file at a given path
    absolute_file_path: str: This is the absolute path to the file you want to read
    """
    os_system_type = os.name
    try:
        return get_file_at_path(absolute_file_path)
    except FileNotFoundError:
        return f"""The file at {absolute_file_path} was not found. Please reconsider your search path
        and try again. The system you are using is {os_system_type}."""


@tool
def overwrite_file_at_path(
        absolute_file_path: Annotated[str, 'This is the absolute path to the file you want to overwrite'],
        new_content: Annotated[str, 'The new content you want to write to the file']):
    """
    Overwrite the contents of a file at a given path
    absolute_file_path: str: This is the absolute path to the file you want to overwrite
    new_content: str: The new content you want to write to the file
    """
    os_system_type = os.name
    try:
        with open(absolute_file_path, 'w') as file:
            file.write(new_content)
        return f"""The file at {absolute_file_path} was overwritten successfully. The system you are using is 
        {os_system_type}."""
    except FileNotFoundError:
        return f"""The file at {absolute_file_path} was not found. Please reconsider your search path
        and try again. The system you are using is {os_system_type}."""


@tool
def get_content_heirarchy_at_path(
        absolute_path: Annotated[str, 'This is the absolute path to the directory you want to search'],
        include_files: Annotated[bool, 'Whether to include files in the search'] = False):
    """
    Get the contents of a directory at a given path
    absolute_path: str: This is the absolute path to the directory you want to search
    include_files: bool: Whether to include files in the search
    """
    os_system_type = os.name

    # Check if absolute path is pointing to a file instead of a directory
    if os.path.isfile(absolute_path):
        return f"""The path provided is a file. Please provide a path to a directory instead. The system you are using 
        is {os_system_type}."""

    try:
        return retrieve_directory_contents_hierarchy(absolute_path, include_files=include_files)
    except FileNotFoundError:
        return f"""The directory at {absolute_path} was not found. Please reconsider your search path
        and try again. The system you are using is {os_system_type}."""


@tool
def request_project_information(info_request: Annotated[
    str, 'A description of the additional information you need from the project of the code'],
                                project_directory_path: Annotated[
                                    str, 'The absolute path to the project directory you want to search'],
                                additional_contenxt: Annotated[
                                    str, 'Additional context to help with finding the information you are seeking'] = ''):
    """
    Request information about a project
    info_request: str: The information you want to retrieve about the project
    """
    python_repl = PythonREPL()
    repl_tool = Tool(
        name="python_repl",
        description="A Python shell. Use this to execute python commands. Input should be a valid python command. If "
                    "you want to see the output of a value, you should print it out with `print(...)`.",
        func=python_repl.run,
    )
    agent = create_project_information_investagor_agent(GptModels().gpt_4_omni,
                                                        tools=[get_content_heirarchy_at_path,
                                                               get_file_at_absolute_path,
                                                               repl_tool])

    result = agent.invoke({"messages": [HumanMessage(f"""
    Information Request:
    {info_request}
    
    Use the tools to get the contents hierarchy of the following to assist you with your search
    Project Directory Path:
    {project_directory_path}
    
    
    Use the following additional context to help with your search (if there's any):
    {additional_contenxt}
    
    """)]})

    return result['output']
