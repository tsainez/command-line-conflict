.PHONY: all install test lint format check clean

all: check

install:
	pip install -r requirements.txt

test:
	export SDL_VIDEODRIVER=dummy && pytest --cov=command_line_conflict tests/

lint:
	flake8 .
	pylint $$(git ls-files '*.py')

format:
	black .
	isort .

check: format lint test

clean:
	rm -rf .pytest_cache
	rm -rf .coverage
	rm -rf htmlcov
	find . -type d -name "__pycache__" -exec rm -rf {} +
