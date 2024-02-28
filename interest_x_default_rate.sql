SELECT status, count(*), AVG(tax) as interest, stddev(tax) as std_deviation
FROM loans
GROUP BY status
ORDER BY status;