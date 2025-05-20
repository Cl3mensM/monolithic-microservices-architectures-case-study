# Check project
echo "Check that you are connected to the right project"
gcloud config set project ba-microservice
gcloud info
echo "Correct project?"
read -p "Press enter to continue"

# Add containers to GCR
echo "Add containers to GCR"
cd microservice_architecture/arrival_times_service
docker buildx build --platform linux/amd64,linux/arm64 \
    -t gcr.io/ba-microservice/arrival_times_service:latest \
    --push .
cd ../disruption_service
docker buildx build --platform linux/amd64,linux/arm64 \
    -t gcr.io/ba-microservice/disruption_service:latest \
    --push .
cd ../routing_service
docker buildx build --platform linux/amd64,linux/arm64 \
    -t gcr.io/ba-microservice/routing_service-routing:latest \
    --push .
cd ../db_abstraction_service
docker buildx build --platform linux/amd64,linux/arm64 \
    -t gcr.io/ba-microservice/db-abstraction_service:latest \
    --push .

# Create GKE cluster
gcloud container clusters create-auto microservice \
    --region=europe-west4

# Get credentials for the cluster
gcloud container clusters get-credentials microservice \
    --region=europe-west4

# Apply Ingress nginx controller
echo "Apply Ingress nginx controller"
kubectl apply -f https://raw.githubusercontent.com/kubernetes/ingress-nginx/controller-v1.10.0/deploy/static/provider/cloud/deploy.yaml

# Apply Kubernetes YAMLs
echo "Apply Kubernetes YAMLs"
cd ../../microservice_kubernetes/GKE
find . -type f -name "*.yaml" -exec kubectl apply -f {} \;
