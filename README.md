# AI-Powered Phishing Email Detection System

An open-source, production-ready email phishing detection platform built with a **FastAPI** backend microservice and a responsive web frontend. The system runs real-time inference using a fine-tuned **DistilBERT** transformer model capable of classifying email text as safe or phishing.

To keep the repository lightweight, clean, and collaborative, the architecture decouples the codebase from the machine learning weights. The source code is maintained here on GitHub, while the heavy fine-tuned neural network weights are streamed and cached directly from the **Hugging Face Model Hub**.

---

## 🚀 Features
- **Real-Time Transformer Inference:** Leverages a custom fine-tuned DistilBERT sequence classification model.
- **Cloud-Streamed Model Architecture:** Zero local model weight setup required; weights automatically stream and cache from Hugging Face on application startup.
- **Asynchronous FastAPI Engine:** High-performance backend utilizing Pydantic for structural request validation and automatic OpenAPI documentation.
- **Interactive UI:** A lightweight, dynamic frontend attached directly via FastAPI `StaticFiles`.

---

## 🛠️ Local Setup & Installation

Follow these steps to set up and run the application on your local machine.

### 1. Clone the Repository
```bash
git clone [https://github.com/Salakawey/Email-Phishing-Detection.git](https://github.com/Salakawey/Email-Phishing-Detection.git)
cd Email-Phishing-Detection