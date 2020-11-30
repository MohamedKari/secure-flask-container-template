"""
Installation:
```
bash <(curl -S https://gist.githubusercontent.com/MohamedKari/d6a2a7a6cdfe5aee32a6c8eefd6029be/raw/gh-secrets.sh)
source .gh-secrets/bin/activate
```
"""
import os
from base64 import b64encode
import json
import subprocess
from pathlib import Path
from typing import Tuple

import fire
import dotenv
from nacl import encoding, public
import requests
from requests import Response

dotenv.load_dotenv()

class Secrets():

    def __init__(self) -> None:
        self.github_token = os.getenv("GITHUB_TOKEN")

    def _encrypt(self, public_key: str, secret_value: str) -> str:
        public_key = public.PublicKey(public_key.encode("utf-8"), encoding.Base64Encoder())
        sealed_box = public.SealedBox(public_key)
        encrypted = sealed_box.encrypt(secret_value.encode("utf-8"))
        return b64encode(encrypted).decode("utf-8")

    def _get_public_key(self, repo_owner, repo_name) -> Tuple[str, str]:
        key_data = requests.get(
        f"https://api.github.com/repos/{repo_owner}/{repo_name}/actions/secrets/public-key",
        headers={
            "Authorization": f"token {self.github_token}"
        }
        ).json()

        return key_data["key_id"], key_data["key"]

    def _to_string(self, resp: Response) -> str:
        if resp.text in ["", None]:
            return ""

        return json.dumps((resp.json()), indent=4, default=str)

    def list(self, repo_owner: str, repo_name: str) -> str:
        response = requests.get(
            f"https://api.github.com/repos/{repo_owner}/{repo_name}/actions/secrets",
            headers={
                "Authorization": f"token {self.github_token}"
            }
        )

        return self._to_string(response)

    def get(self, repo_owner: str, repo_name: str, secret_name) -> str:
        response = requests.get(
            f"https://api.github.com/repos/{repo_owner}/{repo_name}/actions/secrets/{secret_name}",
            headers={
                "Authorization": f"token {self.github_token}"
            }
        )

        return self._to_string(response)
        

    def set(self, repo_owner: str, repo_name: str, secret_name: str, secret_value: str) -> str:
        key_id, key = self._get_public_key(repo_owner, repo_name)
        encrypted_value = self._encrypt(key, secret_value)

        response = requests.put(
            f"https://api.github.com/repos/{repo_owner}/{repo_name}/actions/secrets/{secret_name}",
            headers={
                "Content-Type": "application/json",
                "Authorization": f"token {self.github_token}"
            },
            data=json.dumps({
                "encrypted_value": encrypted_value,
                "key_id": key_id
            })
        )

        return self._to_string(response)

    def deploy_docker_machine_certs(self, repo_owner: str, repo_name: str, docker_machine_name: str) -> str:
        command = [f"docker-machine", "config", docker_machine_name]
        try:
            output = subprocess.check_output(command).decode("utf-8")
        except Exception as e:            
            print(e)
            print("\n\n--------------")
            raise e

        configs = output.split("\n")

        ca_path, cert_path, key_path, docker_host = None, None, None, None
        for config in configs:
            if config.startswith("--tlscacert="):
                ca_path = config.split("=")[1].strip("\"")
            elif config.startswith("--tlscert="):
                cert_path = config.split("=")[1].strip("\"")
            elif config.startswith("--tlskey="):
                key_path = config.split("=")[1].strip("\"")
            elif config.startswith("-H="):
                docker_host = config.split("=")[1]
        
        ca_string, cert_string, key_string = \
            Path(ca_path).read_text(), Path(cert_path).read_text(), Path(key_path).read_text()

        print(ca_string)

        return \
            self.set(repo_owner, repo_name, "CA", ca_string), \
            self.set(repo_owner, repo_name, "CERT", cert_string), \
            self.set(repo_owner, repo_name, "KEY", key_string), \
            self.set(repo_owner, repo_name, "DOCKER_HOST", docker_host)
  

if __name__ == "__main__":
    fire.Fire(Secrets)