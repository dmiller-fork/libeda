.PHONY: run_all freeze

run_all:
	@for file in tests/*.py; do \
		echo "Running $$file"; \
		python3 "$$file"; \
	done

freeze:
	python -m pip freeze > requirements.txt
