[CmdletBinding()]
param (
    $sp_name,
    $sp_password,
    $resourcegrp,
    $storagename,
    $adbws_name
)
$spName = $sp_name
$spPassword = $sp_password
$resourceGrp = $resourcegrp
$strgName = $storagename

Install-Module -Name AzureRm -AllowClobber -Scope CurrentUser

Import-Module Az.Resources
Import-Module Az.Accounts
Write-Host "After Importing Module spname ...$($spName)"
Write-Host "After Importing Module resourceGrp ...$($resourceGrp)"
Write-Host "After Importing Module strgName ...$($strgName)"

$credentials = New-Object Microsoft.Azure.Commands.ActiveDirectory.PSADPasswordCredential `
               -Property @{StartDate=Get-Date; EndDate=Get-Date -Year 2022; Password=$spPassword};

Write-Host "After credentails..."
$spConfig = @{
              DisplayName = $spName
              PasswordCredential = $credentials
             }
			 
$servicePrincipal = New-AzAdServicePrincipal @spConfig
Write-Host "After Service Principal..."
$subscriptionId = (Get-AzContext).Subscription.Id
$scope = "/subscriptions/$subscriptionId/resourceGroups/$resourceGrp/providers/Microsoft.Storage/storageAccounts/$strgName"
$adb_scope = "/subscriptions/$subscriptionId/resourceGroups/$resourceGrp/providers/Microsoft.Databricks/workspaces/$adbws_name"
Write-Host "Creating SP Role for : $($scope)"
$spRoleAssignment_strg = @{
                      ObjectId = $servicePrincipal.id;
                      RoleDefinitionName = 'Storage Blob Data Contributor';
                      Scope = $scope
                     }
New-AzRoleAssignment @spRoleAssignment_strg

Write-Host "Creating SP Role on sub: $($scope)"
$spRoleAssignment_sub = @{
    ObjectId = $servicePrincipal.id;
    RoleDefinitionName = 'Contributor';
    Scope = "/subscriptions/$subscriptionId"
   }
New-AzRoleAssignment @spRoleAssignment_sub

Write-Host "Creating SP Role on ADB WS : $($adb_scope)"
$spRoleAssignment_adb = @{
    ObjectId = $servicePrincipal.id;
    RoleDefinitionName = 'Contributor';
    Scope = $adb_scope
   }
New-AzRoleAssignment @spRoleAssignment_adb

$spNew = Get-AzADServicePrincipal -DisplayName $spName
$appId = $spNew.ApplicationId
$tenant = Get-AzTenant
$tenantId = $tenant.Id 

Write-Host "Successfully Created Service Principal : $($spName)"
Write-Host "APP Id : $($appId)"
echo "##vso[task.setvariable variable=testParam;]$($spName)"
echo "##vso[task.setvariable variable=appId;]$($appId)"
echo "##vso[task.setvariable variable=tenantId;]$($tenantId)"