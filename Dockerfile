FROM python:3.10-slim

# Don't generate .pyc files
ENV PYTHONDONTWRITEBYTECODE 1

# Print output directly to the terminal without buffering.
ENV PYTHONUNBUFFERED 1

# Set the working directory in the container
WORKDIR /app

COPY requirements.txt /app/

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code into the container at /app
COPY . /app

EXPOSE 8000

# Run the application
CMD ["uvicorn", "src.run_server:app", "--host", "0.0.0.0", "--port", "8000"]
