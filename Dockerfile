# This line specifies our base image - think of it as the foundation
# We use python:3.9-slim which gives us a minimal Python environment
FROM python:3.10-slim

WORKDIR /app

# Install system dependencies for CadQuery
RUN apt-get update && apt-get install -y \
    libgl1-mesa-glx \
    libglu1-mesa \
    build-essential \
    cmake \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy your entire project into the container
COPY . .

# Create outputs directory
RUN mkdir -p outputs

# Expose the port the app runs on
EXPOSE 5000

ENV FLASK_APP=app.py
ENV FLASK_ENV=production

# Run the app
CMD ["flask", "run", "--host=0.0.0.0"]
