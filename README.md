
# Simple Multi-Label Weather Classifier

This is a small, original educational project that demonstrates a multi-label weather classifier using a **Logistic Regression** model (One-vs-Rest). The dataset is synthetic and generated in code — perfect for learning and safe to publish.

## What is included
- `backend/`
  - `train_model.py` — generates synthetic data, trains the model, and saves `model.pkl` and `scaler.pkl`.
  - `main.py` — Flask app that serves a simple frontend and exposes `/predict` API.
  - `requirements.txt` — Python dependencies for the backend.
- `frontend/`
  - `index.html`, `style.css`, `script.js` — A simple form-based UI to enter readings and get predictions.
- `run_project.sh` / `run_project.bat` — quick helpers to train & start the app.

## How to run locally (Linux / macOS)
1. Create a Python virtual environment and install dependencies:
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   pip install -r backend/requirements.txt
   ```
2. Train the model (this creates `model.pkl` and `scaler.pkl` inside `backend/`):
   ```bash
   python backend/train_model.py
   ```
3. Start the backend (the Flask app also serves the frontend):
   ```bash
   python backend/main.py
   ```
   Then open http://127.0.0.1:5000 in your browser.

## How to run on Windows (PowerShell)
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r backend\requirements.txt
python backend\train_model.py
python backend\main.py
```

## Notes
- This is a toy project with a synthetic dataset designed for clarity and minimal dependencies.
- You can replace the synthetic data with your own CSV data if desired. Update `train_model.py` to read your file and retrain.
- The frontend is intentionally minimal — it posts JSON to `/predict` and displays the returned labels.
