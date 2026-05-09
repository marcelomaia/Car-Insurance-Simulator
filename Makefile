.PHONY: coverage coverage-clean coverage-html coverage-xml

# Full report: terminal + Cobertura XML (Sonar) + HTML site under htmlcov/
coverage:
	python -m pytest \
		--cov=domain \
		--cov=scripts \
		--cov-report=term-missing \
		--cov-report=xml:coverage.xml \
		--cov-report=html:htmlcov

coverage-clean:
	rm -rf htmlcov .coverage .coverage.* coverage.xml

coverage-html:
	python -m pytest \
		--cov=domain \
		--cov=scripts \
		--cov-report=term-missing \
		--cov-report=html:htmlcov

coverage-xml:
	python -m pytest \
		--cov=domain \
		--cov=scripts \
		--cov-report=term-missing \
		--cov-report=xml:coverage.xml
