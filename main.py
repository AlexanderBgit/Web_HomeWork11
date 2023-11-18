from fastapi import FastAPI, Request
import time

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

from src.routes import contacts
# from src.routes.contacts import contacts

app = FastAPI()

# @app.middleware("http") # on future
# async def add_process_time_header(request: Request, call_next):
#     start_time = time.time()
#     response = await call_next(request)
#     process_time = time.time() - start_time
#     response.headers["My-Process-Time"] = str(process_time)
#     return response


app.include_router(contacts.router, prefix='/api')


@app.get("/")
def read_root():
    return {"message": "That's root"}