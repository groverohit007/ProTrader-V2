from fastapi import APIRouter
from schemas import PredictionRequest, PredictionResponse
from prediction import explainable_signal

router = APIRouter(prefix="/predictions", tags=["predictions"])

@router.post("/explain", response_model=PredictionResponse)
def explain_prediction(req: PredictionRequest):
    out = explainable_signal(req.prices)
    return PredictionResponse(symbol=req.symbol.upper(), **out)
