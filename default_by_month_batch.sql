WITH all_entries AS (
	SELECT 
		DATE(date_trunc('month', loans.created_at)) as month_year,
		clients.batch,
		SUM(case when loans.status = 'default' then 1 else 0 end)/CAST(COUNT(loans.status) AS FLOAT) AS default_rate,
		COUNT(loans.status) as loans
	FROM loans
	LEFT JOIN clients ON loans.user_id = clients.user_id
	GROUP BY clients.batch, month_year
	ORDER BY clients.batch, month_year
)
SELECT month_year, batch, default_rate, loans
FROM all_entries
WHERE DATE '2024-01-25' - month_year > 90; -- WHERE current_date - month_year > 80 for a real case
