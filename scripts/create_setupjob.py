import sys
import json,requests

sub_id = sys.argv[1]
notebook_path = sys.argv[2]
containerName = sys.argv[3]
storageName = sys.argv[4]
clientId = sys.argv[5]
mountName = sys.argv[6]
clientCredential = sys.argv[7]
tenantId = sys.argv[8]
#workspaceurl = sys.argv[9]
workspaceName = sys.argv[9]
resourceGroupName = sys.argv[10]

print("length = {}".format(len(sys.argv)))
print("sub_id = {}".format(sub_id))
print("notebook_path = {}".format(notebook_path))
print("containerName = {}".format(containerName))
print("mountName = {}".format(mountName))
print("storageName = {}".format(storageName))
print("tenantId = {}".format(tenantId))
print("workspaceName = {}".format(workspaceName))
print("resourceGroupName = {}".format(resourceGroupName))

print("clientId = {}".format(clientId))

print("clientCredential = {}".format(clientCredential))


#get AAD token
url = "https://login.microsoftonline.com/{}/oauth2/token".format(tenantId)

payload_base='grant_type=client_credentials&client_id={0}&client_secret={1}&resource={2}'
payload = payload_base.format(clientId,clientCredential,'2ff814a6-3304-4ab8-85cb-cd0e6f879c1d')
headers = {
  'Content-Type': 'application/x-www-form-urlencoded'
}
print(url)
print(payload)
response = requests.request("POST", url, headers=headers, data=payload)
respObj = json.loads(response.text)
token = respObj.get("access_token")
#print("token -->{}".format(token))

# get Mgmt token
print(payload_base)
payload_mgmt=payload_base.format(clientId,clientCredential,'https%3A%2F%2Fmanagement.core.windows.net%2F')
response_mgmt = requests.request("POST", url, headers=headers, data=payload_mgmt)
respMgmtObj = json.loads(response_mgmt.text)
mgmt_token = respMgmtObj.get("access_token")
print("mgmt_token -->{}".format(mgmt_token))

# Get workspace URL using management token

workspaceReqURL = "https://management.azure.com/subscriptions/{0}/resourceGroups/{1}/providers/Microsoft.Databricks/workspaces/{2}?api-version=2018-04-01".format(sub_id,resourceGroupName,workspaceName)
wsurl_payload={}
wsurl_headers = {
  'Authorization': 'Bearer {}'.format(mgmt_token)
}
wsurl_response = requests.request("GET", workspaceReqURL, headers=wsurl_headers, data=wsurl_payload)
props = json.loads(wsurl_response.text).get('properties')
workspaceUrl_postfix = props['workspaceUrl']
print(workspaceUrl_postfix)
workspaceurl='https://{}'.format(workspaceUrl_postfix)
###
# get cluster Id - gets the cluster id of the first cluster
clusterListurl = "{}/api/2.0/clusters/list".format(workspaceurl,resourceGroupName,workspaceName)
payload_clist={}
headers = {
  'X-Databricks-Azure-SP-Management-Token': mgmt_token,
  'X-Databricks-Azure-Workspace-Resource-Id': '/subscriptions/{0}/resourceGroups/{1}/providers/Microsoft.Databricks/workspaces/{2}'.format(sub_id,resourceGroupName,workspaceName),
  'Authorization': 'Bearer {}'.format(token),
  'Content-Type': 'application/json'
}

response_clist = requests.request("GET", clusterListurl, headers=headers, data=payload_clist)
clusters = json.loads(response_clist.text).get("clusters")
cluster_Id = clusters[0].get("cluster_id")
print("clusterId ==> {}".format(cluster_Id))

##

# Create Databricks Job
baseparams ={
    'containerName':containerName,
    'clientId':clientId,
    'mountName':mountName,
    'storageName':storageName,
    'clientSecret':clientCredential,
    'tenantId':tenantId
}
email_notifications={

}
nbTask = {
    'notebook_path':notebook_path,
    'base_parameters':baseparams
}

jsonTask = {
    'existing_cluster_id':cluster_Id ,
    'notebook_task': nbTask,
    'email_notifications':email_notifications,
    'name':'NB_Job_Setup',
    'max_concurrent_runs':1
}

data = json.dumps(jsonTask)

createJobUrl = "{}/api/2.0/jobs/create".format(workspaceurl)
print("create job payload ---> {}".format(data))
job_response = requests.request("POST", createJobUrl, headers=headers, data=data)
print("JOb Create status ---> {}".format(job_response.status_code))
jobId = json.loads(job_response.text).get('job_id')
print('Job Created Successfully with jobId = {}'.format(jobId))

# run the job now
jobrunNwUrl = "{}/api/2.0/jobs/run-now".format(workspaceurl)
rundata = {
  'job_id' : jobId
}
runjobPayload = json.dumps(rundata)
jobrun_response = requests.request("POST", jobrunNwUrl, headers=headers, data=runjobPayload)
runId = json.loads(jobrun_response.text).get('run_id')
print('runId = {}'.format(runId))