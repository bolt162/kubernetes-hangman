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

<img width="769" height="139" alt="Screenshot 2025-11-29 at 7 54 24 PM" src="https://github.com/user-attachments/assets/93d28548-5be7-48fb-93fb-648c3f1bc5d5" />


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

<img width="748" height="104" alt="Screenshot 2025-11-29 at 7 55 02 PM" src="https://github.com/user-attachments/assets/62be8d11-c327-4080-addd-3d0aeb19d52f" />

---

## 3. Loading Images into kind

Commands used:
```bash
kind load docker-image hangman-frontend:latest --name hangman-cluster
kind load docker-image hangman-game-service:latest --name hangman-cluster
kind load docker-image hangman-leaderboard-service:latest --name hangman-cluster
```

**Screenshot: Loading images into kind cluster**

<img width="939" height="136" alt="Screenshot 2025-11-29 at 7 55 14 PM" src="https://github.com/user-attachments/assets/eefc09cf-3b4e-4258-b7ae-fd5f0843639f" />

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

<img width="616" height="346" alt="Screenshot 2025-11-29 at 7 55 22 PM" src="https://github.com/user-attachments/assets/1df9e0c7-18c2-423f-928b-91a58f2d6d11" />

---

## 5. Verifying Deployment

### 5.1 All Pods Running

Command:
```bash
kubectl get pods -n hangman
```

**Screenshot: All pods in Running status**

<img width="568" height="154" alt="Screenshot 2025-11-29 at 8 22 56 PM" src="https://github.com/user-attachments/assets/b930e1f4-2796-4e60-8b89-cadd94825566" />

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

<img width="632" height="88" alt="Screenshot 2025-11-29 at 8 23 23 PM" src="https://github.com/user-attachments/assets/de1d6334-c23b-4764-b72c-d9e0db67549b" />

Expected services:
- frontend (NodePort - port 30000)
- game-service (ClusterIP - port 5001)
- leaderboard-service (ClusterIP - port 5002)
- postgres (ClusterIP - port 5432)

---

## 6. Accessing the Application

Command used:
```bash
kubectl port-forward -n hangman svc/frontend 30000:5000
```

**Screenshot: Port forwarding active**

<img width="769" height="139" alt="Screenshot 2025-11-29 at 7 54 24 PM" src="https://github.com/user-attachments/assets/60e104b3-0ab8-40ce-8ca2-ea7a04524ea9" />

---

## 7. Application Running Screnshot

### 7.1 Home Page

URL: http://localhost:30000

<img width="729" height="348" alt="Screenshot 2025-11-29 at 8 24 46 PM" src="https://github.com/user-attachments/assets/03a5e92f-f335-45fb-8c35-085fdbe03954" />

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

**Microservices Architecture** - Application broken into independent services
**Container Orchestration** - Kubernetes managing multiple containers
**Service Discovery** - Services communicate via Kubernetes DNS
**Load Balancing** - Multiple replicas with automatic load distribution
**Persistent Storage** - PostgreSQL data persists across pod restarts
**Health Checks** - Liveness and readiness probes configured
**Scalability** - Independent scaling of each service

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
