install:
	poetry install

build:
	poetry build

package-install:
	python3 -m pip install --user dist/*.whl --force-reinstall

lint:
	poetry run flake8 --config linter-setup.cfg

test:
	poetry run pytest tests/test_drop.py -vv
