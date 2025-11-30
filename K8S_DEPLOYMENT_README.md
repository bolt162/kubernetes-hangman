# Kubernetes Deployment Guide - Hangman Microservices

This document provides step-by-step instructions for deploying the Hangman application as microservices on Kubernetes.

## Prerequisites

1. **Docker** - For building container images
2. **kind** (Kubernetes in Docker) - For local Kubernetes cluster
   ```bash
   # Install kind on macOS
   brew install kind

   # Or download from: https://kind.sigs.k8s.io/
   ```
3. **kubectl** - Kubernetes CLI
   ```bash
   # Install kubectl on macOS
   brew install kubectl
   ```

## Architecture Overview

The application is split into 3 microservices:

1. **Frontend Service** (2 replicas) - Port 5000
   - Serves HTML templates and static files
   - Proxies requests to backend services

2. **Game Service** (3 replicas) - Port 5001
   - Handles game logic and state
   - Manages word selection and guesses

3. **Leaderboard Service** (2 replicas) - Port 5002
   - Manages high scores
   - Provides leaderboard rankings

All services share a PostgreSQL database with persistent storage.

## Deployment Steps

### Step 1: Create Kubernetes Cluster with kind

```bash
# Create a kind cluster named 'hangman-cluster'
kind create cluster --name hangman-cluster

# Verify cluster is running
kubectl cluster-info --context kind-hangman-cluster
```

### Step 2: Build Docker Images

```bash
# Run the build script
./build-images.sh

# This builds 3 images:
# - hangman-frontend:latest
# - hangman-game-service:latest
# - hangman-leaderboard-service:latest
```

### Step 3: Load Images into kind Cluster

```bash
# Load all images into the kind cluster
kind load docker-image hangman-frontend:latest --name hangman-cluster
kind load docker-image hangman-game-service:latest --name hangman-cluster
kind load docker-image hangman-leaderboard-service:latest --name hangman-cluster

# Verify images are loaded
docker exec -it hangman-cluster-control-plane crictl images | grep hangman
```

### Step 4: Deploy to Kubernetes

```bash
# Run the deployment script
./deploy.sh

# This will:
# 1. Create the 'hangman' namespace
# 2. Deploy PostgreSQL with persistent storage
# 3. Deploy all microservices
# 4. Create services for internal and external access
```

### Step 5: Verify Deployment

```bash
# Check all resources in the hangman namespace
kubectl get all -n hangman

# Expected output:
# - 1 PostgreSQL pod
# - 2 Frontend pods
# - 3 Game Service pods
# - 2 Leaderboard Service pods
# - All services (ClusterIP and NodePort)

# Check pod status
kubectl get pods -n hangman

# Check services
kubectl get svc -n hangman
```

### Step 6: Access the Application

```bash
# Get the NodePort service URL
kubectl get svc frontend -n hangman

# Access the application at:
# http://localhost:30000
```

If using kind, you may need to forward the port:
```bash
kubectl port-forward -n hangman svc/frontend 30000:5000
```

Then access at: http://localhost:30000

## Useful Commands

### View Logs

```bash
# Frontend logs
kubectl logs -l app=frontend -n hangman -f

# Game Service logs
kubectl logs -l app=game-service -n hangman -f

# Leaderboard Service logs
kubectl logs -l app=leaderboard-service -n hangman -f

# PostgreSQL logs
kubectl logs -l app=postgres -n hangman -f
```

### Scale Services

```bash
# Scale frontend to 4 replicas
kubectl scale deployment frontend -n hangman --replicas=4

# Scale game service to 5 replicas
kubectl scale deployment game-service -n hangman --replicas=5
```

### Check Pod Health

```bash
# Describe a specific pod
kubectl describe pod <pod-name> -n hangman

# Get pod details
kubectl get pods -n hangman -o wide

# Check events
kubectl get events -n hangman --sort-by='.lastTimestamp'
```

### Execute Commands in Pods

```bash
# Get a shell in a pod
kubectl exec -it <pod-name> -n hangman -- /bin/sh

# Check database connection from game service
kubectl exec -it <game-service-pod> -n hangman -- python -c "from app import db; print(db)"
```

### Database Access

```bash
# Connect to PostgreSQL
kubectl exec -it <postgres-pod-name> -n hangman -- psql -U hangman_user -d hangman

# Inside psql:
\dt          # List tables
\d games     # Describe games table
SELECT * FROM games LIMIT 10;
```

## Cleanup

To remove all resources:

```bash
# Run cleanup script
./cleanup.sh

# Or manually delete
kubectl delete namespace hangman
kubectl delete pv postgres-pv

# Delete kind cluster
kind delete cluster --name hangman-cluster
```

## Troubleshooting

### Pods Not Starting

```bash
# Check pod status
kubectl describe pod <pod-name> -n hangman

# Common issues:
# 1. Image not loaded into kind - run the load commands again
# 2. PostgreSQL not ready - wait for postgres pod to be Running
# 3. Database connection errors - check postgres service and credentials
```

### Service Not Accessible

```bash
# Check if service exists
kubectl get svc -n hangman

# Check endpoints
kubectl get endpoints -n hangman

# Port forward to test
kubectl port-forward -n hangman svc/frontend 8080:5000
```

### Database Connection Issues

```bash
# Verify postgres is running
kubectl get pods -l app=postgres -n hangman

# Check postgres logs
kubectl logs -l app=postgres -n hangman

# Verify service DNS
kubectl run -it --rm debug --image=busybox --restart=Never -n hangman -- nslookup postgres
```

## Architecture Benefits

1. **Scalability**: Each service can be scaled independently
2. **Fault Isolation**: Failure in one service doesn't crash the entire app
3. **Independent Deployment**: Update services without full redeployment
4. **Load Distribution**: Kubernetes automatically load balances across pods
5. **Self-Healing**: Kubernetes restarts failed pods automatically
6. **Resource Optimization**: Better utilization through container orchestration

## Testing the Application

1. Open http://localhost:30000
2. Enter your name and click "Start New Game"
3. Play the game by guessing letters
4. Win the game to see your score on the leaderboard
5. Check that your score appears on the home page leaderboard

## Monitoring

```bash
# Watch pod status in real-time
watch kubectl get pods -n hangman

# Monitor resource usage
kubectl top pods -n hangman
kubectl top nodes

# View all resources
kubectl get all -n hangman -o wide
```

## Screenshots Needed for Assignment

Take screenshots of:

1. All running pods: `kubectl get pods -n hangman`
2. All services: `kubectl get svc -n hangman`
3. Full resource list: `kubectl get all -n hangman`
4. Application home page (http://localhost:30000)
5. Playing a game
6. Leaderboard showing completed games
7. Pod logs showing service communication

## Additional Resources

- [Kubernetes Documentation](https://kubernetes.io/docs/)
- [kind Documentation](https://kind.sigs.k8s.io/)
- [kubectl Cheat Sheet](https://kubernetes.io/docs/reference/kubectl/cheatsheet/)
