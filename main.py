import json
import traceback
import asyncio
from fastapi import FastAPI, HTTPException, Request, WebSocket, BackgroundTasks
from langchain_core.messages import HumanMessage
from error_monitor.error_monitoring_service import ErrorMonitoringService
from starlette.websockets import WebSocketState, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
monitor_service = ErrorMonitoringService()
message_queue = asyncio.Queue()
background_tasks = set()

active_websockets = set()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def startup_event():
    print("Starting background task")
    task = asyncio.create_task(process_queue())
    background_tasks.add(task)
    task.add_done_callback(background_tasks.discard)
    await asyncio.sleep(0)
    print(f"Background tasks: {len(background_tasks)}")


@app.on_event("shutdown")
async def shutdown_event():
    for task in background_tasks:
        task.cancel()
    await asyncio.gather(*background_tasks, return_exceptions=True)


async def report_to_user(state):
    message = None
    if "initial_error_report" in state:
        message = {"type": "error_report", "content": state["initial_error_report"]}
    elif "recommendation" in state:
        print(f"report_to_user - Recommendation: {state['recommendation']}")
        message = {"type": "chat", "content": state["recommendation"][0]["text"]}

    if message:
        # Send the message to all connected WebSockets
        await send_message_to_websockets(message)
        if "initial_error_report" in state:
            return {"messages": [HumanMessage("Error report received")]}
        # Wait for a response from any client
        try:
            response = await asyncio.wait_for(wait_for_client_response(), timeout=300.0)  # 60 second timeout
            if response["type"] == "feedback":
                return {"messages": [HumanMessage(response["content"])],
                        "user_feedback": response["content"]}
            elif response["type"] == "ignore":
                return {"messages": [HumanMessage("IGNORED")]}
            elif response["type"] == "accept":
                return {"messages": [HumanMessage("ACCEPTED")]}
            else:
                print(f"Unknown response type: {response['type']}")
                return {"messages": [HumanMessage("IGNORED")]}
        except asyncio.TimeoutError:
            print("Timeout waiting for client response, defaulting to IGNORE")
            return {"messages": [HumanMessage("IGNORED")]}

    return {"messages": [HumanMessage("IGNORED")]}


async def send_message_to_websockets(message):
    websockets_to_remove = set()
    for websocket in active_websockets:
        try:
            if websocket.application_state == WebSocketState.CONNECTED:
                await websocket.send_json(message)
            else:
                websockets_to_remove.add(websocket)
        except Exception as e:
            print(f"Error sending message to WebSocket: {e}")
            websockets_to_remove.add(websocket)
    active_websockets.difference_update(websockets_to_remove)


async def update_system_status(state):
    status = state.get("status", None)
    message = None
    if status == 'ACCEPTED':
        message = {"type": "status_update",
                   "content": f"Implementing the following plan: {state['correction_plan'][0]['text']}"}
    if status in ['IGNORED', 'CORRECTIONS_COMPLETE']:
        print(f"update_system_status - Message: {state['messages'][-1]}")
        message = {"type": "status_update", "content": state['messages'][-1].content[0]['text']}

    if message:
        print(f"Sending status update: {message}")
        await send_message_to_websockets(message)
        return {"status": "CONTINUE" if status == 'ACCEPTED' else "END"}


async def wait_for_client_response():
    response_future = asyncio.Future()
    await message_queue.put(("wait_response", response_future))
    return await response_future


@app.post("/error-report")
async def receive_error_report(request: Request, background_tasks: BackgroundTasks):
    try:
        payload = await request.json()
        print(f"Received payload: {payload}")
        error_report_location = payload.get("location", "")
        print(f"Error report location: {error_report_location}")

        # Process the error report in the background
        background_tasks.add_task(monitor_service.process_error_report, error_report_location,
                                  report_to_user,
                                  update_system_status)

        return {"message": "Error report received", "location": error_report_location}
    except json.JSONDecodeError:
        raise HTTPException(status_code=400, detail="Invalid JSON")
    except Exception as e:
        error_report = traceback.format_exc()
        print(f"Error: {error_report}")
        raise HTTPException(status_code=500, detail=str(e))


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    active_websockets.add(websocket)
    print(f"WebSocket connection established. Active connections: {len(active_websockets)}")

    try:
        while True:
            data = await websocket.receive_text()
            try:
                message = json.loads(data)
                if message["type"] in ["feedback", "ignore", "accept"]:
                    # This is a response to a previous message
                    await message_queue.put(message)
                else:
                    await websocket.send_json({"type": "error", "content": "Unknown message type"})
            except json.JSONDecodeError:
                await websocket.send_json({"type": "error", "content": "Invalid JSON format"})
    except WebSocketDisconnect:
        print("WebSocket disconnected")
    finally:
        active_websockets.remove(websocket)
        print(f"WebSocket connection closed. Active connections: {len(active_websockets)}")


async def process_queue():
    print("Starting message processing loop")
    while True:
        print("Waiting for message")
        item = await message_queue.get()

        if isinstance(item, tuple) and item[0] == "wait_response":
            response_future = item[1]
            if not response_future.done():
                # Wait for the next message, which should be the response
                response = await message_queue.get()
                if not response_future.done():
                    response_future.set_result(response)
                else:
                    print("Future was completed before setting the result, skipping.")
            else:
                print("Attempted to set result on a done future, skipping.")
        elif isinstance(item, dict):
            # Handle other message types here
            message_type = item.get("type")
            if message_type in ["feedback", "ignore", "accept"]:
                # Process based on the message type
                print(f"Processing message type: {message_type}")
                # Example: You might want to add specific handling for each type
            else:
                print(f"Unknown message type received: {message_type}")
        else:
            print("Received an item of unknown type")

        message_queue.task_done()
