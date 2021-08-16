# Databricks notebook source
dbutils.widgets.text("clientId", "","")
dbutils.widgets.text("clientSecret", "","")
dbutils.widgets.text("tenantId", "","")
dbutils.widgets.text("containerName", "","")
dbutils.widgets.text("storageName", "","")
dbutils.widgets.text("mountName", "","")


# COMMAND ----------

client = dbutils.widgets.get("clientId")
secret = dbutils.widgets.get("clientSecret")
tenant = dbutils.widgets.get("tenantId")
container = dbutils.widgets.get("containerName")
storage = dbutils.widgets.get("storageName")
mount = dbutils.widgets.get("mountName")
endPoint = "https://login.microsoftonline.com/{}/oauth2/token".format(tenant)
storageURL = "abfss://{0}@{1}.dfs.core.windows.net".format(container,storage)

print(storageURL)

# COMMAND ----------

configs = {"fs.azure.account.auth.type": "OAuth",
       "fs.azure.account.oauth.provider.type": "org.apache.hadoop.fs.azurebfs.oauth2.ClientCredsTokenProvider",
       "fs.azure.account.oauth2.client.id": client,
       "fs.azure.account.oauth2.client.secret": secret,
       "fs.azure.account.oauth2.client.endpoint":endPoint ,
       "fs.azure.createRemoteFileSystemDuringInitialization": "true"}

dbutils.fs.mount(
source = storageURL,
mount_point = mount,
extra_configs = configs)

# COMMAND ----------

#dbutils.fs.unmount("/mnt/adbauto")