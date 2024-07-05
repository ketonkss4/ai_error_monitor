import operator
from typing import TypedDict

from langchain_core.messages import BaseMessage
from typing_extensions import Annotated, Sequence


class WorkflowState(TypedDict):
    messages: Annotated[Sequence[BaseMessage], operator.add]
    error_report: str
    error_location: str
    recommendation_conversation_history: Annotated[Sequence[BaseMessage], operator.add]
    correction_history: Annotated[Sequence[BaseMessage], operator.add]
    recommendation: dict
    status: str
    correction_plan: str
