# Hangman Kubernetes Deployment - Screenshots & Documentation

This document provides a visual walkthrough of deploying the Hangman microservices application on Kubernetes.

---

## Table of Contents
1. [Creating the Kubernetes Cluster](#1-creating-the-kubernetes-cluster)
2. [Building Docker Images](#2-building-docker-images)
3. [Loading Images into kind](#3-loading-images-into-kind)
4. [Deploying to Kubernetes](#4-deploying-to-kubernetes)
5. [Verifying Deployment](#5-verifying-deployment)
6. [Accessing the Application](#6-accessing-the-application)
7. [Application Screenshots](#7-application-screenshots)

---

## 1. Creating the Kubernetes Cluster

Command used:
```bash
kind create cluster --name hangman-cluster
```

**Screenshot: Creating kind cluster**

[PASTE SCREENSHOT HERE - kind create cluster command output]

---

## 2. Building Docker Images

Command used:
```bash
./build-images.sh
```

This script builds three Docker images:
- `hangman-frontend:latest`
- `hangman-game-service:latest`
- `hangman-leaderboard-service:latest`

**Screenshot: Building Docker images**

[PASTE SCREENSHOT HERE - build-images.sh output showing all three images being built]

**Screenshot: Docker images list**

[PASTE SCREENSHOT HERE - docker images output showing the built images]

---

## 3. Loading Images into kind

Commands used:
```bash
kind load docker-image hangman-frontend:latest --name hangman-cluster
kind load docker-image hangman-game-service:latest --name hangman-cluster
kind load docker-image hangman-leaderboard-service:latest --name hangman-cluster
```

**Screenshot: Loading images into kind cluster**

[PASTE SCREENSHOT HERE - kind load docker-image commands output]

---

## 4. Deploying to Kubernetes

Command used:
```bash
./deploy.sh
```

This script:
- Creates the `hangman` namespace
- Deploys PostgreSQL with persistent storage
- Deploys all microservices (frontend, game-service, leaderboard-service)
- Creates all necessary services

**Screenshot: Running deploy.sh**

[PASTE SCREENSHOT HERE - deploy.sh output showing all resources being created]

---

## 5. Verifying Deployment

### 5.1 All Pods Running

Command:
```bash
kubectl get pods -n hangman
```

**Screenshot: All pods in Running status**

[PASTE SCREENSHOT HERE - kubectl get pods showing all 8 pods running]

Expected output:
- 2 frontend pods
- 3 game-service pods
- 2 leaderboard-service pods
- 1 postgres pod

### 5.2 All Services

Command:
```bash
kubectl get svc -n hangman
```

**Screenshot: All services**

[PASTE SCREENSHOT HERE - kubectl get svc showing all services]

Expected services:
- frontend (NodePort - port 30000)
- game-service (ClusterIP - port 5001)
- leaderboard-service (ClusterIP - port 5002)
- postgres (ClusterIP - port 5432)

### 5.3 Complete Deployment Overview

Command:
```bash
kubectl get all -n hangman
```

**Screenshot: Complete deployment status**

[PASTE SCREENSHOT HERE - kubectl get all showing pods, services, deployments, and replicasets]

---

## 6. Accessing the Application

Command used:
```bash
kubectl port-forward -n hangman svc/frontend 30000:5000
```

**Screenshot: Port forwarding active**

[PASTE SCREENSHOT HERE - kubectl port-forward command running and showing "Forwarding from 127.0.0.1:30000 -> 5000"]

---

## 7. Application Screenshots

### 7.1 Home Page

URL: http://localhost:30000

**Screenshot: Application home page showing leaderboard**

[PASTE SCREENSHOT HERE - Browser showing Hangman home page with leaderboard]

### 7.2 Starting a New Game

**Screenshot: New game page with player name input**

[PASTE SCREENSHOT HERE - New game form where user enters their name]

### 7.3 Playing the Game

**Screenshot: Active game showing word progress and guessed letters**

[PASTE SCREENSHOT HERE - Game in progress with partially guessed word]

### 7.4 Winning a Game

**Screenshot: Game won screen showing score**

[PASTE SCREENSHOT HERE - Completed game showing the word was guessed correctly and final score]

### 7.5 Updated Leaderboard

**Screenshot: Leaderboard updated with new winning score**

[PASTE SCREENSHOT HERE - Home page showing updated leaderboard with the new game result]

---

## Architecture Summary

### Microservices Deployed:

1. **Frontend Service** (2 replicas)
   - Serves HTML/CSS/JavaScript
   - Communicates with backend services
   - Exposed via NodePort on port 30000

2. **Game Service** (3 replicas)
   - Handles game logic and word selection
   - Manages game state in PostgreSQL
   - Internal ClusterIP service

3. **Leaderboard Service** (2 replicas)
   - Manages high scores
   - Queries game results from PostgreSQL
   - Internal ClusterIP service

4. **PostgreSQL Database** (1 replica)
   - Persistent storage using PersistentVolume
   - Shared database for game and leaderboard services

### Total Resources:
- **Pods:** 8 (2 frontend + 3 game + 2 leaderboard + 1 postgres)
- **Services:** 4 (1 NodePort + 3 ClusterIP)
- **Deployments:** 4
- **PersistentVolumes:** 1

---

## Key Features Demonstrated

✅ **Microservices Architecture** - Application broken into independent services
✅ **Container Orchestration** - Kubernetes managing multiple containers
✅ **Service Discovery** - Services communicate via Kubernetes DNS
✅ **Load Balancing** - Multiple replicas with automatic load distribution
✅ **Persistent Storage** - PostgreSQL data persists across pod restarts
✅ **Health Checks** - Liveness and readiness probes configured
✅ **Scalability** - Independent scaling of each service

---

## Cleanup

To remove all resources:
```bash
./cleanup.sh
kind delete cluster --name hangman-cluster
```

---

**Project Repository:** [Add your GitHub repo link here]

**Date:** November 29, 2024

**Student:** [Your Name]
