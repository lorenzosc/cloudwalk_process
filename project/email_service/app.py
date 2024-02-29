from flask import Flask, jsonify
import schedule
import time
from ..utils.send_email import send_email
from ..utils.connect import connect

app = Flask(__name__)

def job():
    conn = connect()
    cur = conn.cursor()

    for days in [30, 15, 7, 1, 0]:
        query = f"""
                SELECT user_id, DATE(due_at), due_amount - amount_paid
                FROM loans
                WHERE 
                    status = %s
                    AND DATE(due_at) - CURRENT_DATE = {days}
                """
        month_clients = cur.execute(query, ["ongoing"])

        for name, _, amount in month_clients:
            subject = f"Your debt is due in {days} days"
            body = f"""\
Good afternoon, {name}! 

This is a reminder that the loan you took with us is due in {days} days. \
Don't forget to pay until the due date.

The amount you are still due is R${amount:.2f}.
"""
            to_email = name

            if days == 1:
                subject.replace("days", "day")
                body.replace("days", "day")
            if days == 0:
                subject.replace("in 0 days", "today")
                body.replace("in 0 days", "today")
                body.replace("Don't forget to pay until the due date.", "Don't forget to pay it.")

            send_email(subject, body, to_email)
    
    cur.close()
    conn.close()

schedule.every().day.at("12:00").do(job)

@app.route('/')
def home():
    return "Email service is running"

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0")

while True:
    schedule.run_pending()
    time.sleep(1)
