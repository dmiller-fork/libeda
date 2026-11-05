.PHONY: run_all

run_all:
	@for file in tests/*.py; do \
		echo "Running $$file"; \
		python3 "$$file"; \
	done
