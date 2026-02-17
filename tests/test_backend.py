import os
import sys

from fastapi.testclient import TestClient

sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from main import app


client = TestClient(app)


def test_health():
    response = client.get('/health')
    assert response.status_code == 200
    assert response.json()['status'] == 'ok'


def test_prediction_endpoint():
    prices = [100 + i for i in range(30)]
    response = client.post('/predictions/explain', json={'symbol': 'AAPL', 'prices': prices})
    assert response.status_code == 200
    data = response.json()
    assert data['signal'] in {'BUY', 'HOLD', 'SELL'}


def test_quote_endpoint():
    response = client.get('/market/quote/AAPL')
    assert response.status_code == 200
    assert response.json()['symbol'] == 'AAPL'
