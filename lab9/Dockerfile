# Use the official Python runtime image as your baseline kitchen
FROM python:3.11-slim

# Establish an active working directory inside the container
WORKDIR /app

# Copy the Lab 9 inventory system (source, data and tests) into the container
COPY *.py inventory.json products.csv ./
COPY tests/ tests/

# Default: run the demo. Run the tests with:
#   docker run --rm lab9-inventory python -m unittest discover -s tests -t . -v
CMD ["python", "demo.py"]
