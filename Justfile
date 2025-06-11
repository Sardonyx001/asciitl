set shell := ["fish", "-c"]
set dotenv-load := true

default:
    @just --list

venv:
    @test .venv || uv venv

activate: 
    @source .venv/bin/activate.fish

run: venv activate
    @streamlit run main.py

sloc:
    @echo "`wc -l *.py` lines of code"
