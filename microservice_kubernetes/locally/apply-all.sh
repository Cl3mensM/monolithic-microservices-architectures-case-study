#!/bin/bash

# Apply all YAML files in subdirectories
find . -type f -name "*.yaml" -exec kubectl apply -f {} \;

echo ""
echo "All YAML files have been applied."