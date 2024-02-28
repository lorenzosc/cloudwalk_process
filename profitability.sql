SELECT
	DATE(date_trunc('month', created_at)) AS month_year, 
	SUM(amount_paid) - SUM(loan_amount) AS profit,
	(SUM(amount_paid) - SUM(loan_amount))/SUM(loan_amount) AS roi
FROM loans
WHERE DATE '2024-01-25' - DATE(created_at) > 90 OR status = 'paid'
GROUP BY month_year
ORDER BY month_year;