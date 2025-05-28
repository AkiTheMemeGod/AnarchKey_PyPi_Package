# AnarchKey Client

A Python client library for connecting to and retrieving API keys from the AnarchKey vault service.
## Description
AnarchKeyClient provides a simple interface to securely retrieve API keys stored in the AnarchKey vault service. This package helps developers manage API credentials for their projects without hardcoding sensitive information in their codebase.

## Installation
```bash
pip install AnarchKeyClient
```
## Usage

```python
from AnarchKeyClient import AnarchKeyClient

# Initialize the client with your username and AnarchKey API key
client = AnarchKeyClient(username="YourUsername", api_key="YourAnarchKeyAPIKey")

# Retrieve an API key for a specific project
response = client.get_api_key(project_name="YourProjectName")

# Check if request was successful
if response["success"]:
    api_key = response["key"]
    print(f"Retrieved API key: {api_key}")
else:
    print(f"Error: {response['message']}")
```

## License MIT