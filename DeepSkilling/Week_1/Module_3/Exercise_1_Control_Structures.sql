SET SERVEROUTPUT ON;
--Senario 1
BEGIN
    FOR cust IN (
        SELECT CustomerID,
               FLOOR(MONTHS_BETWEEN(SYSDATE, DOB)/12) AS Age
        FROM Customers
    )
    LOOP
        IF cust.Age > 60 THEN

            UPDATE Loans
            SET InterestRate = InterestRate - 1
            WHERE CustomerID = cust.CustomerID;

            DBMS_OUTPUT.PUT_LINE(
                'Interest rate updated for Customer ID : '
                || cust.CustomerID
            );

        END IF;
    END LOOP;

    COMMIT;
END;
/

-- Verify Scenario 1
SELECT CustomerID,
       InterestRate
FROM Loans
ORDER BY CustomerID;

-- Scenario 2
-- Promote customers to VIP
-- if balance is greater than 10000

BEGIN
    FOR cust IN (
        SELECT CustomerID,
               Balance
        FROM Customers
    )
    LOOP

        IF cust.Balance > 10000 THEN

            UPDATE Customers
            SET IsVIP = 'Y'
            WHERE CustomerID = cust.CustomerID;

            DBMS_OUTPUT.PUT_LINE(
                'Customer '
                || cust.CustomerID
                || ' promoted to VIP.'
            );

        END IF;

    END LOOP;

    COMMIT;
END;
/

-- Verify Scenario 2
SELECT CustomerID,
       Name,
       Balance,
       IsVIP
FROM Customers
ORDER BY CustomerID;

-- Scenario 3
-- Print reminder for loans
-- due within next 30 days

BEGIN

    FOR loan IN (

        SELECT LoanID,
               CustomerID,
               EndDate
        FROM Loans
        WHERE EndDate BETWEEN SYSDATE
                          AND SYSDATE + 30

    )

    LOOP

        DBMS_OUTPUT.PUT_LINE(

            'Reminder : Customer '
            || loan.CustomerID
            || ' | Loan ID : '
            || loan.LoanID
            || ' | Due Date : '
            || TO_CHAR(loan.EndDate,'DD-MON-YYYY')

        );

    END LOOP;

END;
/

-- Verify Scenario 3
SELECT LoanID,
       CustomerID,
       EndDate
FROM Loans
WHERE EndDate BETWEEN SYSDATE
                  AND SYSDATE + 30
ORDER BY EndDate;