# List available commands
default:
    @just --list

# Build with nixpacks
nixpack:
    nixpacks build .

# Build with Docker using buildx
docker:
    docker buildx create --name dokploy-preview-deployments-demo-buildx
    docker buildx build --builder dokploy-preview-deployments-demo-buildx -t dokploy-custom .