from ..utils.connect import connect
from ..utils.send_email import send_email
import datetime
from ..utils.email_config import EMAIL

"""
Generate summary with week information
# of new clients
How many loans were paid
How many loans became defaulted
How much money was lent
What's the profit expected from the money lent, provided it gets completely payed
What's the profit expected from the money lent, based on the average operation performance
Based on the paid and the defaulted loans, how is this week's performance in terms of profit and ROI
"""
if __name__ == "__main__": 
    conn = connect()
    cur = conn.cursor()

    # New clients
    query = """
            SELECT COUNT(user_id)
            FROM clients
            WHERE CURRENT_DATE - DATE(created_at) <= 7;
            """
    cur.execute(query)
    new_clients = cur.fetchall()[0][0]

    # How many loans were paid, how much was paid, and what's the total invested for those loans
    query = """
            SELECT COUNT(amount_paid), SUM(amount_paid), SUM(loan_amount), SUM(amount_paid)- SUM(loan_amount)
            FROM loans
            WHERE CURRENT_DATE - DATE(paid_at) <= 7;
            """
    cur.execute(query)
    result = cur.fetchall()[0]
    loans_paid = result[0]
    amount_received = result[1]
    total_loans_paid = result[2]
    profit_loans_paid = result[3]


    # How many loans became defaulted, how much was lost, how much is due, and what's the total invested
    query = """
        SELECT 
            COUNT(due_amount), 
            SUM(amount_paid)- SUM(loan_amount),
            SUM(due_amount) - SUM(amount_paid),
            SUM(loan_amount)
        FROM loans
        WHERE 
            CURRENT_DATE - DATE(due_at) <= 7
            AND CURRENT_DATE - DATE(due_at) >= 0
            AND status = %s;
        """
    cur.execute(query, ["default"])
    result = cur.fetchall()[0]
    defaulted_loans = result[0]
    money_loss = result[1]
    still_due = result[2]
    total_loans_defaulted = result[3]

    # How many loans where given and how much total money was lent
    query = """
            SELECT COUNT(loan_amount), SUM(loan_amount), SUM(due_amount)
            FROM loans
            WHERE CURRENT_DATE - DATE(created_at) <= 7;
            """
    cur.execute(query)
    result = cur.fetchall()[0]
    loans_made = result[0]
    money_lent = result[1]
    total_due_to_receive = result[2]

    # Average performance
    query = """
            SELECT
                DATE(date_trunc('month', created_at)) AS month_year, 
                SUM(amount_paid) - SUM(loan_amount) AS profit,
                (SUM(amount_paid) - SUM(loan_amount))/SUM(loan_amount) AS roi
            FROM loans
            WHERE CURRENT_DATE - DATE(created_at) > 90
            GROUP BY month_year
            ORDER BY month_year DESC;
            """
    params = ['month']
    months = 12
    cur.execute(query, params)
    result = cur.fetchmany(months)
    roi = 0
    for i in range(months):
        roi += result[i][2]
    roi /= months
    realistic_expected_profit = roi*money_lent

    # ROI and profit from this week
    week_profit = amount_received + money_loss
    week_roi = week_profit/(total_loans_defaulted + total_loans_paid)
    
    # Email
    body = f"""Here is the report for the days from {datetime.date.today() - datetime.timedelta(days=7)} to \
{datetime.date.today()} on the loan operation.

We gathered a total of {new_clients} new clients!

From our previous loans, {loans_paid} were completely payed off, and we received a total of R${amount_received:.2f} \
for a profit of R${profit_loans_paid:.2f}.

Regarding defaults, we had {defaulted_loans} loans that expired this week without being completely payed. In \
that, we lost R${money_loss:.2f}, and the total still due from those clients is R${still_due:.2f}.

As for new loans, we made {loans_made} new loans, totalizing R${money_lent:.2f}. The amount of debt we generated is \
R${total_due_to_receive:.2f}, but according to our operation in the previous {months} months, we can expect to receive \
R${realistic_expected_profit:.2f} due to the return on investiment of our operation of {100*roi:.2f}%.

Averaging this week, our profit is of R${week_profit:.2f} and the return on the investiments is {week_roi*100:.2f}.

This is an automatic email. Please do not respond.
"""
    subject = f"Week from {datetime.date.today() - datetime.timedelta(days=7)} to {datetime.date.today()}"
    send_email(subject, body, EMAIL)
