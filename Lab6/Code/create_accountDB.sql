

-- Create the Accounts table
CREATE TABLE Accounts (
    account INTEGER PRIMARY KEY,
    balance INTEGER NOT NULL
);

-- Insert company account (account 0), initial balance 100
INSERT INTO Accounts (account, balance)
VALUES (0, 100);

-- Insert employee accounts (accounts 1 to 100), initial balance 0
INSERT INTO Accounts (account, balance)
SELECT generate_series(1, 100), 0;


