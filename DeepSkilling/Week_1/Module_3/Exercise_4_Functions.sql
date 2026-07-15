SET SERVEROUTPUT ON;

-- Scenario 1
-- Calculate Customer Age

CREATE OR REPLACE FUNCTION CalculateAge(

    p_DOB DATE

)

RETURN NUMBER

IS

    v_Age NUMBER;

BEGIN

    v_Age := FLOOR(MONTHS_BETWEEN(SYSDATE,p_DOB)/12);

    RETURN v_Age;

END;
/

-- Verify Scenario 1

SELECT CustomerID,
       Name,
       CalculateAge(DOB) AS Age
FROM Customers
ORDER BY CustomerID;

-- Scenario 2
-- Calculate Monthly Loan Installment

CREATE OR REPLACE FUNCTION CalculateMonthlyInstallment(

    p_LoanAmount NUMBER,
    p_InterestRate NUMBER,
    p_Years NUMBER

)

RETURN NUMBER

IS

    v_TotalAmount NUMBER;
    v_MonthlyInstallment NUMBER;

BEGIN

    v_TotalAmount :=
        p_LoanAmount +
        (p_LoanAmount * p_InterestRate * p_Years /100);

    v_MonthlyInstallment :=
        v_TotalAmount / (p_Years*12);

    RETURN ROUND(v_MonthlyInstallment,2);

END;
/

-- Verify Scenario 2

SELECT LoanID,
       LoanAmount,
       InterestRate,
       CalculateMonthlyInstallment(
            LoanAmount,
            InterestRate,
            5
       ) AS Monthly_Installment
FROM Loans
ORDER BY LoanID;

-- Scenario 3
-- Check Sufficient Balance

CREATE OR REPLACE FUNCTION HasSufficientBalance(

    p_AccountID NUMBER,
    p_Amount NUMBER

)

RETURN VARCHAR2

IS

    v_Balance NUMBER;

BEGIN

    SELECT Balance
    INTO v_Balance
    FROM Accounts
    WHERE AccountID = p_AccountID;

    IF v_Balance >= p_Amount THEN
        RETURN 'YES';
    ELSE
        RETURN 'NO';
    END IF;

EXCEPTION

    WHEN NO_DATA_FOUND THEN
        RETURN 'ACCOUNT NOT FOUND';

END;
/

-- Verify Scenario 3

SELECT AccountID,
       Balance,
       HasSufficientBalance(AccountID,5000) AS Status
FROM Accounts
ORDER BY AccountID;