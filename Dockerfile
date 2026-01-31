FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app/mapplebackend


# System dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY mapplebackend/requirements.txt ./requirements.txt
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copy project
COPY mapplebackend /app/mapplebackend

EXPOSE 8000

CMD ["python", "-m", "daphne", "-b", "0.0.0.0", "-p", "8000", "mapplebackend.asgi:application"]

