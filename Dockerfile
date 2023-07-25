# Use the official Python image as the base image
FROM python:3.10

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set the working directory inside the container
WORKDIR /code

# Install system dependencies
RUN apt-get update \
    && apt-get install -y libpq-dev \
    && apt-get clean

# Install Python dependencies
COPY requirements.txt /code/
RUN pip install --no-cache-dir -r requirements.txt

# Copy the Django project files to the container
COPY . /code/

# Expose the port on which Gunicorn will run (if needed)
EXPOSE 8000

RUN python manage.py collectstatic --noinput

# Start the Django application using Gunicorn
CMD ["gunicorn", "server.wsgi", "--log-file", "-"]
