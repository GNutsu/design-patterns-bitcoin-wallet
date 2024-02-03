all: ## Run all
	make install
	make format
	make lint
	make test

install: ## Install requirements
	python -m pip install -r requirements.txt

format: ## Run code formatters
	python -m isort .
	python -m black .

lint: ## Run code linters
	python -m isort --check .
	python -m black --check .
	python -m flake8 bitcoinwallet tests
	python -m mypy bitcoinwallet tests

test:  ## Run tests with coverage
	python -m pytest --cov