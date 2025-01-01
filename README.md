#### Demo website
This for demo sql injection attack for assigment 2 of INTE2634

#### How to run
1. Clone this repository
2. Run 
Using python 3.12
```
python3 -m venf .venv
source .venv/bin/activate
pip install -r requirements.txt
python app.py
```
Or using docker compose
```
docker-compose up -d
```
4. Open browser and go to `http://localhost:8080/`

5. The vulnerable page is `http://localhost:8080/vuln?usesrname=admin`