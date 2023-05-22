import pytest
from bs4 import BeautifulSoup

def test_home_page_with_fixture(test_client):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/' page is requested (GET)
    THEN check that the response is valid
    """
    response = test_client.get('/')
    assert response.status_code == 200
    
def test_about_page_with_fixture(test_client):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/about' page is requested (GET)
    THEN check that the response is valid
    """
    response = test_client.get('/about')
    assert response.status_code == 200

def test_search_game_with_fixture(test_client):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/search' page is requested with a valid search term (POST)
    THEN check that the response returns the valid list template
    """
    response = test_client.post('/search', data={'search_term': 'Apex Legends'})
    assert response.status_code == 200
    assert b'Apex Legends' in response.data
    
def test_search_empty_with_fixture(test_client):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/search' page is requested with an invalid empty search term (POST)
    THEN check that the response returns the error message
    """
    response = test_client.post('/search', data={'search_term': ''})
    assert response.status_code == 200
    soup = BeautifulSoup(response.data, 'html.parser')
    error_container = soup.find('div', class_='error_container')
    error_message = error_container.p.text.strip()
    expected_message = "The search term can't be empty!"
    assert expected_message == error_message
  
def test_home_page_post_with_fixture(test_client):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/' page is posted to (POST)
    THEN check that a '405' (Method Not Allowed) status code is returned
    """
    response = test_client.post('/')
    assert response.status_code == 405

def test_find_gpu_valid_id_with_fixture(test_client):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/find_gpu' page is requested with valid data (POST)
    THEN check that the response returns a the valid game
    """
    response = test_client.post('/find_gpu', data={'game_id': '114795'})
    assert response.status_code == 200
    assert b'Apex Legends' in response.data  # Replace 'Game Name' with an expected game name
    
