---
name: workshop1-docker-compose
description: >-
  Starts every Docker Compose stack in the Workshop 1 (wrk1) repo, or stops
  one named container without taking the rest down. Use when the user says
  bring up all containers in wrk1, start all docker-compose files in Workshop 1,
  or bring down a certain container alone.
---

# Workshop 1 Docker Compose

Use this skill when the user wants Docker containers from the **Workshop 1** repo (`wrk1`) brought **up** (all compose files) or **down** (one container only).

Do not change Workshop 2 `myworld/` or other workshops unless the user asked.

## Find the Workshop 1 repo

Resolve the Workshop 1 root in this order:

1. Path the user gave (folder name, `wrk1`, `Workshop 1`, `DataEngineering-Workshop1`).
2. Sibling of this Workshop 2 repo: `../DataEngineering-Workshop1` (or similar name on disk).
3. If still missing, ask for the full path. Do not invent a repo.

Confirm the root exists before running Docker.

## Discover compose files

From the Workshop 1 root, find every `docker-compose.yml` and `docker-compose.yaml` (also `compose.yml` / `compose.yaml` if present).

Skip copies under `.git`, `node_modules`, `__pycache__`, and `broken/` (drill fixtures).

Prefer `docker compose` (space). If that fails, use `docker-compose` (hyphen).

## Bring up all containers

When the user asks to **bring up all containers** in wrk1 / start **all docker compose files**:

1. List the compose files you will start.
2. For each file, run from that file’s directory:

```bash
docker compose -f docker-compose.yml up -d
```

Use the real filename if it is not `docker-compose.yml`. If several compose files share one folder, pass each `-f` as needed.

3. Wait briefly, then show `docker compose ps` (per stack) or `docker ps` so the user can see what is running.
4. If a stack fails, report that file/path and the error; continue with the others when safe.

Do **not** use `down -v` as part of bring-up.

## Bring down one container only

When the user asks to **bring down a certain container alone** (one name):

1. Identify the target as a **container name**, **Compose service name**, or short unique prefix. If several match, list them and stop only after the user picks one.
2. Stop **only that container**. Do **not** run `docker compose down` (that stops every service in the file). Do **not** use `-v` unless the user asked to delete volumes.

Preferred:

```bash
docker stop <container_name>
```

If they named a Compose **service** and you know which compose file:

```bash
docker compose -f <compose-file> stop <service_name>
```

3. Confirm with `docker ps` that the named container is gone/exited and **other** wrk1 containers are still running.

## Commands the user can say

- “Bring up all containers in wrk1 repo”
- “Start every docker-compose file in Workshop 1”
- “Bring down container `<name>` alone”
- “Stop only `<service>` in wrk1”

## Important

- Operate on **Workshop 1** paths only.
- Bring-up = every discovered compose file, detached (`-d`).
- Bring-down = one container or one service, not the whole stack.
- Keep explanations short and beginner-friendly.
