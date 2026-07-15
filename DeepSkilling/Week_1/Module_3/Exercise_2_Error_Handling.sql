SET SERVEROUTPUT ON;
-- Scenario 1
-- Safe Transfer Funds

CREATE OR REPLACE PROCEDURE SafeTransferFunds (
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

    IF v_Balance < p_Amount THEN
        RAISE_APPLICATION_ERROR(-20001, 'Insufficient Balance');
    END IF;

    UPDATE Accounts
    SET Balance = Balance - p_Amount
    WHERE AccountID = p_FromAccount;

    UPDATE Accounts
    SET Balance = Balance + p_Amount
    WHERE AccountID = p_ToAccount;

    COMMIT;

    DBMS_OUTPUT.PUT_LINE('Funds transferred successfully.');

EXCEPTION

    WHEN NO_DATA_FOUND THEN
        ROLLBACK;
        DBMS_OUTPUT.PUT_LINE('Account not found.');

    WHEN OTHERS THEN
        ROLLBACK;
        DBMS_OUTPUT.PUT_LINE(SQLERRM);

END;
/

-- Verify Scenario 1

BEGIN
    SafeTransferFunds(101,102,1000);
END;
/

SELECT AccountID,
       Balance
FROM Accounts
WHERE AccountID IN (101,102);

-- Scenario 2
-- Update Employee Salary

CREATE OR REPLACE PROCEDURE UpdateSalary(
    p_EmployeeID NUMBER,
    p_Percentage NUMBER
)
IS
BEGIN

    UPDATE Employees
    SET Salary = Salary + (Salary * p_Percentage / 100)
    WHERE EmployeeID = p_EmployeeID;

    IF SQL%ROWCOUNT = 0 THEN
        RAISE_APPLICATION_ERROR(-20002,'Employee ID not found');
    END IF;

    COMMIT;

    DBMS_OUTPUT.PUT_LINE('Salary updated successfully.');

EXCEPTION

    WHEN OTHERS THEN
        ROLLBACK;
        DBMS_OUTPUT.PUT_LINE(SQLERRM);

END;
/

-- Verify Scenario 2

BEGIN
    UpdateSalary(2,10);
END;
/

SELECT EmployeeID,
       Name,
       Salary
FROM Employees
WHERE EmployeeID = 2;

-- Scenario 3
-- Add New Customer

CREATE OR REPLACE PROCEDURE AddNewCustomer(

    p_ID NUMBER,
    p_Name VARCHAR2,
    p_DOB DATE,
    p_Balance NUMBER

)
IS
BEGIN

    INSERT INTO Customers
    (
        CustomerID,
        Name,
        DOB,
        Balance,
        IsVIP,
        LastModified
    )

    VALUES
    (
        p_ID,
        p_Name,
        p_DOB,
        p_Balance,
        'N',
        SYSDATE
    );

    COMMIT;

    DBMS_OUTPUT.PUT_LINE('Customer added successfully.');

EXCEPTION

    WHEN DUP_VAL_ON_INDEX THEN

        ROLLBACK;

        DBMS_OUTPUT.PUT_LINE('Customer ID already exists.');

    WHEN OTHERS THEN

        ROLLBACK;

        DBMS_OUTPUT.PUT_LINE(SQLERRM);

END;
/

-- Verify Scenario 3

BEGIN
    AddNewCustomer(
        11,
        'Chris Evans',
        TO_DATE('1992-08-15','YYYY-MM-DD'),
        9000
    );
END;
/

SELECT *
FROM Customers
WHERE CustomerID = 11;