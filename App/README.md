# ⚽ VARLens AI

<p align="center">
  <img src="docs/logo.png" alt="VARLens AI Logo" width="180">
</p>

<h3 align="center">
See the Call. Trust the Decision.
</h3>

<p align="center">
Explainable Artificial Intelligence for Transparent Sports Officiating
</p>

---

## 📖 Overview

VARLens AI is an Explainable Artificial Intelligence (XAI) platform designed to improve fairness, transparency, and trust in football officiating.

Unlike traditional VAR systems that only provide a final decision, VARLens AI explains **why** a decision was made by combining computer vision, multi-object tracking, offside geometry analysis, and large language models into an intuitive dashboard.

The platform detects players and the ball, tracks player movement, analyzes offside situations, calculates confidence scores, and generates human-readable explanations supported by visual evidence.

---

# ✨ Features

## 🎥 Video Analysis

- Upload football match videos
- Automatic frame extraction
- Real-time inference
- Replay generation
- Match history

---

## 👥 Player Detection

- YOLOv11 player detection
- Ball detection
- Goalkeeper detection
- Referee detection

---

## 🏃 Player Tracking

- ByteTrack multi-object tracking
- Persistent player IDs
- Player trajectory visualization
- Speed estimation

---

## 📐 Offside Detection

- Detect last defender
- Detect attacking player
- Detect pass frame
- Generate offside line
- Offside geometry calculation
- Decision confidence

---

## 🧠 Explainable AI

Instead of only displaying:

> OFFSIDE

VARLens AI explains:

> The attacker was 23 cm ahead of the last defender when the ball was played. Detection confidence was 96.4%. Camera visibility was unobstructed, producing a high-confidence decision.

Explainability includes:

- SHAP Feature Importance
- Confidence Breakdown
- Decision Summary
- Visual Evidence
- GPT-5.5 Natural Language Explanation

---

## 📊 Analytics Dashboard

- Match statistics
- Timeline
- Heatmaps
- Player tracking
- Event analytics
- Decision history
- Confidence visualization

---

# 🏗 System Architecture

```
                         Stadium Cameras
                                │
                                ▼
                       Video Upload API
                                │
                                ▼
                     FastAPI Backend Service
                                │
     ┌──────────────────────────┼──────────────────────────┐
     │                          │                          │
     ▼                          ▼                          ▼
YOLOv11 Detection        ByteTrack Tracking        MediaPipe Pose
     │                          │                          │
     └───────────────┬──────────┴───────────────┐
                     ▼                          ▼
              Offside Geometry          Event Detection
                     │
                     ▼
            Explainability Engine
                     │
          ┌──────────┴──────────┐
          ▼                     ▼
      SHAP Analysis       GPT-5.5 Explanation
                     │
                     ▼
              Interactive Dashboard
```

---

# 🛠 Tech Stack

## Frontend

- Next.js 15
- React
- TypeScript
- Tailwind CSS
- shadcn/ui
- Framer Motion
- Recharts

---

## Backend

- FastAPI
- Python 3.12
- Uvicorn

---

## AI & Computer Vision

- OpenCV
- Ultralytics YOLOv11
- ByteTrack
- MediaPipe
- PyTorch

---

## Explainability

- SHAP
- GPT-5.5

---

## Database

- Supabase PostgreSQL

---

## Authentication

- Supabase Auth

---

## Deployment

- Docker
- Vercel
- Render

---

# 📂 Project Structure

```
VARLens-AI/

├── frontend/
│   ├── app/
│   ├── components/
│   ├── dashboard/
│   ├── replay/
│   ├── analytics/
│   ├── upload/
│   └── lib/
│
├── backend/
│   ├── app/
│   │   ├── api/
│   │   ├── services/
│   │   ├── models/
│   │   ├── schemas/
│   │   ├── explainability/
│   │   ├── tracking/
│   │   ├── cv/
│   │   └── database/
│   │
│   └── main.py
│
├── docs/
│
├── docker/
│
├── datasets/
│
├── README.md
│
└── .env.example
```

---

# 🚀 Installation

## Clone Repository

```bash
git clone https://github.com/yourusername/VARLens-AI.git

cd VARLens-AI
```

---

# Backend

```bash
cd backend

python -m venv .venv

source .venv/bin/activate

pip install -r requirements.txt

uvicorn app.main:app --reload
```

---

# Frontend

```bash
cd frontend

npm install

npm run dev
```

---

# Environment Variables

Backend

```
OPENAI_API_KEY=

SUPABASE_URL=

SUPABASE_KEY=

DATABASE_URL=

YOLO_MODEL=models/yolo11.pt

MODEL_DEVICE=cuda
```

Frontend

```
NEXT_PUBLIC_API_URL=http://localhost:8000
```

---

# API Endpoints

## Authentication

```
POST /auth/login

POST /auth/register
```

---

## Upload

```
POST /videos/upload
```

---

## Analysis

```
POST /analysis/start

GET /analysis/{id}
```

---

## Replay

```
GET /replay/{id}
```

---

## History

```
GET /history
```

---

## Analytics

```
GET /analytics
```

---

# Example API Response

```json
{
  "decision": "OFFSIDE",
  "confidence": 0.964,
  "attacker_id": 14,
  "last_defender_id": 5,
  "distance_cm": 23,
  "frame": 1821,
  "evidence": {
    "tracking_ids": [
      5,
      14
    ],
    "offside_line": {
      "x": 615,
      "y1": 0,
      "y2": 1080
    }
  },
  "explanation": "The attacker was ahead of the last defender when the ball was played. Based on player positions and offside geometry, the decision is OFFSIDE with 96.4% confidence."
}
```

---

# Production Notes

The FastAPI service owns the runtime pipeline located at:

```
backend/app/services/pipeline.py
```

Configure the production model using a licensed local Ultralytics checkpoint:

```
YOLO_MODEL=models/yolo11.pt
```

Do **not** commit proprietary model weights to the repository. Store the checkpoint locally or retrieve it through your deployment process. Every analysis response includes tracking IDs and offside geometry as evidence supporting the decision.

---

# Future Roadmap

- Multi-camera synchronization
- 3D offside reconstruction
- Goal-line technology integration
- Handball detection
- Foul detection
- Penalty detection
- Expected Goals (xG)
- AI referee assistant
- Basketball support
- Tennis support
- Rugby support

---

# Security

- JWT Authentication
- HTTPS Deployment
- Rate Limiting
- Environment Variables
- Secure File Upload
- Role-Based Access Control

---

# Performance

| Component | Target |
|------------|---------|
| Player Detection | 30 FPS |
| Tracking | Real-time |
| Offside Decision | <1 second |
| API Response | <300 ms |
| Dashboard Load | <2 seconds |

---

# License

This project is released under the MIT License.

---

# Team

VARLens AI

**See the Call. Trust the Decision.**

Built with ❤️ using Computer Vision, Explainable AI, and GPT-5.5.
