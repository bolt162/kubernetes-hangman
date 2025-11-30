#!/bin/bash

echo "================================================"
echo "Hangman Kubernetes Deployment Verification"
echo "================================================"
echo ""

echo "Checking pod status..."
kubectl get pods -n hangman
echo ""

echo "Checking services..."
kubectl get svc -n hangman
echo ""

echo "Checking deployments..."
kubectl get deployments -n hangman
echo ""

echo "================================================"
echo "Testing Service Health Endpoints..."
echo "================================================"

# Test game service health
echo -n "Game Service Health: "
kubectl exec -n hangman deployment/frontend -- curl -s http://game-service:5001/health 2>/dev/null || echo "Not Ready"

echo -n "Leaderboard Service Health: "
kubectl exec -n hangman deployment/frontend -- curl -s http://leaderboard-service:5002/health 2>/dev/null || echo "Not Ready"

echo -n "Frontend Service Health: "
kubectl exec -n hangman deployment/frontend -- curl -s http://localhost:5000/health 2>/dev/null || echo "Not Ready"

echo ""
echo "================================================"
echo "Application Access Information"
echo "================================================"
echo ""
echo "To access the application, run ONE of these commands:"
echo ""
echo "Option 1 - Port Forward (recommended for kind):"
echo "  kubectl port-forward -n hangman svc/frontend 30000:5000"
echo "  Then open: http://localhost:30000"
echo ""
echo "Option 2 - NodePort (if kind was configured with extraPortMappings):"
echo "  http://localhost:30000"
echo ""
echo "================================================"
