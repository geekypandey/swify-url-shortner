#!/bin/bash

if [ -d '.venv' ]; then
	. .venv/bin/activate
else
	python -m venv .venv
	. .venv/bin/activate
fi

export SECRET_KEY='reddington'
export DATABASE_URL='sqlite:///url.db'
