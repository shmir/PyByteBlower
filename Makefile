#
# Makefile to build and upload to local pypi servers.
# To upload to pypi.org use plain twine upload.
#
# todo: add support for twine?
#

repo=localhost
user=pypiadmin
password=pypiadmin

help:
	@echo 'install: install pip requirements'
	@echo 'build: build the package'
	@echo 'upload: create and upload the package to local pypi index'
	@echo '        takes the following params:'
	@echo '        repo=repository-url, default localhost:8086'
	@echo '        user=user name, default pypiadmin'
	@echo '        password=user password, default pypiadmin'

install:
	pip install -U -r requirements-dev.txt

.PHONY: build
build:
	rm -rf dist/*
	python setup.py sdist

upload:
	make build
	twine upload --repository-url http://$(repo):8036 --user $(user) --password $(password) dist/*
