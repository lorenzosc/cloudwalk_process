from ..utils.connect import connect
import datetime
from ..utils.send_email import send_email

if __name__ == "__main__":
    conn = connect()
    cur = conn.cursor()

    # Update payed loans
    query = """
        UPDATE loans
        SET status = %s
        WHERE due_amount = amount_paid;
        """
    cur.execute(query, ["paid"])

    # Update defaulted loans
    query = """
        UPDATE loans
        SET status = %s
        WHERE 
            due_amount > amount_paid 
            AND CURRENT_DATE > due_at;
        """
    cur.execute(query, ["default"])
    
    # Verify users, including locked and password-expired
    query = """
            SELECT
                usename,
                usesuper,
                usebypassrls,
                DATE(valuntil)
            FROM pg_user
            """
    cur.execute(query)
    results = cur.fetchall()
    
    print("All users\n")
    for result in results:
        print(f"{result[0]}\n")

    for result in results:

        if result[3]:
            password_valid = (result[3] - datetime.date.today()).days
            if password_valid < 7:
                subject = f"Your password for psql expires in {password_valid} days"
                body = f"Your password expires in {password_valid} days in the psql DB. Change it before it expires!"
                send_email(subject, body, result[0])
        
        if result[1] == True:
            print(f"User {result[0]} is a superuser. This is a reminder in case they shouldn't be")

        if result[2] == True:
            print(f"User {result[0]} can bypass row-level security policies. This is a reminder in case they shouldn't be able to")

    conn.commit()
    cur.close()
    conn.close()