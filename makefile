install:
	test -d venv || virtualenv venv --python=python3
	venv/bin/pip install -r requirements.txt

source:
	@(which python | grep -E "/venv/bin/python\b") || \
		(echo "Remember to  *** source venv/bin/activate ***  before running make start!" && \
			echo "You can make install to get venv + install requirements.txt localy" && \
			exit 1)

start: source
	python scripts/start.py

autorun:
	python test.py
