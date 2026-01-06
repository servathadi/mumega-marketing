"""
GitHub App Authentication Utility
Generates installation tokens for Mumega-Agent.
"""

import time
import jwt
import requests
import os
import logging

logger = logging.getLogger("github_auth")

def get_installation_token(app_id: str, private_key: str, repo_owner: str, repo_name: str) -> str:
    """
    Generate a GitHub App Installation Token for a specific repo.
    """
    # 1. Create JWT (JSON Web Token)
    now = int(time.time())
    payload = {
        "iat": now - 60,
        "exp": now + (10 * 60), # 10 minute expiration
        "iss": app_id
    }
    encoded_jwt = jwt.encode(payload, private_key, algorithm="RS256")

    # 2. Get Installation ID for the repo
    headers = {
        "Authorization": f"Bearer {encoded_jwt}",
        "Accept": "application/vnd.github.v3+json"
    }
    
    url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/installation"
    resp = requests.get(url, headers=headers)
    
    if resp.status_code != 200:
        logger.error(f"Failed to find installation: {resp.text}")
        raise Exception(f"GitHub App not installed on {repo_owner}/{repo_name}")
        
    installation_id = resp.json()["id"]

    # 3. Create Access Token
    token_url = f"https://api.github.com/app/installations/{installation_id}/access_tokens"
    token_resp = requests.post(token_url, headers=headers)
    
    if token_resp.status_code != 201:
        raise Exception(f"Failed to create token: {token_resp.text}")
        
    return token_resp.json()["token"]
