# Use an official Python runtime as the base image
FROM python:3.9-slim

# Set environment variable to ensure output is logged immediately
ENV PYTHONUNBUFFERED=1

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt .

# Install Python dependencies
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copy the rest of your project code into the container
COPY . .

# Expose the port that Gradio uses (default is 7860)
EXPOSE 7860

# Run the application when the container starts
CMD ["python", "main.py"]
