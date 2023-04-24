# Use an official Python base image from the Docker Hub
FROM python:3.10-slim

# Install git
RUN apt-get -y update
RUN apt-get -y install git 

# Set environment variables
ENV PIP_NO_CACHE_DIR=yes \
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

# Create a non-root user and set permissions
# RUN useradd --create-home appuser
WORKDIR /home/appuser
# RUN chown appuser:appuser /home/appuser
# USER appuser

# Copy the requirements.txt file and install the requirements
# COPY --chown=appuser:appuser requirements.txt .
COPY requirements.txt .
# RUN pip install --no-cache-dir --user -r requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application files
# COPY --chown=appuser:appuser . ./
COPY . ./

# Set the entrypoint
ENTRYPOINT ["python", "-m", "main.py"]