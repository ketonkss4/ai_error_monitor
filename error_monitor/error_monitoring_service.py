import functools

from langchain_core.messages import HumanMessage
from langgraph.constants import END
from langgraph.graph import StateGraph

from error_monitor.agents.code_correction_agent import create_code_correction_agent
from error_monitor.agents.error_processor_agent import create_error_processor_agent
from error_monitor.executors.invoke_corrections_plan import invoke_corrections_plan
from error_monitor.executors.process_error_report import invoke_process_error_report
from error_monitor.state.routers import status_router, edit_router
from error_monitor.state.workflow_state import WorkflowState
from utils.file_tools import get_file_at_path
from utils.gpt_models import GptModels


class ErrorMonitoringService:
    def __init__(self):
        self.gpt_model = GptModels().claude_3
        self.current_state = None

    async def process_error_report(self, error_report_location, report_to_user, update_system_status):
        print(f"Processing error report at location: {error_report_location}")

        error_report = get_file_at_path(error_report_location)

        self.current_state = {
            "error_report": error_report,
            "error_location": error_report_location,
            "messages": [HumanMessage(f"Error Report:\n{error_report}")]
        }
        await report_to_user({"initial_error_report": f"""Received:\n```{error_report}```"""})
        await self.start_workflow(self.current_state, report_to_user, update_system_status)

    async def start_workflow(self, input_state, report_to_user, update_system_status):
        print("Creating workflow...")
        graph = StateGraph(WorkflowState)
        print("State graph created")

        error_processing_agent = create_error_processor_agent(self.gpt_model)
        error_processing_node = functools.partial(invoke_process_error_report, agent=error_processing_agent)
        print("Error processing node created")
        print("User feedback node created")

        error_correcting_agent = create_code_correction_agent(self.gpt_model)
        code_correction_node = functools.partial(invoke_corrections_plan, agent=error_correcting_agent)

        graph.add_node("error_processing", error_processing_node)
        graph.add_node("user_feedback", report_to_user)
        graph.add_node("status_update", update_system_status)
        graph.add_node("edit_code", code_correction_node)

        graph.add_conditional_edges("error_processing", status_router, {
            "FEEDBACK_REQUEST": 'user_feedback',
            "STATUS_UPDATE": "status_update",
        })
        graph.add_edge("user_feedback", "error_processing")
        graph.add_conditional_edges("status_update", edit_router, {
            "CONTINUE": 'edit_code',
            "END": END,
        })
        graph.add_edge("edit_code", "status_update")

        graph.set_entry_point("error_processing")

        workflow = graph.compile()
        print("Starting workflow...")
        async for output in workflow.astream(input_state, debug=True, stream_mode='updates'):
            for key, value in output.items():
                print(f"Output from node '{key}':")
                print("---")

                if isinstance(value, dict) and "messages" in value:
                    print(value["messages"][-1].pretty_print())
                else:
                    print(value)
            print("\n---\n")