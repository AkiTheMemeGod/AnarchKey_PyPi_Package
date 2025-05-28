from src.AnarchKeyClient import AnarchKeyClient

anarch = AnarchKeyClient(username="Akash",api_key="")


response = anarch.get_api_key(project_name="SRMCRUDAPI")
print(response)