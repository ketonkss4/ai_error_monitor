from langchain_core.messages import SystemMessage, HumanMessage, AIMessage


def invoke_process_error_report(state, agent):
    error_report = state["error_report"]
    user_feedback = state.get("user_feedback", None)
    latest_message = state['messages'][-1].content
    conversation_history = state.get("recommendation_conversation_history", None)

    if latest_message == 'IGNORED':
        return {"status": "IGNORED", "messages": [HumanMessage("Understood, will standby for the next error report")]}
    if conversation_history is None or len(conversation_history) == 0:
        conversation_history = [
            HumanMessage(f"""
                         Error Report:\n{error_report}
                         
                         Use the following template as a guideline for your corrections proposal once you
                         have reviewed the error and have enough information to make a recommendation:
                            
                         ```
                         ## Corrections Proposal
                         
                         ### Error Summary
                            - Error Summary
                            
                         ### Correction Recommendations
                            - Recommendation 1
                            - Recommendation 2
                            
                        ### Files to edit
                            - File 1
                            - File 2
                            
                        ### Potential Risks [Optional]
                            - Risk 1
                            - Risk 2
                        ```
                         """)
        ]
    else:
        if not latest_message == 'ACCEPTED':
            conversation_history.append(HumanMessage(f"""
                            User Feedback:\n{user_feedback}
                            
                            Please respond in correctly formatted markdown text. 
                            """))
        else:
            conversation_history.append(HumanMessage("""The user has accepted the recommendation. Prepare the final action plan for the
                                                     developers to fix the error. The plan should be in markdown format have an instructional 
                                                     tone and include code snippets to show the changes that need to be made step by step.
                                                     Be sure to call out the specific files in the project that should be edited to make the corrections.
                                                     
                                                     
                                                     Use the following template as a guideline to create your final action plan:
                                                     
                                                     ```
                                                        ## Action Plan
                                                        
                                                        ### Brief Summary of Error
                                                        - Error Summary
                                                        
                                                        ### Steps to Correct Error
                                                        - Step 1
                                                        - Step 2
                                                        ...
                                                        
                                                        ### Files to Edit
                                                        - File 1
                                                        - File 2
                                                        
                                                        
                                                        ### Potential Risks
                                                        - Risk 1
                                                        - Risk 2
                                                        
                                                        ### Additional Considerations (Optional)
                                                        - Consideration 1
                                                        - Consideration 2
                                                        
                                                    ```
                                                        
                                                     """))
    ai_response = agent.invoke({"messages": conversation_history})
    conversation_history.append(AIMessage(ai_response["output"]))
    print(f"AI Response: {ai_response['output']}")
    if latest_message == 'ACCEPTED':
        return {"status": "ACCEPTED", "messages": conversation_history, "correction_plan": ai_response["output"]}
    return {"status": "FEEDBACK", "recommendation_conversation_history": conversation_history,
            "recommendation": ai_response["output"]}
