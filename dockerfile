# Use the official Python image as the base image
FROM python:3.9-slim

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements.txt file to the container
COPY requirements.txt .

# Install the Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the IPAM script files to the container
COPY main.py .
COPY templates templates/

# Expose the port that the FastAPI server will run on
EXPOSE 4000

# Start the FastAPI server when the container is launched
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "4000"]
