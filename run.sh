#!/bin/bash

poetry update
poetry install
poetry run pyside6-project build 
poetry run python main.py