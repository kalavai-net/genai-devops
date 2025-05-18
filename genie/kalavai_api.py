import requests
import os

POOL_URL = "http://hackathon.kalavai.net:8001"
COMPUTE_API_URL = "http://localhost:8000"
API_KEY = os.getenv("KALAVAI_API_KEY")
USER_ID = API_KEY
JOIN_TOKEN = os.getenv("KALAVAI_JOIN_TOKEN")
HF_TOKEN = os.getenv("HF_TOKEN")
LITELLM_KEY = os.getenv("LITELLM_KEY")


def _request_server(url, method, data=None, json=None, params=None):
    headers = {
        "X-API-KEY": API_KEY,
        "Content-Type": "application/json"
    }
    
    response = requests.request(method, url, headers=headers, data=data, json=json, params=params)
    response.raise_for_status()
    return response.json()


def get_pool_resources():
    url = f"{POOL_URL}/fetch_resources"
    return _request_server(url, "GET")

def get_models():
    url = f"{POOL_URL}/fetch_job_names"
    model_data = _request_server(url, "GET")
    details = _request_server(f"{POOL_URL}/fetch_job_details", "POST", json={"jobs": model_data})
    return details
    
def add_gpu_devices(node_name: str):
    cloud_init = f"""
#cloud-config
package_update: true
packages:
  - python3-virtualenv
  - ca-certificates
  - curl

write_files:
  - path: /usr/local/bin/first-boot.sh
    permissions: '0755'
    content: |
      #!/bin/bash
      if [ ! -f /etc/first-boot-done ]; then
        echo "Running first-boot setup..."

        # Create the required directory for Docker's keyrings
        install -m 0755 -d /etc/apt/keyrings

        # Add Docker's official GPG key
        curl -fsSL https://download.docker.com/linux/ubuntu/gpg -o /etc/apt/keyrings/docker.asc
        chmod a+r /etc/apt/keyrings/docker.asc

        # Add the Docker repository
        echo "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.asc] https://download.docker.com/linux/ubuntu $(. /etc/os-release && echo \"${{UBUNTU_CODENAME:-$VERSION_CODENAME}}\") stable" | tee /etc/apt/sources.list.d/docker.list > /dev/null

        # Update package lists and install Docker
        apt-get update
        apt-get install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin

        # install kalavai
        virtualenv -p python3 ~/kalavai
        source ~/kalavai/bin/activate && pip install kalavai-client==0.6.10
        source ~/kalavai/bin/activate && kalavai auth {USER_ID}
        source ~/kalavai/bin/activate && kalavai pool join {JOIN_TOKEN} --non-interactive

        # Mark first-boot complete
        touch /etc/first-boot-done
      fi

runcmd:
  - while [ ! -f /usr/bin/nvidia-smi ]; do sleep 5; done
  - bash /usr/local/bin/first-boot.sh  # Ensure first-boot tasks run once
    """
    
    # Prepare the request payload
    payload = {
        "name": node_name,
        "instance_type": "gpu_small",
        "image_id": "projects/deeplearning-platform-release/global/images/family/common-cu124-ubuntu-2204-py310-conda",
        "tag": "kalavai-node",
        "region": "us-central1-c",
        "cloud_init": cloud_init,
        "disk_size": 100
    }
    
    # Add region as query parameter if provided
    params = {"region": "us-central1-c"}
    
    response = _request_server(
        f"{COMPUTE_API_URL}/instances",
        "POST",
        json=payload,
        params=params)
    return response

def list_gpus():
    url = f"{POOL_URL}/fetch_gpus"
    return _request_server(url, "GET")

def create_model(model_id: str, num_gpus: int=1):
    url = f"{POOL_URL}/deploy_job"
    payload = {
        "template_name": "vllm",
        "values": {
            "model_id": model_id,
            "workers": num_gpus,
            "hf_token": HF_TOKEN,
            "pipeline_parallel_size": num_gpus,
            "litellm_key": LITELLM_KEY
        }
    }
    return _request_server(url, "POST", json=payload)

def delete_model(model_id: str):
    url = f"{POOL_URL}/delete_job"
    return _request_server(url, "POST", json={"name": model_id})
