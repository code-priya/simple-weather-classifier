
#!/usr/bin/env bash
set -e
echo "Setting up virtual environment..."
python3 -m venv .venv || true
source .venv/bin/activate
pip install -r backend/requirements.txt
echo "Training model..."
python backend/train_model.py
echo "Starting Flask app..."
python backend/main.py
