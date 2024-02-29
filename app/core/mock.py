import asyncio
import time
import json
from fastapi import FastAPI, WebSocket
import socketio

# Mock query engine to simulate async responses
class MockQueryEngine:
    def query(self, query):
        # Simulate different response times and responses based on the query
        print(query)
        if "fast" in query:
            time.sleep(1)  # Simulate a fast response
            return {"response": "Fast query response", "query": query}
        elif "medium" in query:
            time.sleep(2)  # Simulate a medium response
            return {"response": "Medium query response", "query": query}
        else:
            time.sleep(3)  # Simulate a slow response
            return {"response": "Slow query response", "query": query}

    async def aquery(self, query):
        # Simulate different response times and responses based on the query
        print(query)
        if "fast" in query:
            await asyncio.sleep(1)  # Simulate a fast response
            return {"response": "Fast query response", "query": query}
        elif "medium" in query:
            await asyncio.sleep(2)  # Simulate a medium response
            return {"response": "Medium query response", "query": query}
        else:
            await asyncio.sleep(3)  # Simulate a slow response
            return {"response": "Slow query response", "query": query}

