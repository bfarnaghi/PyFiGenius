## API Models Description

### Submit Expense
- **Endpoint**: `/api/submit/expense/`
- **Method**: POST
- **Description**: Submits a new expense.
- **Parameters**:
  - `token`: Token associated with the user.
  - `amount`: Amount of the expense.
  - `text`: Description of the expense.
  - `date` (optional): Date of the expense (defaults to current date if not provided).

### Submit Income
- **Endpoint**: `/api/submit/income/`
- **Method**: POST
- **Description**: Submits a new income.
- **Parameters**:
  - `token`: Token associated with the user.
  - `amount`: Amount of the income.
  - `text`: Description of the income.
  - `date` (optional): Date of the income (defaults to current date if not provided).

### List Expenses
- **Endpoint**: `/api/list/expenses/`
- **Method**: GET
- **Description**: Retrieves a list of all expenses associated with the user.

### List Incomes
- **Endpoint**: `/api/list/incomes/`
- **Method**: GET
- **Description**: Retrieves a list of all incomes associated with the user.

### Update Expense
- **Endpoint**: `/api/update/expense/<expense_id>/`
- **Method**: POST
- **Description**: Updates an existing expense.
- **Parameters**:
  - `token`: Token associated with the user.
  - `amount`: Updated amount of the expense.
  - `text`: Updated description of the expense.
  - `date`: Updated date of the expense.

### Update Income
- **Endpoint**: `/api/update/income/<income_id>/`
- **Method**: POST
- **Description**: Updates an existing income.
- **Parameters**:
  - `token`: Token associated with the user.
  - `amount`: Updated amount of the income.
  - `text`: Updated description of the income.
  - `date`: Updated date of the income.

### Delete Expense
- **Endpoint**: `/api/delete/expense/<expense_id>/`
- **Method**: POST
- **Description**: Deletes an existing expense.

### Delete Income
- **Endpoint**: `/api/delete/income/<income_id>/`
- **Method**: POST
- **Description**: Deletes an existing income.

### Submit Income Category
- **Endpoint**: `/api/submit/income_category/`
- **Method**: POST
- **Description**: Submits a new income category.

### Submit Expense Category
- **Endpoint**: `/api/submit/expense_category/`
- **Method**: POST
- **Description**: Submits a new expense category.

### List Income Categories
- **Endpoint**: `/api/list/income_categories/`
- **Method**: GET
- **Description**: Retrieves a list of all income categories.

### List Expense Categories
- **Endpoint**: `/api/list/expense_categories/`
- **Method**: GET
- **Description**: Retrieves a list of all expense categories.

### Update Token
- **Endpoint**: `/api/update/token/<token_id>/`
- **Method**: POST
- **Description**: Updates an existing user token.

### Update Bank Account
- **Endpoint**: `/api/update/bank_account/<account_id>/`
- **Method**: POST
- **Description**: Updates an existing bank account.

### Update Monthly Expense
- **Endpoint**: `/api/update/monthly_expense/<expense_id>/`
- **Method**: POST
- **Description**: Updates an existing monthly expense.

### Delete Income Category
- **Endpoint**: `/api/delete/income_category/<category_id>/`
- **Method**: POST
- **Description**: Deletes an existing income category.

### Delete Expense Category
- **Endpoint**: `/api/delete/expense_category/<category_id>/`
- **Method**: POST
- **Description**: Deletes an existing expense category.

### Delete Token
- **Endpoint**: `/api/delete/token/<token_id>/`
- **Method**: POST
- **Description**: Deletes an existing user token.

### Delete Bank Account
- **Endpoint**: `/api/delete/bank_account/<account_id>/`
- **Method**: POST
- **Description**: Deletes an existing bank account.

### Delete Monthly Expense
- **Endpoint**: `/api/delete/monthly_expense/<expense_id>/`
- **Method**: POST
- **Description**: Deletes an existing monthly expense.
