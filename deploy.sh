#!/bin/bash

# Script to deploy Hangman application to Kubernetes

echo "Deploying Hangman application to Kubernetes..."

# Create namespace
echo "Creating namespace..."
kubectl apply -f k8s/namespace.yaml

# Deploy PostgreSQL
echo "Deploying PostgreSQL..."
kubectl apply -f k8s/postgres-configmap.yaml
kubectl apply -f k8s/postgres-secret.yaml
kubectl apply -f k8s/postgres-pv.yaml
kubectl apply -f k8s/postgres-pvc.yaml
kubectl apply -f k8s/postgres-deployment.yaml
kubectl apply -f k8s/postgres-service.yaml

# Wait for PostgreSQL to be ready
echo "Waiting for PostgreSQL to be ready..."
kubectl wait --for=condition=ready pod -l app=postgres -n hangman --timeout=120s

# Deploy microservices
echo "Deploying Game Service..."
kubectl apply -f k8s/game-service-deployment.yaml
kubectl apply -f k8s/game-service-service.yaml

echo "Deploying Leaderboard Service..."
kubectl apply -f k8s/leaderboard-service-deployment.yaml
kubectl apply -f k8s/leaderboard-service-service.yaml

echo "Deploying Frontend..."
kubectl apply -f k8s/frontend-deployment.yaml
kubectl apply -f k8s/frontend-service.yaml

echo ""
echo "Deployment complete!"
echo ""
echo "Checking deployment status..."
kubectl get all -n hangman

echo ""
echo "Application will be available at: http://localhost:30000"
echo ""
echo "To check logs:"
echo "  kubectl logs -l app=frontend -n hangman"
echo "  kubectl logs -l app=game-service -n hangman"
echo "  kubectl logs -l app=leaderboard-service -n hangman"
