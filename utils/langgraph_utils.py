from langchain.agents import create_openai_tools_agent, AgentExecutor
from langchain_anthropic import ChatAnthropic
from langchain_core.language_models import BaseChatModel
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder


from typing import Sequence

from langchain.agents.format_scratchpad.openai_tools import (
    format_to_openai_tool_messages,
)
from langchain.agents.output_parsers.openai_tools import OpenAIToolsAgentOutputParser
from langchain_anthropic import ChatAnthropic
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import Runnable, RunnablePassthrough
from langchain_core.tools import BaseTool


def create_claude_tools_agent(
        llm: ChatAnthropic, tools: Sequence[BaseTool], prompt: ChatPromptTemplate
) -> Runnable:
    """Create an agent that uses OpenAI tools.

    Args:
        llm: LLM to use as the agent.
        tools: Tools this agent has access to.
        prompt: The prompt to use. See Prompt section below for more on the expected
            input variables.

    Returns:
        A Runnable sequence representing an agent. It takes as input all the same input
        variables as the prompt passed in does. It returns as output either an
        AgentAction or AgentFinish.

    Example:

        .. code-block:: python

            from langchain import hub
            from langchain_community.chat_models import ChatOpenAI
            from langchain.agents import AgentExecutor, create_openai_tools_agent

            prompt = hub.pull("hwchase17/openai-tools-agent")
            model = ChatOpenAI()
            tools = ...

            agent = create_openai_tools_agent(model, tools, prompt)
            agent_executor = AgentExecutor(agent=agent, tools=tools)

            agent_executor.invoke({"input": "hi"})

            # Using with chat history
            from langchain_core.messages import AIMessage, HumanMessage
            agent_executor.invoke(
                {
                    "input": "what's my name?",
                    "chat_history": [
                        HumanMessage(content="hi! my name is bob"),
                        AIMessage(content="Hello Bob! How can I assist you today?"),
                    ],
                }
            )

    Prompt:

        The agent prompt must have an `agent_scratchpad` key that is a
            ``MessagesPlaceholder``. Intermediate agent actions and tool output
            messages will be passed in here.

        Here's an example:

        .. code-block:: python

            from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

            prompt = ChatPromptTemplate.from_messages(
                [
                    ("system", "You are a helpful assistant"),
                    MessagesPlaceholder("chat_history", optional=True),
                    ("human", "{input}"),
                    MessagesPlaceholder("agent_scratchpad"),
                ]
            )
    """
    missing_vars = {"agent_scratchpad"}.difference(
        prompt.input_variables + list(prompt.partial_variables)
    )
    if missing_vars:
        raise ValueError(f"Prompt missing required variables: {missing_vars}")

    llm_with_tools = llm.bind_tools(tools=tools)

    agent = (
            RunnablePassthrough.assign(
                agent_scratchpad=lambda x: format_to_openai_tool_messages(
                    x["intermediate_steps"]
                )
            )
            | prompt
            | llm_with_tools
            | OpenAIToolsAgentOutputParser()
    )
    return agent


def create_agent_worker_node(
        llm: BaseChatModel, tools: list, system_prompt: str
):
    # Each worker node will be given a name and some tools.
    prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                system_prompt,
            ),
            MessagesPlaceholder(variable_name="messages"),
            MessagesPlaceholder(variable_name="agent_scratchpad"),
        ]
    )
    # check if llm is instance of type ChatAnthropic
    if isinstance(llm, ChatAnthropic):
        agent = create_claude_tools_agent(llm, tools, prompt)
        print("Claude Agent Worker Node Created")
    else:
        agent = create_openai_tools_agent(llm, tools, prompt)
        print("OpenAI Agent Worker Node Created")
    executor = AgentExecutor(agent=agent, tools=tools, max_iterations=50, verbose=True)
    print("Agent Worker Node Created")
    return executor

