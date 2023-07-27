# Use an official Python runtime as a base image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install required packages from requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Expose the port that your Flask app is listening on
EXPOSE 3063

# Start the Flask app when the container is run
CMD ["python", "app.py"]
