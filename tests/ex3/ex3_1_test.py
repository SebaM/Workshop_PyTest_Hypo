import requests


def test_get_pens_check_status_equals_200():
    response = requests.get("http://localhost:8000/api/v1/docs#/shop/list_pens_api_api_v1_pens_get")
    assert response.headers['Content-Type'] == 'text/html; charset=utf-8'
    assert response.status_code == 200
