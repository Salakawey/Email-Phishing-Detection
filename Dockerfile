# Use the official lightweight Python image
FROM python:3.10-slim

# Set up the working directory inside the container
WORKDIR /code

# Copy requirements first to leverage Docker cache layers
COPY ./requirements.txt /code/requirements.txt

# Install dependencies cleanly without saving cache bloat
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

# Create a non-root system user for security compliance in the sandboxed space
RUN useradd -m -u 1000 user
USER user
ENV HOME=/home/user \
    PATH=/home/user/.local/bin:$PATH \
    TRANSFORMERS_CACHE=/tmp/.cache

WORKDIR $HOME/app

# Copy the entire workspace code over, ensuring ownership stays with our user
COPY --chown=user . $HOME/app

# Expose port 7860 (Hugging Face's mandatory container port) and run Uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "7860"]