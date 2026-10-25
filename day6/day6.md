# Day 6: Push Image to Azure Container Registry (ACR)

## What I did
- Set up a personal Azure subscription with a **$20/month budget alert** (50/80/100%)
- Installed the Azure CLI and signed in with `az login`
- Created resource group `rg-ai-infra-lab` in `southcentralus`
- Created a Basic-tier ACR registry
- Tagged and pushed my API image, pulled it back, and ran it through Compose

## Key concepts
- **Container registry**: A storage service for images, like GitHub for containers. AKS pulls images from here.
- **Image name format**: `<registry>/<repository>:<tag>`, e.g. `tejaaiinfralab01.azurecr.io/myapi:v1`
- **`docker tag`**: Adds a second name to an existing image; nothing is copied, same IMAGE ID.
- **`az acr login`**: Uses my Azure sign-in to give Docker a temporary token (~3 hours), with no password stored.
- **Resource group**: A folder for related resources; deleting it deletes everything inside.
- **ACR names**: Globally unique, 5–50 letters and numbers, no dashes.

## Tagging
- Avoid relying on `latest`: it changes over time, so you can't tell what's actually running.
- Tag with versions (`v1`) and the Git commit (`git rev-parse --short HEAD`) to link each image to exact code.

## What I observed
- Second push of the same image said **"Layer already exists"** for every layer: registries reuse layers, same caching idea as Day 2.
- Deleted the local image, pulled from ACR, and ran it with Compose using `image:` instead of `build:`. This is how AKS will run it.

## Key commands
- `az group create --name rg-ai-infra-lab --location southcentralus`
- `az acr create --resource-group rg-ai-infra-lab --name <acr> --sku Basic`
- `az acr login --name <acr>`
- `docker tag myapi:day5 <acr>.azurecr.io/myapi:v1`
- `docker push <acr>.azurecr.io/myapi:v1`
- `az acr repository show-tags --name <acr> --repository myapi --output table`
- Cleanup (when needed): `az group delete --name rg-ai-infra-lab --yes`

## Gotchas
- `unauthorized` on push → token expired; run `az acr login` again.
- PowerShell variables like `$ACR` disappear in a new terminal.
- Use a personal subscription for learning, never the work one.

## Next
Day 7: Compose with API, Postgres, and Redis cache, and push `myapi:v2` to ACR.