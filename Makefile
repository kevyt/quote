#!/bin/bash
SHELL := /bin/bash

build:
	source venv/bin/activate
	pip install -r requirements.txt
	flask db upgrade

run:
	source venv/bin/activate
	flask run

.PHONY: build run
