# Use official Python image as base
FROM python:3.9-slim

# Set working directory inside container
WORKDIR /app

# Copy requirements file first
COPY requirements.txt .

# Install Python libraries
RUN pip install -r requirements.txt

# Copy the app code
COPY . .

# Expose port 8501
EXPOSE 8501

# Command to run the app
CMD ["python", "-m", "streamlit", "run", "app.py", "--server.address=0.0.0.0"]