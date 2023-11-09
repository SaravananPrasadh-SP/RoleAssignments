import requests

# Define variables
config = {
    "role_name": "autorole1",
    "column_mask_name": "testcolumnmask1",
    "catalog": "tpch",
    "schema": "tiny",
    "table": "customer",
    "columns": ["nationkey"],
    "base_url": "https://sep.saipov.az.starburstdata.net/api/v1/biac",
    "auth_header": {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "X-Trino-Role": "system=ROLE{sysadmin}",
        "Authorization": "Basic YWRtaW46U3RhcmJ1cnN0UjBja3Mh"
    }
}

# Create the role
role_url = f"{config['base_url']}/roles"
role_payload = {
    "name": config["role_name"],
    "description": "This is a role created by API"
}
role_response = requests.post(role_url, json=role_payload, headers=config["auth_header"], verify=False)
role_id = role_response.json()["id"]

# Create the column mask
column_mask_url = f"{config['base_url']}/expressions/columnMask"
column_mask_payload = {
    "name": config["column_mask_name"],
    "description": "This is will replace vowels with stars",
    "expression": "regexp_replace(\"@column\",'[aeiou]','*')"
}
column_mask_response = requests.post(column_mask_url, json=column_mask_payload, headers=config["auth_header"], verify=False)
column_mask_id = column_mask_response.json()["id"]

# Create a column mask for the role
role_column_mask_url = f"{config['base_url']}/roles/{role_id}/columnMasks"
role_column_mask_payload = {
    "expressionId": column_mask_id,
    "entity": {
        "category": "TABLES",
        "allEntities": False,
        "catalog": config["catalog"],
        "schema": config["schema"],
        "table": config["table"],
        "columns": config["columns"]
    }
}
requests.post(role_column_mask_url, json=role_column_mask_payload, headers=config["auth_header"], verify=False)

# Attach the role to the user
user_role_url = f"{config['base_url']}/subjects/users/admin/assignments"
user_role_payload = {
    "roleId": role_id,
    "roleAdmin": False
}
requests.post(user_role_url, json=user_role_payload, headers=config["auth_header"], verify=False)
