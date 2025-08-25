from fastapi.testclient import TestClient
from app.main import app


client = TestClient(app)

def test_eligibility_pass():
    payload = {
        'income': 60000,
        'age': 30,
        'employment_status': 'employed'
    }
    response = client.post('/loan-eligibility', json=payload)
    assert response.status_code == 200
    assert response.json() == {"eligible": True}


def test_eligibility_fail_underage():
    payload = {
        'income': 60000,
        'age': 18,
        'employment_status': 'employed'
    }
    response = client.post('/loan-eligibility', json=payload)
    assert response.status_code == 200
    assert response.json() == {"eligible": False}


def test_eligibility_fail_low_income():
    payload = {
        'income': 40000,
        'age': 30,
        'employment_status': 'employed'
    }
    response = client.post('/loan-eligibility', json=payload)
    assert response.status_code == 200
    assert response.json() == {"eligible": False}
