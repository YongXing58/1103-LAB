# Use the official Python runtime image as your baseline kitchen
FROM python:3.11-slim

# Establish an active working directory inside the container
WORKDIR /app

# Copy the OOP inventory system files into the container workspace
COPY main.py product.py inventory.py inventory_file.py ./

# Define the execution command to run when the container starts
CMD ["python", "main.py"]
