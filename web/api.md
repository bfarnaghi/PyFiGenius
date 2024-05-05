# Expense and Income API Documentation

## Submit Expense

### Endpoint

#### POST /submit/expense/
#### POST /submit/income/


### Description
This endpoint allows users to submit expenses/incomes.

### Request Parameters
| Parameter | Type   | Description                                  |
|-----------|--------|----------------------------------------------|
| token     | String | Authentication token for the user            |
| amount    | Float  | Amount of the expense/income                 |
| text      | String | Description of the expense/income            |
| date      | String | (Optional) Date of the expense in ISO format |

### Request Example
```json
{
    "token": "user_token_here",
    "amount": 25.50,
    "text": "Dinner with friends",
    "date": "2024-05-05T18:30:00"
}
```

#### Response
##### 200 OK: Expense submitted successfully
```json
{
    "status": "ok",
    "expense_id": 123
}
```
##### 400 Bad Request: Missing required fields or invalid token
```json
{
    "status": "error",
    "message": "Invalid or expired token."
}
```
##### 405 Method Not Allowed: Only POST requests are allowed
```json
{
    "status": "error",
    "message": "Only POST requests are allowed."
}
```