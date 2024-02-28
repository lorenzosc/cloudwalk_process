WITH all_months as (
	SELECT 
		DATE(date_trunc('month', created_at)) as month_year, 
		sum(loan_amount) as total_loan
	FROM loans
	GROUP BY month_year
	ORDER BY month_year
	)
SELECT month_year, total_loan
FROM all_months
WHERE total_loan = (
	SELECT MAX(total_loan)
	FROM all_months
)