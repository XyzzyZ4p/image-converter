$server = "localhost"
$port = "8080"
$header = "Content-Type: multipart/form-data"
$token = $(Get-Content $PSScriptRoot/../../../token)
$file =  "$PSScriptRoot/test-image.png"
$params = 'data={"quality"="1","x"="250","y"="200"}'
$type = 'type=text/plain'
$bad_token = $(Get-Content $PSScriptRoot/bad_token)

curl -X POST "$server`:$port" -H "$header" -H "Authorization: Bearer $token" -F "file=@$file" -F "$params;$type"
# curl -X POST "$server`:$port" -H "$header" -H "Authorization: Bearer $bad_token" -F "file=@$file" -F "$params;$type"
