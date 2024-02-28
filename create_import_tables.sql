DROP TABLE loans;
DROP TABLE clients;

CREATE TABLE clients (
	user_id int8 primary key,
	created_at TIMESTAMP NOT NULL,
	status varchar(10) 
		CHECK(status = 'approved' OR status = 'denied'),
	batch int8 NOT NULL,
	credit_limit int8 NOT NULL,
	interest_rate int8 NOT NULL,
	denied_reason varchar(80),
	denied_at TIMESTAMP
);

CREATE TABLE loans (
	user_id int8 references clients(user_id) NOT NULL,
	loan_id int8 primary key,
	created_at TIMESTAMP NOT NULL,
	due_at TIMESTAMP NOT NULL,
	paid_at TIMESTAMP,
	status varchar(10)
		CHECK(status = 'paid' OR status = 'default' OR status = 'ongoing'),
	loan_amount float8 NOT NULL,
	tax float8 NOT NULL,
	due_amount float8 NOT NULL,
	amount_paid float8 NOT NULL
);


COPY clients(user_id, created_at, status, batch, credit_limit,
			interest_rate, denied_reason, denied_at)
FROM 'C:\Users\loren\Downloads\clients.csv'
DELIMITER ','
CSV HEADER;

COPY loans(user_id, loan_id, created_at, due_at, paid_at, status,
		  loan_amount, tax, due_amount, amount_paid)
FROM 'C:\Users\loren\Downloads\loans.csv'
DELIMITER ','
CSV HEADER;