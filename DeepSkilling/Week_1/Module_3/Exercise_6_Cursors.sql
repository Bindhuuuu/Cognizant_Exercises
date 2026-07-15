SET SERVEROUTPUT ON;

-- Scenario 1
-- Generate Monthly Statements

DECLARE

    CURSOR GenerateMonthlyStatements IS

        SELECT
            T.TransactionID,
            C.Name,
            T.TransactionDate,
            T.Amount,
            T.TransactionType
        FROM Transactions T
        JOIN Accounts A
            ON T.AccountID = A.AccountID
        JOIN Customers C
            ON A.CustomerID = C.CustomerID
        WHERE EXTRACT(MONTH FROM T.TransactionDate) =
              EXTRACT(MONTH FROM SYSDATE)
        AND EXTRACT(YEAR FROM T.TransactionDate) =
              EXTRACT(YEAR FROM SYSDATE);

BEGIN

    DBMS_OUTPUT.PUT_LINE('------ Monthly Statements ------');

    FOR rec IN GenerateMonthlyStatements LOOP

        DBMS_OUTPUT.PUT_LINE(
            'Transaction ID : ' || rec.TransactionID ||
            ' | Customer : ' || rec.Name ||
            ' | Amount : ' || rec.Amount ||
            ' | Type : ' || rec.TransactionType
        );

    END LOOP;

END;
/

-- Verify Scenario 1

SELECT *
FROM Transactions
WHERE EXTRACT(MONTH FROM TransactionDate)=EXTRACT(MONTH FROM SYSDATE);

-- Scenario 2
-- Apply Annual Maintenance Fee

DECLARE

    CURSOR ApplyAnnualFee IS

        SELECT AccountID
        FROM Accounts;

BEGIN

    FOR acc IN ApplyAnnualFee LOOP

        UPDATE Accounts
        SET Balance = Balance - 100
        WHERE AccountID = acc.AccountID;

    END LOOP;

    COMMIT;

    DBMS_OUTPUT.PUT_LINE('Annual maintenance fee applied.');

END;
/

-- Verify Scenario 2

SELECT AccountID,
       Balance
FROM Accounts
ORDER BY AccountID;

-- Scenario 3
-- Update Loan Interest Rates

DECLARE

    CURSOR UpdateLoanInterestRates IS

        SELECT LoanID,
               InterestRate
        FROM Loans;

BEGIN

    FOR loan IN UpdateLoanInterestRates LOOP

        UPDATE Loans
        SET InterestRate = InterestRate + 0.5
        WHERE LoanID = loan.LoanID;

    END LOOP;

    COMMIT;

    DBMS_OUTPUT.PUT_LINE('Loan interest rates updated.');

END;
/

-- Verify Scenario 3

SELECT LoanID,
       InterestRate
FROM Loans
ORDER BY LoanID;