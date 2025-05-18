import json


def map_openapi_to_function(spec,short_name:str=None):
    """Map an OpenAPI endpoint spec to a function ala open AI
       you can add functions from this to the tool format with for example
       
       ```python
       fns = [map_openai_to_function(openpi_spec_json['/weather']['get'])]
       tools = [{'type': 'function', 'function': f} for f in fns]
       ```
       
       TODO: create a pydantic model for this but for now im just trying to understand it and see who complains
    """
    def _map(schema):
        """
        Recursively map the parameters containing schema to a flatter representation,
        retaining only 'type', 'description', and optional 'enum' in nested types.
        """
        if 'schema' in schema:
            schema = schema['schema']
        mapped_schema = {
            'type': schema.get('type'),
            'description': schema.get('description', '')  
        }
        
        if 'enum' in schema:
            mapped_schema['enum'] = schema['enum']

        if schema.get('type') == 'array' and 'items' in schema:
            mapped_schema['items'] = _map(schema['items'])

        if schema.get('type') == 'object' and 'properties' in schema:
            mapped_schema['properties'] = {k: _map(v) for k, v in schema['properties'].items()}

        return mapped_schema
        
    try:
        r =  {
            'name': short_name or (spec.get('operationId') or spec.get('title')),
            'description': spec.get('description') or spec.get('summary'),
            'parameters' : {
                'type': 'object',
                'properties': {p['name']:_map(p) for p in (spec.get('parameters') or [])},
                'required': [p['name'] for p in spec.get('parameters') or [] if p.get('required')]
            } 
        }
    except:
        print(f"Failing to parse {spec=}")
        raise
    return r

if __name__ == "__main__":
    with open('openapi.json', 'r') as f:
        openapi_spec_json = json.load(f)
    
    tools = []
    with open('tools.py', 'w') as f:
        f.write("import requests\n\nBASE_URL = 'https://api.cogenai.kalavai.net'\nHEADERS = {'Authorization': 'Bearer YOUR_TOKEN'}\n\n")
        for path, methods in openapi_spec_json["paths"].items():
            for method, spec in methods.items():
                fns = [map_openapi_to_function(spec,short_name=path.replace('/', ''))]
                for fn in fns:
                    tools.append({'type': 'function', 'function': fn})
                    if method == "get":
                        f.write(f"""
def {fn['name']}(**kwargs):
    print(f'{fn['name']} called with {{kwargs}}')
    try:
        response = requests.request(
            method="{method}",
            url=f"{{BASE_URL}}{path}",
            headers=HEADERS,
            params=kwargs
        )
        response.raise_for_status()
        return f'{fn['name']} called called with {{kwargs}}: {{response.json()}}'
    except Exception as e:
        return f'ERROR {fn['name']} called called with {{kwargs}}: {{str(e)}}'
""")
                    elif method == "post":
                        f.write(f"""
def {fn['name']}(**kwargs):
    print(f'{fn['name']} called with {{kwargs}}')
    try:
        response = requests.request(
            method="{method}",
            url=f"{{BASE_URL}}{path}",
            headers=HEADERS,
            json=kwargs
        )
        response.raise_for_status()
        return f'{fn['name']} called called with {{kwargs}}: {{response.json()}}'
    except Exception as e:
        return f'ERROR {fn['name']} called called with {{kwargs}}: {{str(e)}}'
""")
                    elif method == "delete":
                        f.write(f"""
def {fn['name']}(**kwargs):
    print(f'{fn['name']} called with {{kwargs}}')
    try:
        response = requests.request(
            method="{method}",
            url=f"{{BASE_URL}}{path}",
            headers=HEADERS,
            params=kwargs
        )
        response.raise_for_status()
        return f'{fn['name']} called called with {{kwargs}}: {{response.json()}}'
    except Exception as e:
        return f'ERROR {fn['name']} called called with {{kwargs}}: {{str(e)}}'
""")
        formatted_tool = json.dumps(tools, indent=2)
        f.write(f"\n\nTOOLS = {formatted_tool}")



