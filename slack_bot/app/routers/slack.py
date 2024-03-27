import os
from app.utils.analitque import create_chat_session, create_user, get_chat_session, post_query
from app.utils.slack_api import post_message
from fastapi import APIRouter, Header, HTTPException, BackgroundTasks
from typing import List, Optional
from pydantic import BaseModel, Field

router = APIRouter()

class SlackEvent(BaseModel):
    token: str
    challenge: Optional[str] = Field(None)
    type: str
    team_id: str
    context_team_id: Optional[str]
    context_enterprise_id: Optional[str]
    api_app_id: str
    event: dict
    event_id: str
    event_time: int
    authorizations: List[dict]
    is_ext_shared_channel: bool
    event_context: str

@router.get("/check")
async def check_health():
    return "Slack app backend is up and running!"

@router.post("/event")
async def handle_slack_event(slack_event: SlackEvent, background_tasks: BackgroundTasks, x_slack_signature: str = Header(...), x_slack_request_timestamp: str = Header(...)):
    # Implement your verification logic here
    print("handle_slack_event")
    if slack_event.type == "url_verification":
        if not slack_event.challenge:
            raise HTTPException(status_code=400, detail="Challenge field is required for URL verification")
        return {"challenge": slack_event.challenge}
    elif slack_event.type == "event_callback":
        # Check if the event is a message event
        if slack_event.event["type"] == "message":
            # Check if the message is not from a bot
            if "bot_id" not in slack_event.event:
                # Enqueue processing of message in background
                background_tasks.add_task(process_message, slack_event.event)
                return {"message": "Processing message in background"}
    else:
        return {"message": "Event type not supported"}


def process_message(event: dict):
    # Implement your message processing logic here
    print("Message from user")
    print(event)
    chat_sessions = get_chat_session(chat_name=event["user"])
    # Check that chat_sessions is not None and not an empty list
    if not chat_sessions:
        chat_sessions = create_chat_session(chat_name=event["user"])
    if not chat_sessions:
        raise HTTPException(status_code=500, detail="Failed to create chat session")
    chat_session = chat_sessions[0]
    response_to_query = post_query(chat_session_id=chat_session["id"], query=event["text"])
    if not response_to_query:
        raise HTTPException(status_code=500, detail="Failed to post query")
    post_message(bot_token=os.environ.get("SLACK_BOT_TOKEN"), sink=event["user"], text=response_to_query["text"])