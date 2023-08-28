import os

from dotenv import load_dotenv, dotenv_values

load_dotenv()

config = dotenv_values(".env")

OBJECTS_TO_DETECT = [2, 3, 5, 7] # Cars, motorcycles, buses and trucks
MODEL_PATH=os.getenv("MODEL_PATH")