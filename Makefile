.PHONY: validate test-python test-node

validate:
	bash scripts/validate_all.sh

test-python:
	python3 -m pytest -q agent-runtime/tests

test-node:
	cd control-plane && npm test
