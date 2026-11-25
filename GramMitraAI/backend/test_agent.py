import os,tempfile
os.environ['DB_PATH']=tempfile.mktemp(suffix='.db');os.environ.pop('OPENAI_API_KEY',None)
from fastapi.testclient import TestClient
from unittest.mock import patch,AsyncMock
from main import app
client=TestClient(app)
def test_workflow():
    with patch('main.locate',AsyncMock(return_value={'name':'Vijayawada','admin1':'Andhra Pradesh','latitude':16.5,'longitude':80.6})),patch('main.weather',AsyncMock(return_value={'daily':{'time':['2026-11-25'],'precipitation_probability_max':[70],'precipitation_sum':[12]}})):
        r=client.post('/api/agent',json={'goal':'Plan field work','location':'Vijayawada'});assert r.status_code==200; data=r.json();assert len(data['trace'])==5;assert data['resources'];assert client.post('/api/feedback',json={'run_id':data['id'],'helpful':True}).status_code==200;assert client.get('/api/metrics').json()['helpful']==1
def test_failure():
    with patch('main.locate',AsyncMock(side_effect=ValueError('Unknown town'))):
        r=client.post('/api/agent',json={'goal':'Plan field work','location':'unknown','language':'te'});assert r.status_code==200;assert r.json()['weather'] is None;assert any(x['status']=='failed' for x in r.json()['trace'])
def test_validation(): assert client.post('/api/agent',json={'goal':'x','location':'a'}).status_code==422
