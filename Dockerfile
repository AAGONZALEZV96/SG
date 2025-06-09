FROM python:3.12-slim

WORKDIR /app

# Install Node.js for Serverless
RUN apt-get update && apt-get install -y \
    curl \
    && curl -fsSL https://deb.nodesource.com/setup_18.x | bash - \
    && apt-get install -y nodejs \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY requirements.txt package.json ./

# Install Python and Node dependencies
RUN pip install -r requirements.txt
RUN npm install

# Copy application code
COPY . .

# Expose port
EXPOSE 3000

# Start command
CMD ["npm", "run", "start"]
