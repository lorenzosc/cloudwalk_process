SELECT 
	batch,
	SUM(case when status = 'approved' then 1 else 0 end)/CAST(COUNT(status) AS FLOAT) as ratio,
	SUM(case when status = 'approved' then 1 else 0 end) as approved_clients
FROM clients
GROUP BY batch
ORDER BY batch;