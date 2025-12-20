# Use the official Python image
FROM python:3.10-slim

# Set the working directory
WORKDIR /app

# Copy your project files into the container
COPY . .

# Install the libraries
RUN pip install --no-cache-dir -r requirements.txt

# Run Streamlit on port 8080 (Required for Cloud Run)
CMD streamlit run app.py --server.port 8080 --server.address 0.0.0.0
