# Use a lightweight official Python image
FROM python:3.11-slim

# Set the working directory in the container
WORKDIR /app

# Copy only requirements first for better caching
COPY kev_fetcher/requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the app
COPY . .

# Run the fetcher script by default
CMD ["python", "-m", "kev_fetcher.fetch_kev"]
