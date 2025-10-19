# app/main.py
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import pickle
import os


MODEL_PATH = os.environ.get('MODEL_PATH', 'models/new_model/model.pkl')


app = FastAPI(title='Model Serving (demo)')


class Item(BaseModel):
    text: str


# load model at startup
try:
    with open(MODEL_PATH, 'rb') as f:
        model = pickle.load(f)
except Exception:
    model = None


@app.get('/health')
def health():
    return {"status": "ok"}


@app.post('/predict')
def predict(item: Item):
    global model
    if model is None:
        raise HTTPException(status_code=503, detail='Model not loaded')
    pred = model.predict([item.text])[0]
    prob = None
    try:
        prob = float(model.predict_proba([item.text])[0].max())
    except Exception:
        pass
    return {"prediction": int(pred), "confidence": prob}