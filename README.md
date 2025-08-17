# 📚 SpeedReading

**SpeedReading** is a modern, fast, and self-hosted backend for a speed-reading platform — open source and licensed under **GPLv3**.
This repository contains only the **backend**, built with **Python 3.11** and **FastAPI**.

## ✨ Features

* 🏠 Self-hosted backend
* 🔐 Secure authentication via JWT cookies
* 👤 User management & profiles
* 📖 Speed reading lessons and exercises
* ⚡ Real-time updates (progress tracking, stats)
* 🗄️ Configurable Redis and PostgreSQL integration
* 🧹 Logging with rotation and retention

## 🛣️ Roadmap

* 🌐 Web frontend (React / TailwindCSS)
* 📊 Analytics dashboard for reading stats
* 🎯 Gamification (points, badges, leaderboards)
* 📱 Mobile-friendly REST API endpoints

## 🚀 Getting Started

### 🧑‍💻 1. Run from source

```bash
git clone https://github.com/lifufkd/SpeedReading
cd SpeadReading
pip install -r requirements.txt
cd ./src
nano .env  # Fill in the env file according to the section "ENV configuration"
uvicorn main:app --host 0.0.0.0 --port 8000
```

### 🐳 2. Run with Docker

#### 1. Standalone

```bash
docker pull ghcr.io/lifufkd/speed-reading:latest
docker run \
  --name speed-reading \
  -d \
  -p 8000:8000 \
  -v <PATH_TO_MEDIA_FOLDER>:/app/data \
  --env-file <PATH-TO-ENV> \
  ghcr.io/lifufkd/speed-reading:latest
```

#### 2. All in one (with Docker Compose)

```bash
git clone https://github.com/lifufkd/SpeedReading
cd SpeedReading
docker-compose -f docker-compose.prod.yml up -d
```

## ⚙️ ENV Configuration

```bash
# Database settings
DB_USER=postgres
DB_PASSWORD=postgres
DB_DATABASE=postgres
DB_HOST=localhost
DB_PORT=5432

# Redis settings
REDIS_HOST=localhost
REDIS_PORT=6379
REDIS_DATABASE=0
REDIS_USER=
REDIS_PASSWORD=

# JWT Settings
AUTHJWT_SECRET_KEY=your_256_bit_random_string
AUTHJWT_DENYLIST_ENABLED=True
AUTHJWT_ACCESS_TOKEN_EXPIRES=900          # 15 minutes
AUTHJWT_REFRESH_TOKEN_EXPIRES=604800      # 7 days

# Super admin credentials
SUPER_ADMIN_LOGIN=admin
SUPER_ADMIN_PASSWORD=Admin123@

# Logging settings
LOG_LEVEL=INFO
LOG_FILE_PATH=app_data/logs/app.log
LOG_ROTATION=10 MB
LOG_RETENTION=7 days
LOG_COMPRESSION=gz

# CORS
CORS_ALLOW_CREDENTIALS=True
CORS_ALLOW_METHODS=["*"]
CORS_ALLOW_HEADERS=["*"]
CORS_ALLOWED_ORIGINS=[]
```

> All environment variables can also be configured via `.env` file.

## ❤️ Contributing

You can help by testing, opening issues, or contributing code.
Check the repository for more details and examples.

## 📜 License

Distributed under the GPLv3 License. See [LICENSE](https://github.com/lifufkd/SpeedReading/blob/main/LICENSE) for more information.
