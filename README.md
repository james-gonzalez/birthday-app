# birthday-app

Saves/updates the given user’s name and date of birth in a sqlite database.

This is just an sample application created as a demo.

## API calls
PUT `/hello/<username> --data{ “dateOfBirth”: “YYYY-MM-DD” }`
Response: `204 No Content`

**Note:** `<username>` must contain only letters.
`YYYY-MM-DD` must be a date before the today date.

Description: Returns hello birthday message for the given user
Request: GET `/hello/<username>`
Response: `200 OK`

## Response Examples:
A. If username’s birthday is in N days:
{ “message”: “Hello, <username>! Your birthday is in N day(s)”
}
B. If username’s birthday is today:
{ “message”: “Hello, <username>! Happy birthday!” }
