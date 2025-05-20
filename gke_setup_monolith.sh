# Check project
echo "Check that you are connected to the right project"
gcloud config set project ba-monolith
gcloud info
echo "Correct project?"
read -p "Press enter to continue"

# Add containers to GCR
echo "Add containers to GCR"
cd monolithic_architecture
docker buildx build --platform linux/amd64,linux/arm64 \
    -t gcr.io/ba-monolith/my-django-app:latest \
    --push .

# Create GKE cluster
gcloud container clusters create-auto monolith \
    --region=europe-west4

# Get credentials for the cluster
gcloud container clusters get-credentials monolith \
    --region=europe-west4

# Apply Kubernetes YAMLs
echo "Apply Kubernetes YAMLs"
cd ../monolith_kubernetes/GKE
find . -type f -name "*.yaml" -exec kubectl apply -f {} \;