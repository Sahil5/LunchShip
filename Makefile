.PHONY: all
all: devenv

.PHONY: devenv
devenv: venv
venv: requirements.txt
	virtualenv --python=python2.7 venv
	venv/bin/pip install --upgrade -r requirements.txt

.PHONY: clean
clean:
	rm -r venv
