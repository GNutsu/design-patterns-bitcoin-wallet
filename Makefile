all: ## Run all
	make install
	make format
	make lint
	make test

install: ## Install requirements
	python -m pip install -r requirements.txt

format: ## Run code formatters
	python3 -m isort .
	python3 -m black .

lint: ## Run code linters
	python3 -m isort --check .
	python3 -m black --check .
	python3 -m flake8 bitcoinwallet tests
	python3 -m mypy bitcoinwallet tests

test:  ## Run tests with coverage
	python3 -m pytest --cov