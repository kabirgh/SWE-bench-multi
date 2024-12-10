import os
import json
from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse, JSONResponse
from datetime import datetime, timedelta

app = FastAPI()

# Add cache dictionary and cache duration at the top level
instances_cache = {}
CACHE_DURATION = timedelta(minutes=30)  # Adjust duration as needed


@app.get("/")
def root():
    return FileResponse("pr_explorer.html", status_code=200)


@app.get("/list_files")
def list_files():
    repos = []
    for root, _dirs, files in os.walk("dataset"):
        for file in files:
            if (
                file.endswith("-task-instances.jsonl")
                and os.path.basename(root) != "dataset"
            ):
                repo_name = os.path.basename(root)
                repos.append(repo_name)
    return JSONResponse(content=repos)


@app.get("/instances/{repo}")
def get_instances(repo: str):
    # Check cache first
    if repo in instances_cache:
        cache_data, cache_time = instances_cache[repo]
        if datetime.now() - cache_time < CACHE_DURATION:
            return JSONResponse(content=cache_data)

    # If not in cache or expired, read from file
    file_path = f"dataset/{repo}/{repo}-task-instances.jsonl"
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="Repository not found")

    with open(file_path, "r") as f:
        instances_data = [json.loads(line.strip()) for line in f]
        response_data = {
            "repository": instances_data[0]["repo"]
            if instances_data and len(instances_data) > 0
            else "No instances found",
            "repo_short": repo,
            "issues": instances_data,
        }

    # Store in cache with timestamp
    instances_cache[repo] = (response_data, datetime.now())
    return JSONResponse(content=response_data)
