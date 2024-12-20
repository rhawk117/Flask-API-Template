$ErrorActionPreference = "Stop"

$BaseUrl = "http://127.0.0.1:5000"

function Test-Endpoint {
    param(
        [string]$TestName,
        [scriptblock]$Action
    )
    Write-Host "[..] running test -> $TestName"
    try {
        $response = & $Action
        if ($null -eq $response) {
            Write-Host "[PASS] - $TestName"
            return $response
        }
        else {
            Write-Host "[PASS] - $TestName"
            return $response
        }
    }
    catch {
        Write-Host "[FAIL] - $TestName - $($_.Exception.Message)"
        return $null
    }
}


$registerResponse = Test-Endpoint -TestName "Register User (jeff/jeff)" -Action {
    Invoke-RestMethod -Uri "$BaseUrl/auth/register" `
        -Method POST `
        -Headers @{ "Content-Type" = "application/json" } `
        -Body '{"username":"jeff","password":"jeff"}'
}

if ($registerResponse -and $registerResponse.message -ne "User registered successfully") {
    Write-Host "FAIL: Register User - Unexpected response message"
}
else {
    Write-Host "Registration response check: PASS"
}

$loginResponse = Test-Endpoint -TestName "Login with (jeff/jeff)" -Action {
    Invoke-RestMethod -Uri "$BaseUrl/auth/login" `
        -Method POST `
        -Headers @{ "Content-Type" = "application/json" } `
        -Body '{"username":"jeff", "password":"jeff"}'
}

if ($loginResponse -and $null -eq $loginResponse.token) {
    Write-Host "FAIL: Login - Token not returned"
    exit 1
}
else {
    Write-Host "Login token check: PASS"
}

$token = $loginResponse.token
$headers = @{ "Authorization" = "Bearer $token"; "Content-Type" = "application/json" }

$createTodoResponse = Test-Endpoint -TestName "Create a new Todo" -Action {
    Invoke-RestMethod -Uri "$BaseUrl/todos/" `
        -Method POST `
        -Headers $headers `
        -Body '{"name":"get jacked","description":"some one has to"}'
}

if ($createTodoResponse -and $createTodoResponse.message -ne "Todo created") {
    Write-Host "FAIL: Create Todo - Unexpected response message"
}
else {
    Write-Host "Create Todo response check: PASS"
}

$todoId = $createTodoResponse.id

$listTodosResponse = Test-Endpoint -TestName "List Todos" -Action {
    Invoke-RestMethod -Uri "$BaseUrl/todos/" `
        -Method GET `
        -Headers @{ "Authorization" = "Bearer $token" }
}

if ($listTodosResponse -and ($listTodosResponse | Measure-Object).Count -eq 1) {
    Write-Host "List Todos Check: PASS"
}
else {
    Write-Host "FAIL: List Todos - Expected 1 todo, got something else"
}

$updateTodoResponse = Test-Endpoint -TestName "Update Todo (mark completed)" -Action {
    Invoke-RestMethod -Uri "$BaseUrl/todos/$todoId" `
        -Method PATCH `
        -Headers $headers `
        -Body '{"completed":true}'
}

if ($updateTodoResponse -and $updateTodoResponse.message -ne "Todo updated") {
    Write-Host "FAIL: Update Todo - Unexpected response message"
}
else {
    Write-Host "Update Todo response check: PASS"
}

$deleteTodoResponse = Test-Endpoint -TestName "Delete Todo" -Action {
    Invoke-RestMethod -Uri "$BaseUrl/todos/$todoId" `
        -Method DELETE `
        -Headers @{ "Authorization" = "Bearer $token" }
}

if ($deleteTodoResponse -and $deleteTodoResponse.message -ne "Todo deleted") {
    Write-Host "FAIL: Delete Todo - Unexpected response message"
}
else {
    Write-Host "Delete Todo response check: PASS"
}

Write-Host "All tests completed."