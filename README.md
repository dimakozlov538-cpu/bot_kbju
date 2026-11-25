# 🥗 Bot KBJU (Калькулятор Калорий, Белков, Жиров и Углеводов)

[![Repository](https://img.shields.io/badge/Repository-GitHub-181717?logo=github&logoColor=white)](https://github.com/dimakozlov538-cpu/bot_kbju)
![Python](https://img.shields.io/badge/Python-3.10+-3776AB?logo=python&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-2496ED?logo=docker&logoColor=white)
![Nginx](https://img.shields.io/badge/Nginx-009639?logo=nginx&logoColor=white)
![Monitoring](https://img.shields.io/badge/Monitoring-Prometheus_%2B_Grafana-E6522C?logo=prometheus&logoColor=white)

Высокодоступный Telegram-бот для трекинга КБЖУ с полноценной production-инфраструктурой: контейнеризацией, обратным проксированием (Webhook), мониторингом метрик и автоматическим резервным копированием данных.

## 📋 Оглавление
- [Архитектура проекта](#-архитектура-проекта)
- [Реализованные DevOps-практики](#-реализованные-devops-практики)
- [Технологический стек](#-технологический-стек)
- [🚀 Быстрый старт](#-быстрый-старт)
- [Переменные окружения](#-переменные-окружения)
- [Мониторинг и логи](#-мониторинг-и-логи)
- [Резервное копирование](#-резервное-копирование)

---

## 🏗 Архитектура проекта

Вся инфраструктура оркестрируется через **Docker Compose** и разделена на изолированные сервисы для обеспечения отказоустойчивости и безопасности:

```mermaid
flowchart LR
    User([Пользователь Telegram]) -- Webhook --> Nginx[Nginx<br/>Reverse Proxy & SSL]
    Nginx -- "/webhook" --> App[Backend App<br/>Python Async API]
    App --读写--> DB[(PostgreSQL<br/>Основная БД)]
    App -- Кэш --> Cache[(Redis<br/>Состояния/Кэш)]
    
    Monitoring[Monitoring Stack<br/>Prometheus + Grafana] -. Метрики .-> Nginx
    Monitoring -. Метрики .-> App
    Monitoring -. Метрики .-> DB
    
    Backup[Cron Backup Script] -- Ежедневный дамп --> Backups[(Backups<br/>Локально + S3)]
