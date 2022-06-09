$server = "localhost"
$port = "8080"
$token = $(Get-Content $PSScriptRoot/../../../token)
$bad_token = $(Get-Content $PSScriptRoot/bad_token)

curl -X GET "$server`:$port/log/" -H "Authorization: Bearer $token"
# curl -X GET "$server`:$port/log/" -H "Authorization: Bearer $bad_token"