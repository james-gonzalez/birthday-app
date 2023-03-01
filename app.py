import sqlite3
from flask import Flask, request, jsonify
import datetime
import os

app = Flask(__name__)

conn = sqlite3.connect("users.db", check_same_thread=False)
c = conn.cursor()

# create table if it doesn't exist
c.execute(
    """CREATE TABLE IF NOT EXISTS hello (username TEXT PRIMARY KEY, dateOfBirth TEXT)"""
)
conn.commit()


def put_user(username, dateOfBirth):
    # Insert or replace the user's data into the table
    c.execute("""SELECT * FROM hello WHERE username = ?""", (username,))
    row = c.fetchone()
    if row:
        # update existing row
        c.execute(
            """UPDATE hello SET dateOfBirth = ? WHERE username = ?""",
            (dateOfBirth, username),
        )
    else:
        # insert new row
        c.execute("""INSERT INTO hello VALUES (?, ?)""", (username, dateOfBirth))
    conn.commit()

    return jsonify(messaage="User data saved successfully.")


def get_user(username):
    # query table for username and dateOfBirth
    c.execute("""SELECT * FROM hello WHERE username = ?""", (username,))
    row = c.fetchone()
    if row:
        # get dateOfBirth from row
        dob = row[1]
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
            return jsonify(messaage=f"Hello {username}! Happy birthday!")
        elif delta_days == 0:
            # return f'Hello {username}! Your birthday is tomorrow!'
            return jsonify(messaage=f"Hello {username}! Your birthday is tomorrow!")
        else:
            # return f'Hello {username}! Your birthday is in {delta_days} days!'
            return jsonify(
                messaage=f"Hello {username}! Your birthday is in {delta_days} days!"
            )
    else:
        # return f'Hello {username}! I dont know your birthday.'
        return jsonify(messaage=f"Hello {username}! I dont know your birthday.")


@app.route("/hello/<username>", methods=["PUT"])
def put_hello(username):
    # Check if username contains only letters
    if not username.isalpha():
        return "Invalid username. It must contain only letters."

    data = request.get_json()

    dob = data["dateOfBirth"]

    dateObject = datetime.datetime.strptime(dob, "%Y-%m-%d")

    today = datetime.date.today()

    if dateObject.date() > today:
        return "Error: The date must be in the past."
    else:
        put_user(username, dob)

        return ("", 204)


@app.route("/hello/<username>", methods=["GET"])
def get_hello(username):
    greeting = get_user(username)

    return greeting


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=os.environ.get("PORT"), use_debugger=False)
