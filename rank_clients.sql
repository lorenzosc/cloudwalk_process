SELECT 
	clients.user_id,
	SUM(loans.loan_amount) as total_loan, 
	SUM(loans.due_amount) as total_due,
	SUM(loans.amount_paid) as total_paid,
	SUM(loans.amount_paid) - SUM(loans.loan_amount) as profit,
	(SUM(loans.amount_paid) - SUM(loans.loan_amount))/SUM(loans.loan_amount) as roi,
	SUM(loans.amount_paid) - SUM(loans.due_amount) as debt
FROM loans
INNER JOIN clients on clients.user_id = loans.user_id
WHERE DATE '2024-01-25' - DATE(loans.created_at) > 90 OR loans.status = 'paid'
GROUP BY clients.user_id
ORDER BY debt ASC, profit ASC	
LIMIT 10;