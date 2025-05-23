

# api/index.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
from datetime import datetime
import random, threading, time, os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Hello, world!"}

@app.get("/api/{item_id}")
def read_item(item_id: int):
    return {"item_id": item_id}

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os

app = FastAPI()

allowed_origins = os.getenv("ALLOWED_ORIGINS", "*").split(",")  # Split in case of multiple origins

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,  # ALLOWED_ORIGINS variable 
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods (GET, POST, etc.)
    allow_headers=["*"],  # Allow all headers
)


class SensorData(BaseModel):
    timestamp: str
    ground_resistance: float
    temperature: float
    fault_status: bool

data_store: List[SensorData] = []

@app.post("/sensor-data/")
def receive_sensor_data(data: SensorData):
    data_store.append(data)
    return {"message": "Data received", "data": data}

@app.get("/sensor-data/", response_model=List[SensorData])
def get_sensor_data():
    return data_store

def generate_sample_data():
    now = datetime.utcnow().isoformat()
    resistance = round(random.uniform(1.0, 10.0), 2)
    temperature = round(random.uniform(15.0, 35.0), 2)
    fault = random.choice([False, True])
    return SensorData(timestamp=now, ground_resistance=resistance, temperature=temperature, fault_status=fault)

def background_data_generator():
    while True:
        data_store.append(generate_sample_data())
        if len(data_store) > 100:
            data_store.pop(0)
        time.sleep(1)

threading.Thread(target=background_data_generator, daemon=True).start()
