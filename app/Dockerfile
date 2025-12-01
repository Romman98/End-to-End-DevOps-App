# 1️⃣ Base image
FROM python:3.11-slim

# 2️⃣ Set working directory inside the container
WORKDIR /app

# 3️⃣ Copy dependency list first (for caching)
COPY requirements.txt .

# 4️⃣ Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# 5️⃣ Copy the rest of the application code
COPY . .

# 6️⃣ Expose a port (optional, if your app runs as a service)
EXPOSE 5000

# 7️⃣ Set default command to run the app
CMD ["python", "app.py"]
