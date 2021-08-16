[CmdletBinding()]
param (
    $testParam,
    $appId,
    $tenantId
)

Write-Host "testParam : $($testParam)"
Write-Host "appId : $($appId)"
Write-Host "tenantId : $($tenantId)"
Write-Host "DatabricksClusterId : $env:DatabricksClusterId"
echo "##vso[task.setvariable variable=DatabricksClusterId;]$($DatabricksClusterId)"
