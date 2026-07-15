SET SERVEROUTPUT ON;

-- Scenario 1
-- Process Monthly Interest
-- Apply 1% interest to all Savings Accounts

CREATE OR REPLACE PROCEDURE ProcessMonthlyInterest
IS
BEGIN

    UPDATE Accounts
    SET Balance = Balance + (Balance * 0.01)
    WHERE AccountType = 'Savings';

    COMMIT;

    DBMS_OUTPUT.PUT_LINE('Monthly interest processed successfully.');

END;
/

-- Verify Scenario 1

BEGIN
    ProcessMonthlyInterest;
END;
/

SELECT AccountID,
       AccountType,
       Balance
FROM Accounts
WHERE AccountType = 'Savings'
ORDER BY AccountID;

-- Scenario 2
-- Update Employee Bonus
-- Add bonus percentage to employees of a department

CREATE OR REPLACE PROCEDURE UpdateEmployeeBonus(

    p_Department VARCHAR2,
    p_BonusPercent NUMBER

)
IS
BEGIN

    UPDATE Employees
    SET Salary = Salary + (Salary * p_BonusPercent / 100)
    WHERE Department = p_Department;

    COMMIT;

    DBMS_OUTPUT.PUT_LINE('Employee bonus updated successfully.');

END;
/

-- Verify Scenario 2

BEGIN
    UpdateEmployeeBonus('IT',10);
END;
/

SELECT EmployeeID,
       Name,
       Department,
       Salary
FROM Employees
WHERE Department='IT'
ORDER BY EmployeeID;

-- Scenario 3
-- Transfer Funds
-- Transfer amount between two accounts

CREATE OR REPLACE PROCEDURE TransferFunds(

    p_FromAccount NUMBER,
    p_ToAccount NUMBER,
    p_Amount NUMBER

)
IS

    v_Balance NUMBER;

BEGIN

    SELECT Balance
    INTO v_Balance
    FROM Accounts
    WHERE AccountID = p_FromAccount;

    IF v_Balance >= p_Amount THEN

        UPDATE Accounts
        SET Balance = Balance - p_Amount
        WHERE AccountID = p_FromAccount;

        UPDATE Accounts
        SET Balance = Balance + p_Amount
        WHERE AccountID = p_ToAccount;

        COMMIT;

        DBMS_OUTPUT.PUT_LINE('Funds transferred successfully.');

    ELSE

        DBMS_OUTPUT.PUT_LINE('Insufficient Balance.');

    END IF;

EXCEPTION

    WHEN NO_DATA_FOUND THEN

        DBMS_OUTPUT.PUT_LINE('Account not found.');

    WHEN OTHERS THEN

        ROLLBACK;

        DBMS_OUTPUT.PUT_LINE(SQLERRM);

END;
/

-- Verify Scenario 3

BEGIN
    TransferFunds(101,102,500);
END;
/

SELECT AccountID,
       Balance
FROM Accounts
WHERE AccountID IN (101,102)
ORDER BY AccountID;