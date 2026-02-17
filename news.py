from fastapi import APIRouter

from schemas import NewsImpactRequest

router = APIRouter(prefix="/news", tags=["news"])

POSITIVE_WORDS = {"beats", "growth", "up", "surge", "record", "profit"}
NEGATIVE_WORDS = {"miss", "down", "drop", "lawsuit", "loss", "risk"}


@router.post("/impact")
def impact(req: NewsImpactRequest):
    scored = []
    total = 0.0
    for item in req.news:
        text = f"{item.headline} {item.body or ''}".lower()
        pos = sum(1 for w in POSITIVE_WORDS if w in text)
        neg = sum(1 for w in NEGATIVE_WORDS if w in text)
        score = round((pos - neg) / max(pos + neg, 1), 4)
        total += score
        scored.append({"headline": item.headline, "score": score})

    avg = round(total / max(len(scored), 1), 4)
    label = "neutral" if avg == 0 else ("positive" if avg > 0 else "negative")
    return {"symbol": req.symbol.upper(), "overall": label, "impact_score": avg, "items": scored}
