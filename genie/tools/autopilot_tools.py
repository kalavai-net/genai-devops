from kalavai_api import (
    get_pool_resources,
    get_models,
    #add_gpu_devices,
    list_gpus,
    create_model,
    delete_model
)

POOL_URL = "http://hackathon.kalavai.net:3000"
GCP_URL = "https://console.cloud.google.com/compute/instances?inv=1&invt=AbxukQ&organizationId=1030585665541&project=kalavai&rapt=AEjHL4PDdc2YNcYg67OaeIocynOWo9EnJUivCtfIELq8rUjPTlCPabpg20wJXOF3O6sjKcm7CDWA_4dOMC7gNlP-3F3joXKbQLyKc9tQeO42c-TrvYg1EZ0"

TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "display_dashboard",
            "description": "Display the dashboard UI of the pool so the user can see the details of the computing pool",
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
            "name": "list_models",
            "description": "List all the models deployed in the pool",
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
            "name": "deploy_model",
            "description": "Deploy an AI model to our pool",
            "parameters": {
                "type": "object",
                "properties": {
                    "model_id": {"type": "string", "description": "The model ID from hugginface to deploy"},
                    "num_gpus": {"type": "integer", "description": "The number of GPUs to deploy the model to"}
                },
                "required": ["model_id"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "remove_model",
            "description": "Delete an AI model from our pool once is no longer needed",
            "parameters": {
                "type": "object",
                "properties": {
                    "model_id": {"type": "string", "description": "The model ID from our pool to delete"},
                },
                "required": ["model_id"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_available_resources",
            "description": "Get the available resources, such as number of devices, CPUs or RAM memory in our pool",
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
            "name": "get_available_gpus",
            "description": "Get a list of available GPUs in the pool",
            "parameters": {
                "type": "object",
                "properties": {},
                "required": []
            }
        }
    },
    # {
    #     "type": "function",
    #     "function": {
    #         "name": "add_gpus",
    #         "description": "Add GPUs to our pool",
    #         "parameters": {
    #             "type": "object",
    #             "properties": {
    #                 "node_name": {"type": "string", "description": "The name of the GPU node to add to the pool"}
    #             },
    #             "required": ["node_name"]
    #         }
    #     }
    # },
    {
        "type": "function",
        "function": {
            "name": "show_how_to",
            "description": "Display instructions onhow to connect to models in the pool",
            "parameters": {
                "type": "object",
                "properties": {
                    "model_id": {"type": "string", "description": "The model ID to connect to"},
                    "language": {"type": "string", "enum": ["python", "curl"], "description": "The language to use to connect to the model"}
                },
                "required": ["model_id"]
            }
        }
    }
]


def show_how_to(model_id: str, language: str="python"):
    models = get_models()
    address = None
    for model in models:
        if model["name"] == "litellm":
            address = model["endpoint"]
            break
    if language == "python":
        response = """
    To connect to a model in the pool, you can use the following python snippet:
    ```
import requests
import json

API_KEY = "<your-api-key>"  # Replace with your actual API key

response = requests.post(
    "<MODEL_ENDPOINT>/v1/completions",
    headers={"Authorization": f"Bearer {API_KEY}"},
    json={
        "model": "<MODEL_ID",
        "prompt": "What's the meaning of life?",
        "max_tokens": 1000
    }
).json()

print(
    json.dumps(response, indent=2)
) 
    ```
    """ + f"Replace <MODEL_ID> with the model ID {model_id}, and <MODEL_ENDPOINT> with the endpoint {address}"
    elif language == "curl":
        response = """
    To connect to a model in the pool, you can use the following curl command:
    ```
curl -X POST '<MODEL_ENDPOINT>/v1/completions' \
  -H 'Content-Type: application/json' \
  -H 'Authorization: Bearer <your-api-key>' \
  -d '{
    "model": "<MODEL_ID>",
    "prompt": "What is the meaning of life?",
    "max_tokens": 1000
}' """
        
    return response + f"\nReplace <MODEL_ID> with the model ID {model_id}, and <MODEL_ENDPOINT> with the endpoint {address}"


def display_dashboard():
    return f"Sure, you can access it here: {POOL_URL}"

def list_models():
    models = get_models()
    if len(models) == 0:
        return "No models deployed in our pool"
    else:
        return f"Here's a list of the models deployed in our pool:\n\n{models}. Format them as a table."

def deploy_model(model_id: str, num_gpus: int=1):
    result = create_model(model_id, num_gpus)
    return f"Deploying model {model_id}\n\nSee the progress: {POOL_URL}/jobs"

def remove_model(model_id: str):
    result = delete_model(model_id)
    return f"Deleting model {model_id}...{result}\n\nSee the progress: {POOL_URL}/jobs"

def get_available_resources():
    resources = get_pool_resources()
    return f"Here are the resources: {resources}. Format them as a table with the following columns: nodes, GPU, CPU, RAM"

def get_available_gpus():
    gpus = list_gpus()
    if len(gpus) == 0:
        return "No GPUs available in the pool"
    else:
        return f"Here are the available GPUs: {gpus}. Format them as a table."

# def add_gpus(node_name: str):
#     result = add_gpu_devices(node_name)
#     return f"GPUs added. It may take a few minutes to boot up\n\nSee the progress: {GCP_URL}"
