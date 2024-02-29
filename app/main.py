from dotenv import load_dotenv
load_dotenv()
from datetime import datetime
from sqlalchemy.orm import Session
from fastapi import FastAPI, WebSocket, Depends, HTTPException, status
from app.dependencies import get_current_user, get_db, sget_current_user
from typing import Annotated
from app.schemas.user import User
from app.database import crud
from app.routers import chat, chat_session, vector_store, conn_params
from app.internal import auth
from fastapi.middleware.cors import CORSMiddleware
from app.database.base import Base, engine
import socketio
import json
import os
from app.core.mock import MockQueryEngine

Base.metadata.create_all(bind=engine)

async def generate_query(token, session_id, user_query, sid):
    db_generator = get_db()
    db = next(db_generator)
    current_user = sget_current_user(token, db)

    creds = crud.get_user_db_creds(db=db, user_id=current_user.id)
    if creds is None:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid token or credentials")

    query_engine = MockQueryEngine()
    response = query_engine.query(user_query)
    print(response)

    await sio.emit('message', json.dumps({"aa_text": aa_text}), room=sid)
    await sio.emit('message', json.dumps({"sql_query": sql_query}), room=sid)
    await sio.emit('message', json.dumps({"dataframe": dataframe}), room=sid)
    await sio.emit('message', json.dumps({"plot_code": html_plot_js}), room=sid)
    
app = FastAPI()
sio = socketio.AsyncServer(async_mode='asgi', cors_allowed_origins="*")
socketio_app = socketio.ASGIApp(sio)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(chat_session.router, prefix="/chat_session", tags=["chat_session"])
app.include_router(chat.router, tags=["chat"])
app.include_router(vector_store.router, prefix="/vector_store", tags=["vector_store"])
app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(conn_params.router, prefix="/conn-params", tags=["connection parameters"])

@app.get("/", tags=["root"])
async def root():
    return {"app": f"{os.getenv('APP_NAME')}"}

@sio.event
async def connect(sid, environ):
    print('connect ', sid)
    await sio.emit('message', 'Connected to the server!', room=sid)  # Emit a message to the connected client

@sio.event
async def disconnect(sid):
    print('disconnect ', sid)

@sio.event
async def message(sid, data):
    json_data = json.loads(data)
    user_query = json_data.get('user_query')
    session_id = json_data.get('sessionId')
    token = json_data.get('token')
    
    await generate_query(token, session_id, user_query, sid)

app.mount('/socket.io', socketio_app)