#!/bin/bash

# Script to build all Docker images for the Hangman microservices

echo "Building Docker images for Hangman microservices..."

# Build Frontend Service
echo "Building Frontend Service..."
docker build -t hangman-frontend:latest ./services/frontend/

# Build Game Service
echo "Building Game Service..."
docker build -t hangman-game-service:latest ./services/game-service/

# Build Leaderboard Service
echo "Building Leaderboard Service..."
docker build -t hangman-leaderboard-service:latest ./services/leaderboard-service/

echo ""
echo "All images built successfully!"
echo ""
echo "Image list:"
docker images | grep hangman

echo ""
echo "To load images into kind cluster, run:"
echo "  kind load docker-image hangman-frontend:latest --name hangman-cluster"
echo "  kind load docker-image hangman-game-service:latest --name hangman-cluster"
echo "  kind load docker-image hangman-leaderboard-service:latest --name hangman-cluster"
