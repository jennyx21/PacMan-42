PYTHON = python3
MAIN = pac-man.py
CONFIG = config.json
LINT_CHECK = src/

install:
	uv sync

run:
	uv run $(PYTHON) $(MAIN) $(CONFIG)

debug:
	uv run $(PYTHON) -m pdb $(MAIN) $(CONFIG)

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type d -name ".mypy_cache" -exec rm -rf {} +

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
