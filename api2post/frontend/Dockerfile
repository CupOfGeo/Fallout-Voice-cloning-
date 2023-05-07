# Use an official Python runtime as a parent image
FROM python:3.9-slim-buster
RUN apt-get update \
    && apt-get -y install libpq-dev gcc
# Set the working directory to /app
WORKDIR /app

COPY requirements.txt requirements.txt

# Install any needed packages specified in requirements.txt
RUN pip install --trusted-host pypi.python.org -r requirements.txt

# Copy the current directory contents into the container at /app
COPY . /app

# Set the environment variable for the backend URL
ENV BACKEND_URL=http://0.0.0.0:80

# Make port 80 available to the world outside this container
EXPOSE 8050

# Run transcript-reviewer.py when the container launches
CMD ["uvicorn", "transcript-reviewer:app", "--host", "0.0.0.0", "--port", "8050"]
