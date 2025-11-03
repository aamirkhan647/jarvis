.PHONY: run test clean install

install:
	pip install -r requirements.txt

run:
	python -m jobtailor.app

test:
	pytest -v jobtailor/tests

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -name "*.pyc" -delete
	rm -rf .pytest_cache build dist *.egg-info
