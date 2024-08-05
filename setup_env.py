import os

env_vars = """
# Azure configuration
AZURE_SPEECH_RESOURCE_KEY = your_azure_speech_resource_key,
AZURE_SPEECH_REGION = you_azure_speech_region
"""

def create_env_file():
    env_file_path = '.env'

    with open(env_file_path, 'w') as env_file:
            env_file.write(env_vars)

    print(f"{env_file_path} created.")

if __name__ == '__main__':
    create_env_file()
