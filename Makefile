lint: ## Run type checker and linter
	@uv run ruff format
	@uv run ruff check
	@uv run pyrefly check

test: ## Run tests
	@uv run pytest

score: ## Run sentiment scoring on sample data
	@uv run ff-vibes --input data/raw.csv --text-column text --output out.csv