# Use the official Python runtime image as your baseline kitchen
FROM python:3.11-slim

# Establish an active working directory inside the container
WORKDIR /app

# Copy the Lab 7 inventory system (source, tests and data) into the container
COPY *.py inventory.json ./

# Default: run the program. Run the tests with:
#   docker run --rm lab7-inventory python -m unittest -v
CMD ["python", "main.py"]
