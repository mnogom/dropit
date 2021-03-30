install:
	poetry install

build:
	poetry build

package-install:
	python3 -m pip install --user dist/*.whl --force-reinstall

lint:
	poetry run flake8 dropit
	poetry run flake8 tests

test:
	poetry run pytest tests/test_drop.py -vv

coverage:
	poetry run pytest --cov=dropit --cov-report xml tests

run:
	poetry run dropit