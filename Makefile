.PHONY: all
all: devenv

.PHONY: devenv
devenv: venv
venv:
	virtualenv --python=python2.7 venv
	venv/bin/pip install --upgrade -r requirements.txt
