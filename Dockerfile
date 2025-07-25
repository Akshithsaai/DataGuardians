# Use an official Python runtime as a parent image
# adding this one as a dummy push
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Make port 5000 available to the world outside this container (adjust if needed)
#EXPOSE 8080

# Define environment variable
ENV PYTHONUNBUFFERED=1

# Run the application
CMD ["python", "main_method.py" , "--gcp_bigquery_dataset" , "data_mgmt" , "--project_id" , "ltc-reboot25-team-24" , "--location" , "europe-west2"]
