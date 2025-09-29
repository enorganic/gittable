SHELL := bash
.PHONY: docs
MINIMUM_PYTHON_VERSION := 3.9

# Create all environments
install:
	{ hatch --version || pipx install --upgrade hatch || python3 -m pip install --upgrade hatch ; } && \
	{ poetry --version || pipx install --upgrade poetry || python3 -m pip install --upgrade poetry ; } && \
	hatch env create default && \
	hatch env create docs && \
	hatch env create hatch-static-analysis && \
	hatch env create hatch-test && \
	echo "Installation complete"

# Re-create all environments, from scratch (no reference to pinned
# requirements)
reinstall:
	{ hatch --version || pipx install --upgrade hatch || python3 -m pip install --upgrade hatch ; } && \
	{ poetry --version || pipx install --upgrade poetry || python3 -m pip install --upgrade poetry ; } && \
	hatch env prune && \
	make && \
	make requirements

distribute:
	hatch build && hatch publish && rm -rf dist

# This will upgrade all requirements, and refresh pinned requirements to
# match. The same can be accomplished with `make reinstall`, but this
# runs faster, because environments are not recreated.
upgrade:
	hatch run dependence upgrade\
	 --include-pointer /tool/hatch/envs/default\
	 --include-pointer /project\
	 pyproject.toml && \
	hatch run docs:dependence upgrade\
	 --include-pointer /tool/hatch/envs/docs\
	 --include-pointer /project\
	 pyproject.toml && \
	hatch run hatch-static-analysis:dependence upgrade\
	 --include-pointer /tool/hatch/envs/hatch-static-analysis\
	 --include-pointer /project\
	 pyproject.toml && \
	hatch run hatch-test.py$(MINIMUM_PYTHON_VERSION):dependence upgrade\
	 --include-pointer /tool/hatch/envs/hatch-test\
	 --include-pointer /project\
	 pyproject.toml

# This will update pinned requirements to align with the
# package versions installed in each environment, and will align the project
# dependency versions with those installed in the default environment
requirements:
	hatch run dependence update\
	 --include-pointer /tool/hatch/envs/default\
	 --include-pointer /project\
	 pyproject.toml && \
	hatch run docs:dependence update pyproject.toml --include-pointer /tool/hatch/envs/docs && \
	hatch run hatch-test.py$(MINIMUM_PYTHON_VERSION):dependence update pyproject.toml --include-pointer /tool/hatch/envs/hatch-test && \
	hatch run hatch-static-analysis:dependence update pyproject.toml --include-pointer /tool/hatch/envs/hatch-static-analysis && \
	echo "Requirements updated"

# Test & check linting/formatting (for local use only)
test:
	{ hatch --version || pipx install --upgrade hatch || python3 -m pip install --upgrade hatch ; } && \
	{ poetry --version || pipx install --upgrade poetry || python3 -m pip install --upgrade poetry ; } && \
	hatch fmt --check && hatch run mypy && hatch test -c

format:
	hatch fmt --formatter
	hatch fmt --linter
	hatch run mypy && \
	echo "Format Successful!"

docs:
	hatch run docs:mkdocs build && \
	hatch run docs:mkdocs serve

# Cleanup untracked files
clean:
	git clean -f -e .vscode -e .idea -x .
