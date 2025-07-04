# Use a lightweight Python base image
FROM python:3.11-slim

# Set the working directory
WORKDIR /app

# Install dependencies
COPY email_service/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the service code
COPY . .

# Run the email sending script
CMD ["python", "-m", "email_service.send_emails"]
