# Use an official Python runtime as a parent image
FROM python:3.9-buster

# Set the working directory in the container
WORKDIR /app

# Install system dependencies required by cffi and clean up to reduce image size
RUN apt-get update \
    && apt-get install -y --no-install-recommends libpq-dev gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy main.py into the container at /app
COPY . /app

# Copy the requirements file into the container
COPY requirements.txt /app

# Install Python dependencies
RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt

# Make port 15400 available to the world outside this container
EXPOSE 15400

# Run the application using full path to uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "15400", "--reload"]
