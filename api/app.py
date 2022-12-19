import mlflow 
import uvicorn
import pandas as pd 
from pydantic import BaseModel
from typing import Literal, List, Union
from fastapi import FastAPI, File, UploadFile
import joblib

description = """
Welcome to  API.  Try it out 🕹️

## Introduction Endpoints


"""

tags_metadata = [
    {
        "name": "Introduction Endpoints",
        "description": "Simple endpoints to try out!",
    },
    {
        "name": "Machine Learning",
        "description": "Prediction Endpoint."
    }
]

app = FastAPI(
    title="GetAround",
    description=description,
    version="0.1",
    contact={
        "name": "GetAround",
        "url": "https://GetAround.com",
    },
    openapi_tags=tags_metadata
)

class DescriptionVehicule(BaseModel):
    marque: str
    kilometrage: int
    puissance: int
    energie: str
    car_type: str
    parking_private: bool 
    gps: bool 
    air_conditionning: bool 
    automatic: bool 
    getaround_connect: bool 
    speed_regulator: bool 
    winter_tires: bool 


@app.get("/", tags=["Introduction Endpoints"])
async def index():
    """
    Renvoie simplement un message de bienvenue !
    """
    message = "Bonjour! Ce `/` est le point de terminaison le plus simple et par défaut. Si vous voulez en savoir plus, consultez la documentation de l'API sur `/docs`"
    return message

@app.post("/predict", tags=["Machine Learning"])
async def predict(price_day: DescriptionVehicule):
    """
    Prediction of salary for a given year of experience! 
    """
    # Read data 
    price_day = pd.DataFrame({
                            "model_key": [price_day.marque],
                            "mileage": [price_day.kilometrage],
                            "engine_power": [price_day.puissance],
                            "fuel": [price_day.energie],
                            "car_type": [price_day.car_type],
                            "private_parking_available": [price_day.parking_private],
                            "has_gps": [price_day.gps],
                            "has_air_conditioning": [price_day.air_conditionning],
                            "automatic_car": [price_day.automatic],
                            "has_getaround_connect": [price_day.getaround_connect],
                            "has_speed_regulator": [price_day.speed_regulator],
                            "winter_tires": [price_day.winter_tires]
    })

    # Log model from mlflow 
    logged_model = 'runs:/eb5e512da4414cc280c92b50330d6328/my-first-mlflow-experiment'

    # Load model as a PyFuncModel.
    loaded_model = mlflow.pyfunc.load_model(logged_model)

    # If you want to load model persisted locally
    #loaded_model = joblib.load('salary_predictor/model.joblib')

    prediction = loaded_model.predict(price_day)

    # Format response
    response = {"prediction": prediction.tolist()[0]}
    return response


if __name__=="__main__":
    uvicorn.run(app, host="0.0.0.0", port=4000)