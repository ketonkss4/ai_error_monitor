def status_router(state):
    status = state["status"]
    if status == "FEEDBACK":
        return "FEEDBACK_REQUEST"
    return "STATUS_UPDATE"


def edit_router(state):
    status = state["status"]
    if status == "CONTINUE":
        return "CONTINUE"
    return "END"
