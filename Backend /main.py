from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
from datetime import datetime
import random
import threading
import time
from dotenv import load_dotenv
import os

load_dotenv()  # Load .env file contents into environment variables



# FastAPI app
app = FastAPI()

# Read the ALLOWED_ORIGINS from the environment variable
allowed_origins = os.getenv("ALLOWED_ORIGINS", "").split(",")
print("ALLOWED_ORIGINS:", os.getenv("ALLOWED_ORIGINS"))

# CORS configuration for React frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Data model
class SensorData(BaseModel):
    timestamp: str
    ground_resistance: float
    temperature: float
    fault_status: bool

# In-memory data store
data_store: List[SensorData] = []

# Endpoint to receive posted data (optional)
@app.post("/sensor-data/")
def receive_sensor_data(data: SensorData):
    data_store.append(data)
    return {"message": "Data received", "data": data}

# Endpoint to retrieve all sensor data
@app.get("/sensor-data/", response_model=List[SensorData])
def get_sensor_data():
    return data_store

# Simulate sensor data
def generate_sample_data():
    now = datetime.utcnow().isoformat()
    resistance = round(random.uniform(1.0, 10.0), 2)
    temperature = round(random.uniform(15.0, 35.0), 2)
    fault = random.choice([False, False,True, False, True])  # Fault occurs occasionally
    return SensorData(timestamp=now, ground_resistance=resistance, temperature=temperature, fault_status=fault)

# Background thread to generate new data every second
def background_data_generator():
    while True:
        data_store.append(generate_sample_data())
        # Limit size (e.g., keep last 100 points)
        if len(data_store) > 100:
            data_store.pop(0)
        time.sleep(1)

# Start background thread
threading.Thread(target=background_data_generator, daemon=True).start()
