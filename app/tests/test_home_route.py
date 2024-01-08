from app.main import app
from app.models import *

def test_home_route():
    response = app.test_client().get('/')
    assert response.status_code == 200
    print()

    
    


