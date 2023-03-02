import boto3
from boto3.dynamodb.conditions import Key
from flask import Flask, request, jsonify
import datetime
import os

app = Flask(__name__)

# create a dynamodb resource
dynamodb = boto3.resource("dynamodb")

# create a table object
table = dynamodb.Table("users")


def put_user(username, dob):
    # insert or replace the user's data into the table
    table.put_item(Item={"username": username, "dateofbirth": dob})


def get_user(username):
    # query table for username and dateOfBirth
    # use the get_item method with a consistent read option
    response = table.query(KeyConditionExpression=Key("username").eq(username))
    if response["Items"]:
        dob = response["Items"][0]["dateofbirth"]
        # convert dateOfBirth to datetime object
        dob_dt = datetime.datetime.strptime(dob, "%Y-%m-%d")
        # get today's date as datetime object
        today_dt = datetime.datetime.today()
        # calculate days until next birthday
        next_birthday_dt = dob_dt.replace(year=today_dt.year)
        if next_birthday_dt < today_dt:
            next_birthday_dt = next_birthday_dt.replace(year=today_dt.year + 1)
        delta_days = (next_birthday_dt - today_dt).days

        # return greeting message based on days until next birthday
        if delta_days == 364:
            # return f'Hello {username}! Happy birthday!'
            return jsonify(message=f"Hello {username}! Happy birthday!")
        elif delta_days == 0:
            # return f'Hello {username}! Your birthday is tomorrow!'
            return jsonify(message=f"Hello {username}! Your birthday is tomorrow!")
        else:
            # return f'Hello {username}! Your birthday is in {delta_days} days!'
            return jsonify(
                message=f"Hello {username}! Your birthday is in {delta_days} days!"
            )
    else:
        return jsonify(message=f"Hello {username}! I dont know your birthday.")


@app.route("/hello/<username>", methods=["PUT"])
def put_hello(username):
    # Check if username contains only letters
    if not username.isalpha():
        return jsonify(message="Invalid username. It must contain only letters.")

    data = request.get_json()

    dob = data["dateOfBirth"]

    dateObject = datetime.datetime.strptime(dob, "%Y-%m-%d")

    today = datetime.date.today()

    if dateObject.date() > today:
        return jsonify(message="Error: The date must be in the past.")
    else:
        put_user(username, dob)

        return ("", 204)


@app.route("/hello/<username>", methods=["GET"])
def get_hello(username):
    greeting = get_user(username)

    return greeting


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=os.environ.get("PORT"), use_debugger=False)
