import pytest
from unittest.mock import patch

@patch('api.chat.requests.post')
def test_responder_ok(mock_post, client):
    mock_post.return_value.status_code = 200
    mock_post.return_value.json.return_value = {'message': 'Hola, soy el bot'}
    response = client.post('/chat/send-message', json={'message': 'Hola'})
    assert response.status_code == 200
    assert response.get_json()['message'] == 'Hola, soy el bot'

@patch('api.chat.requests.post', side_effect=Exception('Error externo'))
def test_responder_error(mock_post, client):
    with pytest.raises(Exception) as excinfo:
        client.post('/chat/send-message', json={'message': 'Hola'})
    assert 'Error externo' in str(excinfo.value) 