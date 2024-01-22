# Use an official Python runtime as a parent image
FROM python:3.9.2-slim

# Set the working directory to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip install --upgrade pip && pip install -r requirements.txt

# Make port 9876 available to the world outside this container
EXPOSE 9876

# Define environment variable for production
ARG GITHUB_ACCESS_TOKEN
ARG LLM_URL_WITHOUT_TRAILING_SLASH
ARG RUN_POD_ACCESS_TOKEN


ENV GITHUB_ACCESS_TOKEN=$GITHUB_ACCESS_TOKEN
ENV LLM_URL_WITHOUT_TRAILING_SLASH=$LLM_URL_WITHOUT_TRAILING_SLASH
ENV RUN_POD_ACCESS_TOKEN=RUN_POD_ACCESS_TOKEN

# Run app.py when the container launches
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "9876", "--workers", "4"]



# sudo docker buildx build --platform=linux/amd64 -t vishals9711/llm_backend:latest --progress=plain --build-arg GITHUB_ACCESS_TOKEN=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 --build-arg LLM_URL_WITHOUT_TRAILING_SLASH=http://localhost:8090 .

