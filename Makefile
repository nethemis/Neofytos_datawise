install:
	python -m venv venv/
	source venv/bin/activate
	pip install -r requirements.txt

activate:
	source venv/bin/activate

setup_db:
	python src/setup_db.py


test:
	pytest tests/


run-A1:
	python src/A1.Volumetrics.py

run-A2:
	python src/A2.Conversion_rate.py 

run-B1:
	python src/B.recommendation_system.py 
