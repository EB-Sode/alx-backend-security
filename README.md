# alx-backend-security

# IP Tracking App

A Django-based application that tracks user IP addresses, stores them in a PostgreSQL database, and uses Redis for caching and performance optimization. The project demonstrates caching strategies, Dockerized service integration, and scalable deployment configurations.

## 🚀 Overview

This project implements a backend system to:

Track incoming user IP addresses.

Store property listings in PostgreSQL.

Cache property lists and querysets in Redis.

Measure Redis cache performance (hits/misses ratio).

Use Docker Compose for PostgreSQL and Redis services.

It’s an ideal example of combining Django + PostgreSQL + Redis + Docker for high-performance backend applications.

## 🧱 Tech Stack
Component	Purpose
Django	Web framework & API layer
PostgreSQL	Persistent database storage
Redis	Cache backend for performance
Docker & Docker Compose	Containerized service orchestration
Gunicorn	WSGI HTTP server for deployment
Celery (optional)	Background task processing
Python-dotenv