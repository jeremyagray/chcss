#***********************************************************************
#
# Makefile - chore makefile for chcss
#
# SPDX-License-Identifier: GPL-3.0-or-later
#
# chcss, a CSS naming hierarchy enforcer.
# Copyright (C) 2021 Jeremy A Gray <jeremy.a.gray@gmail.com>.
#
#***********************************************************************

.PHONY : build clean commit dist docs freeze lint pip test test-all upload upload-test

test-all:
	pytest -vv --cov chcss --cov-report term --cov-report html

build :
	cd docs && make html
	pip install -q build
	python -m build

clean :
	rm -rf build
	rm -rf dist
	rm -rf chcss.egg-info
	cd docs && make clean

dist : clean build

docs :
	cd docs && make html

commit :
	pre-commit run --all-files

lint :
	flake8 --exit-zero
	black --check .

pip :
	pip install -r requirements.txt

freeze : requirements.txt
	pip freeze > requirements.txt

test:
	pytest --cov chcss --cov-report term

upload:
	python3 -m twine upload --verbose dist/*

upload-test:
	python3 -m twine upload --verbose --repository testpypi dist/*
