# Day 4: Environment Variables and Volumes

## Key concepts
- **`-e`**: Sets one environment variable when starting a container (`-e APP_NAME="Teja Platform"`), overriding the Dockerfile's `ENV` default.
- **`--env-file`**: Loads many environment variables from a file (`--env-file .env`); the file must stay out of Git and the image.
- **Named volume**: Docker-managed storage (`-v appdata:/data`) that lives outside the container, so data survives when the container is deleted; used for databases and app data.
- **Bind mount**: Links a folder on my laptop into the container (`-v ${PWD}/app:/code/app`) so code edits show up without a rebuild; for development only, never production.

## What I observed
- Same image showed different messages and environments just by changing `-e` values.
- Visit count reset to 1 after recreating the container without a volume, and survived with `appdata` mounted.

## Issue I hit and fixed
- `/visits` returned 500 with `PermissionError: [Errno 13] Permission denied: '/data'`.
- Cause: the app runs as non-root `appuser`, which can't create folders in `/` (owned by root).
- Fix: added `RUN mkdir /data && chown appuser:appuser /data` **before** `USER appuser` in the Dockerfile.
- Lesson: with non-root containers, explicitly give the app ownership of any folder it writes to.

## Precedence (strongest first)
`-e` / `--env-file` → Dockerfile `ENV` → default in `os.getenv()`

## Next
Real secrets (passwords, API keys) don't belong in env vars or `.env` files. Azure Key Vault is covered on Day 23.