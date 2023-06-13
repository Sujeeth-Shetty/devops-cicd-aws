# Use an official Python runtime as the base image
FROM --platform=linux/amd64 python:3.10-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements.txt file
COPY requirements.txt .

# Install the Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the app.py file into the container
COPY src/app.py .

# Expose the port on which the server will run
EXPOSE 5000

# Define the command to run your application
CMD ["python", "app.py"]
