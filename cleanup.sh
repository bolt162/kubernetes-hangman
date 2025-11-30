#!/bin/bash

# Script to cleanup Kubernetes resources

echo "Cleaning up Hangman application from Kubernetes..."

kubectl delete namespace hangman
kubectl delete pv postgres-pv

echo "Cleanup complete!"
