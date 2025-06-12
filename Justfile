default:
    just --list

run:
    uv run streamlit run main.py

sloc:
    @echo "`wc -l *.py` lines of code"
