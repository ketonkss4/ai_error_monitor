from langchain_core.messages import HumanMessage, AIMessage

from error_monitor.agents.code_validator_agent import create_code_validator_agent
from error_monitor.models.output_models import CorrectionsEval
from utils.gpt_models import GptModels


def invoke_corrections_plan(state, agent, correction_history=None, attempts=0):
    error_report = state["error_report"]
    corrections_plan = state["correction_plan"]
    message_history = state.get("messages")

    if correction_history is None:
        print("Starting Corrections Plan Execution")
        correction_history = []
        corrections_prompt = HumanMessage(f"""
        Error Report:\n{error_report}
        
        Please implement the following correction plan and return a summary of the changes you made
        
        Correction Plan:\n{corrections_plan}
        
        IMPORTANT: **Remember when implementing changes its best to rewrite the entire file as to not make whitespace errors
        always overwrite the entire file to include your changes**
        
        Always respond with markdown. Use the following Post Correction Report Template:
        
        ```
        ## Post Correction Report
        
        ### Files Changes
        - File 1
        - File 2    
        - File 3
        ...
        ### Summary of Changes
        - Change 1
        - Change 2
        
        ### Conclusion
        - Conclusion
        ```
        """)
        message_history.append(corrections_prompt)
        correction_history.append(corrections_prompt)
    else:
        message_history.append(correction_history[-1])

    corrections_result = agent.invoke({"messages": correction_history})

    message_history.append(AIMessage(corrections_result["output"]))
    correction_history.append(AIMessage(corrections_result["output"]))

    if attempts <= 4:
        print(f"Validation Attempt {attempts + 1}")
        validations_agent = create_code_validator_agent(GptModels().claude_3)
        eval_result = validations_agent.invoke({"messages": [HumanMessage(f"""
        The following corrections plan was executed by the previous agent:
        {corrections_plan}
        
        This is the Post Corrections report from the agent:
        {corrections_result["output"]}
        
        Please use the provided tools to verify the changes were made correctly and the code is syntactically correct
        
        if there are any errors please create a list of corrections for the agent to make to amend the mistakes
        
        """)]})

        validation_result = GptModels().claude_3.with_structured_output(CorrectionsEval).invoke([
            HumanMessage(f"""Format the following corrections evaluation:
            {eval_result['output']}
            """)
        ])
        if validation_result.needs_corrections:
            message_history.append(HumanMessage(validation_result.corrections))
            correction_history.append(HumanMessage(validation_result.corrections))
            return invoke_corrections_plan(state, agent, correction_history, attempts + 1)

    print(f"Corrections Complete, Attempts Total: {attempts}")
    return {"status": "CORRECTIONS_COMPLETE", "messages": message_history, "correction_history": correction_history}
