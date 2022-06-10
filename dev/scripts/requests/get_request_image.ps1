$server = "localhost"
$port = "8080"
$file=$args[0]
$output = "received_file.jpg"
$token = $(Get-Content $PSScriptRoot/../../../token)
$bad_token = $(Get-Content $PSScriptRoot/bad_token)

curl -X GET "$server`:$port/$file" -H "Authorization: Bearer $token" --output "$output"
# curl -X GET "$server`:$port/$file" -H "Authorization: Bearer $bad_token" --output "$output"

