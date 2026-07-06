import os
import torch
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
from transformers import AutoTokenizer, AutoModelForSequenceClassification

# Initialize the FastAPI app
app = FastAPI(title="AI Phishing Detection System")

# --- ROBUST PATH CALCULATION FOR YOUR AI MODEL ---
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(CURRENT_DIR, "my_saved_model")

print(f"Targeting model folder at: {MODEL_PATH}")
print("Loading Fine-Tuned Deep Learning Model... Please wait...")

try:
    # Load your custom DistilBERT brain from your local folder
    tokenizer = AutoTokenizer.from_pretrained(MODEL_PATH)
    model = AutoModelForSequenceClassification.from_pretrained(MODEL_PATH)
    model.eval()  # Put the model in evaluation mode (turns off dropout layers)
    print("Model loaded successfully! AI engine is ready.")
except Exception as e:
    print(f"\nCRITICAL ERROR LOADING MODEL PATH: {e}")
    print("Please check if the 'my_saved_model' folder is sitting right next to main.py\n")

# Define data structure for incoming requests
class EmailPayload(BaseModel):
    text: str

# 1. UPDATED REAL AI ENDPOINT
@app.post("/api/predict")
async def predict_email(payload: EmailPayload):
    if not payload.text.strip():
        return {"error": "Email text cannot be empty."}
    
    # Run the user's text through your custom DistilBERT tokenizer
    inputs = tokenizer(payload.text, return_tensors="pt", padding=True, truncation=True, max_length=256)
    
    # Calculate predictions safely using PyTorch without calculating gradients
    with torch.no_grad():
        outputs = model(**inputs)
        logits = outputs.logits
        probabilities = torch.softmax(logits, dim=1).flatten().tolist()
    
    # Convert probability matrix decimals to clean percentages
    safe_score = round(probabilities[0] * 100, 2)
    phishing_score = round(probabilities[1] * 100, 2)
    
    # Set the threshold classification verdict
    prediction_result = "Phishing" if phishing_score > safe_score else "Safe"
    
    return {
        "prediction": prediction_result,
        "phishing_probability": f"{phishing_score}%",
        "safe_probability": f"{safe_score}%"
    }

# 2. Host our static frontend files
app.mount("/static", StaticFiles(directory="static"), name="static")

# 3. Serve the index.html page reliably
@app.get("/")
async def read_index():
    html_file_path = os.path.join(CURRENT_DIR, "static", "index.html")
    return FileResponse(html_file_path)