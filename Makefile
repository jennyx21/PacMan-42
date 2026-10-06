MAIN = pac-man.py
CONFIG = config.json
LINT_CHECK = src/

install:
	uv sync

run:
	uv run python3 $(MAIN) $(CONFIG)

debug:
	uv run python -m pdb -m src

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	rm -rf .mypy_cache

lint:
	uv run flake8 $(LINT_CHECK)
	uv run mypy --warn-return-any --warn-unused-ignores \
	--ignore-missing-imports --disallow-untyped-defs \
	--check-untyped-defs $(LINT_CHECK)

lint-strict:
	uv run flake8 $(LINT_CHECK)
	uv run mypy --strict $(LINT_CHECK)

re: clean install run

.PHONY: install run debug clean lint lint-strict re
