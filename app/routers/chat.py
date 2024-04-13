from typing import Annotated
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, WebSocket, Form, HTTPException, status
from app.database import crud
from app.schemas.user import User
from app.dependencies import get_current_user, get_db, sget_current_user
from app.schemas.chat_feedback import ChatFeedback, ChatFeedbackCreate, UserRatingEnum
from app.core.mock import MockQueryEngine
from app.schemas.chat_session import ChatMessage

router = APIRouter()

@router.post("/{session_id}/query")
async def execute_user_query(
    session_id: str,
    current_user: Annotated[User, Depends(get_current_user)],
    db: Annotated[Session, Depends(get_db)],
    user_query: Annotated[str, Form(example="This is a test message")],
):

    print("should await for query execution")
    query_engine = MockQueryEngine()
    result = query_engine.query(user_query)

    aa_text = result.get("response")
    sql_query = result.get("response")
    dataframe = result.get("response")
    plot_code = result.get("response")
    crud.add_message_to_chat_session_history(db=db, chat_history=ChatMessage(**message_info, message_type="aa", message_content=sql_query, content_type="sql"))

    return {
        "session_id": session_id,
        "user_id": current_user.id,
        "message_type": "aa",
        "text": aa_text,
        "sql_query": sql_query,
        "dataframe": dataframe,
        "plot_code": plot_code,
    }

@router.post("/{history_id}/feedback", response_model=ChatFeedback)
async def create_chat_feedback(
    db: Annotated[Session, Depends(get_db)],
    history_id: int,
    session_id: Annotated[str, Form()],
    user_prompt: Annotated[str, Form()],
    aa_response: Annotated[str, Form()],
    user_rating: Annotated[UserRatingEnum, Form(examples=['good', 'bad'])],
    user_comment: Annotated[str, Form()]
):

    """
    param history_id: chat history ID (path parameter)  
    param db: Database session (dependencies)
    """

    chat_feedback = ChatFeedbackCreate(
        history_id = history_id,
        session_id = session_id,
        user_prompt=user_prompt,
        aa_response=aa_response,
        user_rating=user_rating,
        user_comment=user_comment
    )

    return crud.create_feedback(db=db, chat_feedback=chat_feedback)