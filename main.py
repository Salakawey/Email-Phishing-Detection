import os
import logging
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI
app = FastAPI(
    title="AI Phishing Guard",
    description="Professional AI-Powered Email Phishing Detection System",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, restrict to specific domains
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Robust Model Loading ---
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = "Salakawey/Email-Phishing-DistilBERT"

logger.info(f"Loading model from: {MODEL_PATH}")

try:
    tokenizer = AutoTokenizer.from_pretrained(MODEL_PATH)
    model = AutoModelForSequenceClassification.from_pretrained(MODEL_PATH)
    model.eval()
    logger.info("✅ Model loaded successfully!")
except Exception as e:
    logger.error(f"❌ Failed to load model: {e}")
    tokenizer = None
    model = None

# Request model
class EmailPayload(BaseModel):
    text: str

@app.post("/api/predict")
async def predict_email(payload: EmailPayload):
    if not payload.text or not payload.text.strip():
        raise HTTPException(status_code=400, detail="Email text cannot be empty.")

    if model is None or tokenizer is None:
        raise HTTPException(status_code=503, detail="Model not loaded. Service unavailable.")

    try:
        # Tokenize
        inputs = tokenizer(
            payload.text,
            return_tensors="pt",
            padding=True,
            truncation=True,
            max_length=256
        )

        # Inference
        with torch.no_grad():
            outputs = model(**inputs)
            logits = outputs.logits
            probabilities = torch.softmax(logits, dim=1).flatten().tolist()

        safe_score = round(probabilities[0] * 100, 2)
        phishing_score = round(probabilities[1] * 100, 2)

        prediction_result = "Phishing" if phishing_score > safe_score else "Safe"

        return {
            "prediction": prediction_result,
            "phishing_probability": f"{phishing_score}%",
            "safe_probability": f"{safe_score}%",
            "confidence": max(safe_score, phishing_score)
        }

    except Exception as e:
        logger.error(f"Prediction error: {e}")
        raise HTTPException(status_code=500, detail="Internal server error during prediction.")

# Health check
@app.get("/health")
async def health():
    return {
        "status": "healthy",
        "model_loaded": model is not None
    }

# Serve static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Serve index
@app.get("/")
async def read_index():
    html_file_path = os.path.join(CURRENT_DIR, "static", "index.html")
    if not os.path.exists(html_file_path):
        raise HTTPException(status_code=404, detail="Frontend not found.")
    return FileResponse(html_file_path)