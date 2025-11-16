
@echo off
python -m venv .venv
.\.venv\Scripts\activate
pip install -r backend\requirements.txt
python backend\train_model.py
python backend\main.py
