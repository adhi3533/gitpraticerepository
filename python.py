import os
from azure.identity import DefaultAzureCredential
from azure.mgmt.storage import StorageManagementClient
from azure.storage.blob import BlobServiceClient

# --------------------------
# USER INPUT SECTION
# --------------------------
subscription_id = "393f65b7-2e65-4160-96d2-0d364a1c1674"
resource_group_name = "mystorage"
location = "centralindia"
storage_account_name = "mypythonstorage123456"   # must be globally unique
container_name = "mycontainer"
file_to_upload = "sample.txt"  # file must exist locally
# --------------------------

# Authenticate
credential = DefaultAzureCredential()

# 1. Create Storage Management Client
storage_client = StorageManagementClient(credential, subscription_id)

# 2. Create Resource Group
print("Creating resource group...")
os.system(f"az group create --name {resource_group_name} --location {location}")

# 3. Create Storage Account
print("Creating storage account...")
async_create = storage_client.storage_accounts.begin_create(
    resource_group_name,
    storage_account_name,
    {
        "location": location,
        "sku": {"name": "Standard_LRS"},
        "kind": "StorageV2"
    }
)
storage_account = async_create.result()
print("Storage account created successfully.")

# 4. Get Storage Account Keys
keys = storage_client.storage_accounts.list_keys(resource_group_name, storage_account_name)
account_key = keys.keys[0].value

# 5. Connect to Blob Service
blob_service_client = BlobServiceClient(
    f"https://{storage_account_name}.blob.core.windows.net",
    credential=account_key
)

# 6. Create Container
container_client = blob_service_client.get_container_client(container_name)

try:
    container_client.create_container()
    print(f"Container '{container_name}' created.")
except:
    print(f"Container '{container_name}' already exists.")

# 7. Upload File
print("Uploading file...")
blob_client = container_client.get_blob_client(file_to_upload)

with open(file_to_upload, "rb") as data:
    blob_client.upload_blob(data, overwrite=True)

print(f"File '{file_to_upload}' uploaded successfully!")
print(f"Blob URL: https://{storage_account_name}.blob.core.windows.net/{container_name}/{file_to_upload}")
