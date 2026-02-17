from fastapi import APIRouter
from v2_backend.schemas import PredictionRequest, PredictionResponse
from v2_backend.services.prediction import explainable_signal

router = APIRouter(prefix="/predictions", tags=["predictions"])

@router.post("/explain", response_model=PredictionResponse)
def explain_prediction(req: PredictionRequest):
    out = explainable_signal(req.prices)
    return PredictionResponse(symbol=req.symbol.upper(), **out)
