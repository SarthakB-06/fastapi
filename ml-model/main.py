from fastapi import FastAPI
from schemas import InputSchema, OutputSchema
from predict import make_prediction


app = FastAPI()


@app.get('/')
def read_root():
    return {"message": "Welcome to the ML Model API"}


@app.post('/predict' , response_model=OutputSchema)
def predict(input_data : InputSchema):
    prediction = make_prediction(input_data.model_dump())
    return OutputSchema(predicted_price=prediction)

