import requests


def test_get_pens_check_status_equals_200():
    response = requests.get("http://localhost:8000/api/v1/docs#/shop/list_pens_api_api_v1_pens_get")
    assert response.headers['Content-Type'] == 'text/html; charset=utf-8'
    assert response.status_code == 200

def test_get_pens_check_status_equal_400(mocker):
    #GIVEN
    mock_get = mocker.patch("requests.get")
    mock_get.return_value.status_code = 400
    mock_get.return_value.json.return_value = {}
    #WHEN
    response = requests.get("http://localhost:8000/api/v1/docs#/shop/list_pens_api_api_v1_pens_get")
    #THEN
    assert response.status_code == 400
    mock_get.assert_called_once_with('http://localhost:8000/api/v1/docs#/shop/list_pens_api_api_v1_pens_get')

