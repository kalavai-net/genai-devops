import requests

BASE_URL = 'http://localhost:8000'
HEADERS = {'Authorization': 'Bearer sk--BnVfdA8bKzGPjr-JWYlzw'}


TOOLS = [
  {
    "type": "function",
    "function": {
      "name": "delete_nodes",
      "description": "Delete specified nodes from the pool",
      "parameters": {
        "type": "object",
        "properties": {
            "nodes": {
                "type": "array",
                "items": {
                    "type": "string"
                }
            }
        },
        "required": ["nodes"]
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "cordon_nodes",
      "description": "Mark nodes as unschedulable",
      "parameters": {
        "type": "object",
        "properties": {
            "nodes": {
                "type": "array",
                "items": {
                    "type": "string"
                }
            }
        },
        "required": ["nodes"]
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "uncordon_nodes",
      "description": "Mark nodes as schedulable",
      "parameters": {
        "type": "object",
        "properties": {
            "nodes": {
                "type": "array",
                "items": {
                    "type": "string"
                }
            }
        },
        "required": ["nodes"]
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "get_pool_token",
      "description": "Get a token for the pool",
      "parameters": {
        "type": "object",
        "properties": {
          "mode": {
            "type": "integer",
            "enum": [0, 1, 2],
            "description": "0 for admin, 1 for user, 2 for worker"
          }
        },
        "required": [
          "mode"
        ]
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "fetch_devices",
      "description": "Get list of available devices",
      "parameters": {
        "type": "object",
        "properties": {},
        "required": []
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "fetch_resources",
      "description": "Get available resources in the pool, like GPUs, CPUs and memory available",
      "parameters": {
        "type": "object",
        "properties": {},
        "required": []
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "fetch_job_names",
      "description": "Get list of jobs currently running in the pool",
      "parameters": {
        "type": "object",
        "properties": {},
        "required": []
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "fetch_gpus",
      "description": "Get list of GPUs connected to the pool",
      "parameters": {
        "type": "object",
        "properties": {
          "available": {
            "type": "boolean",
            "description": "True if only available GPUs are requested, False if all GPUs are requested"
          }
        },
        "required": []
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "fetch_job_logs",
      "description": "Get logs for a specific job to inspect how the job is running in the pool",
      "parameters": {
        "type": "object",
        "properties": {
          "job_name": {
            "type": "string",
            "description": "ID of the job to get logs for"
          },
        },
        "required": [
          "job_name"
        ]
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "fetch_job_defaults",
      "description": "Get default values for a job template to use for a new job",
      "parameters": {
        "type": "object",
        "properties": {
          "name": {
            "type": "string",
            "description": "Name of the job template to get default values for"
          }
        },
        "required": [
          "name"
        ]
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "deploy_job",
      "description": "Deploy a new job",
      "parameters": {
        "type": "object",
        "properties": {},
        "required": []
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "delete_job",
      "description": "Delete a job",
      "parameters": {
        "type": "object",
        "properties": {
            "name": {
                "type": "string",
                "description": "Name of the job to delete"
            }
        },
        "required": ["name"]
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "is_connected",
      "description": "Check if the agent is connected to a pool",
      "parameters": {
        "type": "object",
        "properties": {},
        "required": []
      }
    }
  }
]

def create_pool(**kwargs):
    print(f'create_pool called with {kwargs}')
    try:
        response = requests.request(
            method="post",
            url=f"{BASE_URL}/create_pool",
            headers=HEADERS,
            json=kwargs
        )
        response.raise_for_status()
        return f'create_pool called called with {kwargs}: {response.json()}'
    except Exception as e:
        return f'ERROR create_pool called called with {kwargs}: {str(e)}'

def join_pool(**kwargs):
    print(f'join_pool called with {kwargs}')
    try:
        response = requests.request(
            method="post",
            url=f"{BASE_URL}/join_pool",
            headers=HEADERS,
            json=kwargs
        )
        response.raise_for_status()
        return f'join_pool called called with {kwargs}: {response.json()}'
    except Exception as e:
        return f'ERROR join_pool called called with {kwargs}: {str(e)}'

def attach_to_pool(**kwargs):
    print(f'attach_to_pool called with {kwargs}')
    try:
        response = requests.request(
            method="post",
            url=f"{BASE_URL}/attach_to_pool",
            headers=HEADERS,
            json=kwargs
        )
        response.raise_for_status()
        return f'attach_to_pool called called with {kwargs}: {response.json()}'
    except Exception as e:
        return f'ERROR attach_to_pool called called with {kwargs}: {str(e)}'

def stop_pool(**kwargs):
    print(f'stop_pool called with {kwargs}')
    try:
        response = requests.request(
            method="post",
            url=f"{BASE_URL}/stop_pool",
            headers=HEADERS,
            json=kwargs
        )
        response.raise_for_status()
        return f'stop_pool called called with {kwargs}: {response.json()}'
    except Exception as e:
        return f'ERROR stop_pool called called with {kwargs}: {str(e)}'

def delete_nodes(**kwargs):
    print(f'delete_nodes called with {kwargs}')
    try:
        response = requests.request(
            method="post",
            url=f"{BASE_URL}/delete_nodes",
            headers=HEADERS,
            json=kwargs
        )
        response.raise_for_status()
        return f'delete_nodes called called with {kwargs}: {response.json()}'
    except Exception as e:
        return f'ERROR delete_nodes called called with {kwargs}: {str(e)}'

def cordon_nodes(**kwargs):
    print(f'cordon_nodes called with {kwargs}')
    try:
        response = requests.request(
            method="post",
            url=f"{BASE_URL}/cordon_nodes",
            headers=HEADERS,
            json=kwargs
        )
        response.raise_for_status()
        return f'cordon_nodes called called with {kwargs}: {response.json()}'
    except Exception as e:
        return f'ERROR cordon_nodes called called with {kwargs}: {str(e)}'

def uncordon_nodes(**kwargs):
    print(f'uncordon_nodes called with {kwargs}')
    try:
        response = requests.request(
            method="post",
            url=f"{BASE_URL}/uncordon_nodes",
            headers=HEADERS,
            json=kwargs
        )
        response.raise_for_status()
        return f'uncordon_nodes called called with {kwargs}: {response.json()}'
    except Exception as e:
        return f'ERROR uncordon_nodes called called with {kwargs}: {str(e)}'

def get_pool_token(**kwargs):
    print(f'get_pool_token called with {kwargs}')
    try:
        response = requests.request(
            method="get",
            url=f"{BASE_URL}/get_pool_token",
            headers=HEADERS,
            params=kwargs
        )
        response.raise_for_status()
        return f'get_pool_token called called with {kwargs}: {response.json()}'
    except Exception as e:
        return f'ERROR get_pool_token called called with {kwargs}: {str(e)}'

def fetch_devices(**kwargs):
    print(f'fetch_devices called with {kwargs}')
    try:
        response = requests.request(
            method="get",
            url=f"{BASE_URL}/fetch_devices",
            headers=HEADERS,
            params=kwargs
        )
        response.raise_for_status()
        return f'fetch_devices called called with {kwargs}: {response.json()}'
    except Exception as e:
        return f'ERROR fetch_devices called called with {kwargs}: {str(e)}'

def send_pool_invites(**kwargs):
    print(f'send_pool_invites called with {kwargs}')
    try:
        response = requests.request(
            method="post",
            url=f"{BASE_URL}/send_pool_invites",
            headers=HEADERS,
            json=kwargs
        )
        response.raise_for_status()
        return f'send_pool_invites called called with {kwargs}: {response.json()}'
    except Exception as e:
        return f'ERROR send_pool_invites called called with {kwargs}: {str(e)}'

def fetch_resources(**kwargs):
    print(f'fetch_resources called with {kwargs}')
    try:
        response = requests.request(
            method="get",
            url=f"{BASE_URL}/fetch_resources",
            headers=HEADERS,
            params=kwargs
        )
        response.raise_for_status()
        return f'fetch_resources called called with {kwargs}: {response.json()}'
    except Exception as e:
        return f'ERROR fetch_resources called called with {kwargs}: {str(e)}'

def fetch_job_names(**kwargs):
    print(f'fetch_job_names called with {kwargs}')
    try:
        response = requests.request(
            method="get",
            url=f"{BASE_URL}/fetch_job_names",
            headers=HEADERS,
            params=kwargs
        )
        response.raise_for_status()
        return f'fetch_job_names called called with {kwargs}: {response.json()}'
    except Exception as e:
        return f'ERROR fetch_job_names called called with {kwargs}: {str(e)}'

def fetch_gpus(**kwargs):
    print(f'fetch_gpus called with {kwargs}')
    try:
        response = requests.request(
            method="get",
            url=f"{BASE_URL}/fetch_gpus",
            headers=HEADERS,
            params=kwargs
        )
        response.raise_for_status()
        return f'fetch_gpus called called with {kwargs}: {response.json()}'
    except Exception as e:
        return f'ERROR fetch_gpus called called with {kwargs}: {str(e)}'

def fetch_job_details(**kwargs):
    print(f'fetch_job_details called with {kwargs}')
    try:
        response = requests.request(
            method="post",
            url=f"{BASE_URL}/fetch_job_details",
            headers=HEADERS,
            json=kwargs
        )
        response.raise_for_status()
        return f'fetch_job_details called called with {kwargs}: {response.json()}'
    except Exception as e:
        return f'ERROR fetch_job_details called called with {kwargs}: {str(e)}'

def fetch_job_logs(**kwargs):
    print(f'fetch_job_logs called with {kwargs}')
    try:
        response = requests.request(
            method="get",
            url=f"{BASE_URL}/fetch_job_logs",
            headers=HEADERS,
            params=kwargs
        )
        response.raise_for_status()
        return f'fetch_job_logs called called with {kwargs}: {response.json()}'
    except Exception as e:
        return f'ERROR fetch_job_logs called called with {kwargs}: {str(e)}'

def fetch_job_templates(**kwargs):
    print(f'fetch_job_templates called with {kwargs}')
    try:
        response = requests.request(
            method="get",
            url=f"{BASE_URL}/fetch_job_templates",
            headers=HEADERS,
            params=kwargs
        )
        response.raise_for_status()
        return f'fetch_job_templates called called with {kwargs}: {response.json()}'
    except Exception as e:
        return f'ERROR fetch_job_templates called called with {kwargs}: {str(e)}'

def fetch_job_defaults(**kwargs):
    print(f'fetch_job_defaults called with {kwargs}')
    try:
        response = requests.request(
            method="get",
            url=f"{BASE_URL}/fetch_job_defaults",
            headers=HEADERS,
            params=kwargs
        )
        response.raise_for_status()
        return f'fetch_job_defaults called called with {kwargs}: {response.json()}'
    except Exception as e:
        return f'ERROR fetch_job_defaults called called with {kwargs}: {str(e)}'

def deploy_job(**kwargs):
    print(f'deploy_job called with {kwargs}')
    try:
        response = requests.request(
            method="post",
            url=f"{BASE_URL}/deploy_job",
            headers=HEADERS,
            json=kwargs
        )
        response.raise_for_status()
        return f'deploy_job called called with {kwargs}: {response.json()}'
    except Exception as e:
        return f'ERROR deploy_job called called with {kwargs}: {str(e)}'

def delete_job(**kwargs):
    print(f'delete_job called with {kwargs}')
    try:
        response = requests.request(
            method="post",
            url=f"{BASE_URL}/delete_job",
            headers=HEADERS,
            json=kwargs
        )
        response.raise_for_status()
        return f'delete_job called called with {kwargs}: {response.json()}'
    except Exception as e:
        return f'ERROR delete_job called called with {kwargs}: {str(e)}'

def authenticate_user(**kwargs):
    print(f'authenticate_user called with {kwargs}')
    try:
        response = requests.request(
            method="get",
            url=f"{BASE_URL}/authenticate_user",
            headers=HEADERS,
            params=kwargs
        )
        response.raise_for_status()
        return f'authenticate_user called called with {kwargs}: {response.json()}'
    except Exception as e:
        return f'ERROR authenticate_user called called with {kwargs}: {str(e)}'

def load_user_session(**kwargs):
    print(f'load_user_session called with {kwargs}')
    try:
        response = requests.request(
            method="get",
            url=f"{BASE_URL}/load_user_session",
            headers=HEADERS,
            params=kwargs
        )
        response.raise_for_status()
        return f'load_user_session called called with {kwargs}: {response.json()}'
    except Exception as e:
        return f'ERROR load_user_session called called with {kwargs}: {str(e)}'

def user_logout(**kwargs):
    print(f'user_logout called with {kwargs}')
    try:
        response = requests.request(
            method="get",
            url=f"{BASE_URL}/user_logout",
            headers=HEADERS,
            params=kwargs
        )
        response.raise_for_status()
        return f'user_logout called called with {kwargs}: {response.json()}'
    except Exception as e:
        return f'ERROR user_logout called called with {kwargs}: {str(e)}'

def is_connected(**kwargs):
    print(f'is_connected called with {kwargs}')
    try:
        response = requests.request(
            method="get",
            url=f"{BASE_URL}/is_connected",
            headers=HEADERS,
            params=kwargs
        )
        response.raise_for_status()
        return f'is_connected called called with {kwargs}: {response.json()}'
    except Exception as e:
        return f'ERROR is_connected called called with {kwargs}: {str(e)}'
