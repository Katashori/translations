FROM python:3.13-slim

WORKDIR /app

# Install pg_isready and other necessary dependencies
RUN apt-get update && apt-get install -y postgresql-client

COPY requirements.txt ./
RUN pip install -r requirements.txt

# Copy the rest of your application code
COPY . .

CMD ["./run.sh"]
