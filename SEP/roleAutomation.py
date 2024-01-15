### Understand the program
### Ensure the program works
### Refactor the program
    ### Role, Mask, Mapping if exists.
import json
import requests
from bravado.requests_client import RequestsClient
from bravado.client import SwaggerClient
import os


def check_if_role_exists(name, base_url,auth_header):
    os.environ['REQUESTS_CA_BUNDLE'] = '/Users/saravanan.prasadh/Library/Application Support/mkcert/rootCA.pem'
    http_client = RequestsClient()
    http_client.session.headers.update(auth_header)
    api_instance=SwaggerClient.from_url(f'{base_url}/api/v1/biac/roles', http_client=http_client)

    try:
        api_response = api_instance.list_roles()
        print(api_response)
        for role in api_response:
            if role['name']==name:
                return role['id']
        return False
    except Exception as e:
        print('Exception when calling RolesApi')

def check_if_maskexpression_exists(name, base_url,auth_header):
    os.environ['REQUESTS_CA_BUNDLE'] = '/Users/saravanan.prasadh/Library/Application Support/mkcert/rootCA.pem'
    http_client = RequestsClient()
    http_client.session.headers.update(auth_header)
    api_instance=SwaggerClient.from_url(f'{base_url}/api/v1/biac/expressions/columnMask', http_client=http_client)
    try:
        api_response = api_instance.list_column_mask_expressions()
        print(api_response)
        for me in api_response:
            if me['name']==name:
                return me['id']
        return False
    except Exception as e:
        print('Exception when calling expressionsApi')


def delete_role(id, base_url,auth_header):
    os.environ['REQUESTS_CA_BUNDLE'] = '/Users/saravanan.prasadh/Library/Application Support/mkcert/rootCA.pem'
    http_client = RequestsClient()
    http_client.session.headers.update(auth_header)
    api_instance=SwaggerClient.from_url(f'{base_url}/api/v1/biac/roles', http_client=http_client)
    try:
        api_response = api_instance.delete_role(id)
    except Exception as e:
        print('Exception when calling RolesApi')

    
def delete_mask_expression(id, base_url,auth_header):
    os.environ['REQUESTS_CA_BUNDLE'] = '/Users/saravanan.prasadh/Library/Application Support/mkcert/rootCA.pem'
    http_client = RequestsClient()
    http_client.session.headers.update(auth_header)
    api_instance=SwaggerClient.from_url(f'{base_url}/api/v1/biac/expressions/columnMask', http_client=http_client)
    try:
        api_response = api_instance.delete_column_mask_expression(id)
    except Exception as e:
        print('Exception when calling expressionsApi')

def create_mask_expression(mask, base_url, auth_header, overwrite=False):
    """Create a mask expression on the server with an option to overwrite."""
    if overwrite or not isinstance(check_if_maskexpression_exists(mask['name'], base_url,auth_header), str):
        if overwrite:
            delete_mask_expression(check_if_maskexpression_exists(mask['name'], base_url,auth_header), base_url)
        url = f"{base_url}/create_mask_expression"
        response = requests.post(url, headers=auth_header, json=mask)
        return response.json()
    else:
        return {'message': 'Mask expression already exists and overwrite is False.'}

def create_role(role, base_url, auth_header, overwrite=False):
    """Create a role on the server with an option to overwrite."""
    if overwrite or not isinstance(check_if_role_exists(role['name'], base_url,auth_header), str):
        if overwrite:
            delete_role(check_if_role_exists(role['name'], base_url), base_url,auth_header)
        url = f"{base_url}/create_role"
        response = requests.post(url, headers=auth_header, json=role)
        return response.json()
    else:
        return {'message': 'Role already exists and overwrite is False.'}

def map_role_to_mask(mapping, base_url, auth_header, overwrite=False):
    """Map a role to a mask expression with an option to overwrite."""
    # Assuming a combined check for both role and mask expression existence
    if overwrite or not check_if_exists(mapping['RoleName'], base_url, auth_header, 'role_mapping'):
        if overwrite:
            # Assuming the API can delete a role mapping directly
            delete_entity(mapping['RoleName'], base_url, auth_header, 'role_mapping')
        # Placeholder for the HTTP POST request to map the role to the mask
        url = f"{base_url}/map_role_to_mask"
        response = requests.post(url, headers=auth_header, json=mapping)
        return response.json()
    else:
        return {'message': 'Role mapping already exists and overwrite is False.'}

# Constants (replace with actual values)
BASE_URL = "https://sep.mwpov.sa.fieldeng.starburstdata.net"
AUTH_HEADER = {
    "Accept": "application/json",
    "Content-Type": "application/json",
    "Authorization": "Basic YWRtaW46YWRtaW4=",
    "X-Trino-Role": "system=ROLE{sysadmin}"
}

# Load the JSON configuration
with open('config.json', 'r') as config_file:
    config_data = json.load(config_file)

# Create Mask Expressions
for mask in config_data['MaskExpressions']:
    create_mask_expression(mask, BASE_URL, AUTH_HEADER, overwrite=True)

# Create Roles
for role in config_data['Roles']:
    create_role(role, BASE_URL, AUTH_HEADER, overwrite=True)

# Map Roles to Mask Expressions
for mapping in config_data['RoleMappings']:
    map_role_to_mask(mapping, BASE_URL, AUTH_HEADER, overwrite=True)
