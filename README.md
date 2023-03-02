# birthday-app

Saves/updates the given user’s name and date of birth in a sqlite database.

This is just an sample application created as a demo.

## Requirements

- Python 3.6+
- SQLite3

## API calls

PUT `/hello/<username> --data{ “dateOfBirth”: “YYYY-MM-DD” }`

Description: If the conditions are correct, it will save `<username>` as the user's name
and then set `“dateOfBirth”` as the date of birth

Response: `204 No Content`

**Note:** `<username>` must contain only letters.

`YYYY-MM-DD` must be a date before the today date.

Response: `204 No Content`

GET `/hello/<username> `

Description: Returns hello birthday message for the given user

Response: `200 OK`

## Response Examples:
A. If username’s birthday is in N days:
{ “message”: “Hello, <username>! Your birthday is in N day(s)”
}
B. If username’s birthday is today:
{ “message”: “Hello, <username>! Happy birthday!” }

## Examples:

To store the user `tom` with the birthday `1985-01-21`
```
curl -XPUT http://localhost:5000/hello/tom --data '{ "dateOfBirth": "1985-01-21" }' -H "Content-Type:application/json" -i
```

To get the user `tom` birthday
```
curl -XPUT http://localhost:5000/hello/tom
```

## Docker

Included is a `Dockerfile` and a `docker-compose` file which allow you to easily test
the application, with the `docker-compose` file you can see that you can run multiple
replicas calling the same volume/dataset.

Simply run `docker-compose up -d` to get stated.
