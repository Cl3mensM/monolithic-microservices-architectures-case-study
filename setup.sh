#!/bin/bash

echo "Installing Helm repos..."
helm repo add ingress-nginx https://kubernetes.github.io/ingress-nginx
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
helm repo add grafana https://grafana.github.io/helm-charts
helm repo update

echo "Installing Helm charts..."
helm upgrade --install ingress-nginx ingress-nginx/ingress-nginx
helm upgrade --install prometheus prometheus-community/kube-prometheus-stack
helm upgrade --install grafana grafana/grafana \
--set adminPassword='admin' \
--set service.type=NodePort

echo "Applying Kubernetes YAMLs..."
cd microservice_kubernetes/locally
./apply-all.sh