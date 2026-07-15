SET SERVEROUTPUT ON;
-- Scenario 1
-- Automatically update LastModified when
-- Customer details are updated

CREATE OR REPLACE TRIGGER UpdateCustomerLastModified

BEFORE UPDATE
ON Customers

FOR EACH ROW

BEGIN

    :NEW.LastModified := SYSDATE;

END;
/

-- Verify Scenario 1

UPDATE Customers
SET Balance = Balance + 1000
WHERE CustomerID = 1;

SELECT CustomerID,
       Name,
       Balance,
       LastModified
FROM Customers
WHERE CustomerID = 1;

-- Scenario 2
-- Maintain Audit Log for Transactions

CREATE OR REPLACE TRIGGER LogTransaction

AFTER INSERT
ON Transactions

FOR EACH ROW

BEGIN

    INSERT INTO AuditLog(

        AuditID,
        TransactionID,
        Action,
        LogDate

    )

    VALUES(

        (SELECT NVL(MAX(AuditID),0)+1 FROM AuditLog),
        :NEW.TransactionID,
        'Transaction Inserted',
        SYSDATE

    );

END;
/

-- Verify Scenario 2

INSERT INTO Transactions
VALUES(
    2001,
    101,
    SYSDATE,
    2500,
    'Deposit'
);

SELECT *
FROM AuditLog
ORDER BY AuditID;

-- Scenario 3
-- Validate Deposits and Withdrawals

CREATE OR REPLACE TRIGGER CheckTransactionRules

BEFORE INSERT
ON Transactions

FOR EACH ROW

DECLARE

    v_Balance NUMBER;

BEGIN

    SELECT Balance
    INTO v_Balance
    FROM Accounts
    WHERE AccountID = :NEW.AccountID;

    IF :NEW.TransactionType = 'Withdrawal' THEN

        IF :NEW.Amount > v_Balance THEN

            RAISE_APPLICATION_ERROR(
                -20010,
                'Withdrawal exceeds available balance.'
            );

        END IF;

    ELSIF :NEW.TransactionType = 'Deposit' THEN

        IF :NEW.Amount <= 0 THEN

            RAISE_APPLICATION_ERROR(
                -20011,
                'Deposit amount must be positive.'
            );

        END IF;

    END IF;

END;
/

-- Verify Scenario 3

INSERT INTO Transactions
VALUES(
    2002,
    101,
    SYSDATE,
    500,
    'Withdrawal'
);

SELECT *
FROM Transactions
WHERE TransactionID = 2002;