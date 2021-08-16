import os
import uuid
import sys
from azure.identity import ClientSecretCredential
from azure.storage.filedatalake import DataLakeServiceClient
from azure.core._match_conditions import MatchConditions
from azure.storage.filedatalake._models import ContentSettings

clientId = sys.argv[1]
clientCredential = sys.argv[2]
tenantId = sys.argv[3]
storageName = sys.argv[4]
in_container = sys.argv[5]
out_container = sys.argv[6]
fileName = sys.argv[7]
filePath = sys.argv[8]

try:
    global service_client
    credential = ClientSecretCredential(tenantId, clientId, clientCredential)
    service_client = DataLakeServiceClient(account_url="{}://{}.dfs.core.windows.net".format(
        "https", storageName), credential=credential)
    file_system_client = service_client.create_file_system(file_system=in_container)
    print("After creating container -->{}".format(in_container))
    # output container 
    service_client.create_file_system(file_system=out_container)
    print("After creating container -->{}".format(out_container))
    directory_client = file_system_client.get_directory_client("/")
    file_client  = directory_client.create_file(fileName)
    local_file = open(filePath,'r')
    file_contents = local_file.read()
    file_client.append_data(data=file_contents, offset=0, length=len(file_contents))
    file_client.flush_data(len(file_contents))
    print("After uploading sample file in container -")
except Exception as e:
    print(e)
