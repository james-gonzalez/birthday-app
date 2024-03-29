# birthday-app

A Python application, using the Flask module to serve 2 http methods, one to get a users date of birth and another to set any users date of birth. The state is saved in an AWS DynamoDB table, NoSQL database. Please see below for more information.

## Requirements

- [Python 3.7+](https://www.python.org/downloads/)
- [AWS Credentials](https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-configure.html)
- [AWS DynamoDB](https://aws.amazon.com/dynamodb/)
- [Pytest](https://docs.pytest.org) (For testing)
- [Serverless](https://github.com/serverless/serverless) (For deployment)

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

## Deployment to AWS - Serverless

We use the [serverless](https://github.com/serverless/serverless) framework to give us a very simple way to provision all of the resources we require to deploy a stateful web-applcation to the cloud.

Please see `./serverless.yml` for reference.

### How to deploy

Make sure you have serverless and the required plugins installed:
```bash
npm install -g serverless
serverless plugin install -n serverless-python-requirements
serverless plugin install -n serverless-wsgi
serverless plugin install -n serverless-dynamodb-local
```

To deploy:
```bash
serverless deploy
```

To remove:
```
serverless remove
```

To view logs/debug:
```
serverless logs -f app
```

To test locally:
```
serverless wsgi serve
```

**Note:** If you want to avoid the prefix in the uri from API Gateway, you need to utilise custom-domains, read about them here: https://www.serverless.com/blog/serverless-api-gateway-domain/

## Testing

You can find [pytest](https://docs.pytest.org/en/7.2.x/) test coverage under `./tests/` to cover each of the API call conditions set out above.

Simply run `pytest` in the root of the repo.

## Diagram
![Diagram](/diagrams/birthday-app.png)
