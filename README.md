# AgriIntel — Agricultural Intelligence Platform

An AI-powered agricultural decision support platform built with Machine Learning, FastAPI, PostgreSQL, and Streamlit.

## Modules
- **Yield Prediction** — Random Forest regression on FAO/World Bank crop data (R² = 0.95)
- **Fertilizer Recommendation** — Random Forest classification on NPK/soil/crop data (Accuracy = 100%, verified legitimate)
- **Weather Intelligence** — Live weather data via OpenWeatherMap API
- **Crop Disease Detection** — CNN with transfer learning on PlantVillage dataset *(coming)*
- **Irrigation Recommendation** — Rule engine + ML hybrid *(coming)*

## Tech Stack
Python · scikit-learn · pandas · FastAPI · PostgreSQL · Streamlit · PyTorch · OpenCV

## Setup
```bash
python -m venv venv
venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

## Project Status
- [x] Phase 0 — Foundation
- [x] Phase 1 — Yield Prediction
- [x] Phase 2 — Fertilizer Recommendation
- [x] Phase 3 — Weather Integration
- [x] Phase 4 — FastAPI Backend
- [x] Phase 5 — Database
- [x] Phase 6 — Frontend Dashboard