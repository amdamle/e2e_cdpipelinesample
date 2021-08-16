[CmdletBinding()]
param (
    $sp_name,
    $sp_password,
    $sp_appid,
    $tenant,
    $containername,
    $outcontainername,
    $storagename,
    $filename,
    $filepath
)
Write-Host "**** sp_appid ****$($sp_appid)"
# login using service principal created
az login --service-principal --username $sp_appid --password $sp_password --tenant $tenant
# Create container in storage account
Write-Host "**** Creating src container ****$($containername)"
# az storage fs create --account-name autowsstrprod21 --auth-mode login --name input
az storage fs create --account-name $storagename --auth-mode login --name $containername
Write-Host "**** Container $($containername) Created ****"
Write-Host "**** Creating results container ****$($outcontainername)"
az storage fs create -n $outcontainername --account-name $storagename --auth-mode login
Write-Host "**** Container $($outcontainername) Created ****"
# az storage blob list --container-name $containername --account-name $storagename --auth-mode login
# upload sample text file to newly created container
az storage blob upload --name $filename --file $filepath --container-name $containername --account-name $storagename --auth-mode login

Write-Host "**** Successfully uploaded sample file into container ****"