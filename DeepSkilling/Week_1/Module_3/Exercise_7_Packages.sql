SET SERVEROUTPUT ON;

-- Scenario 1
-- Customer Management Package

CREATE OR REPLACE PACKAGE CustomerManagement AS

    PROCEDURE AddCustomer(
        p_ID NUMBER,
        p_Name VARCHAR2,
        p_DOB DATE,
        p_Balance NUMBER
    );

    PROCEDURE UpdateCustomerBalance(
        p_ID NUMBER,
        p_Balance NUMBER
    );

    FUNCTION GetCustomerBalance(
        p_ID NUMBER
    ) RETURN NUMBER;

END CustomerManagement;
/

CREATE OR REPLACE PACKAGE BODY CustomerManagement AS

    PROCEDURE AddCustomer(
        p_ID NUMBER,
        p_Name VARCHAR2,
        p_DOB DATE,
        p_Balance NUMBER
    )
    IS
    BEGIN

        INSERT INTO Customers
        VALUES(
            p_ID,
            p_Name,
            p_DOB,
            p_Balance,
            'N',
            SYSDATE
        );

        COMMIT;

        DBMS_OUTPUT.PUT_LINE('Customer Added Successfully.');

    END;

    PROCEDURE UpdateCustomerBalance(
        p_ID NUMBER,
        p_Balance NUMBER
    )
    IS
    BEGIN

        UPDATE Customers
        SET Balance = p_Balance
        WHERE CustomerID = p_ID;

        COMMIT;

        DBMS_OUTPUT.PUT_LINE('Customer Balance Updated.');

    END;

    FUNCTION GetCustomerBalance(
        p_ID NUMBER
    )

    RETURN NUMBER

    IS

        v_Balance NUMBER;

    BEGIN

        SELECT Balance
        INTO v_Balance
        FROM Customers
        WHERE CustomerID = p_ID;

        RETURN v_Balance;

    END;

END CustomerManagement;
/

-- Verify Scenario 1

BEGIN
    CustomerManagement.AddCustomer(
        12,
        'Tony Stark',
        TO_DATE('1975-05-29','YYYY-MM-DD'),
        50000
    );
END;
/

BEGIN
    CustomerManagement.UpdateCustomerBalance(12,60000);
END;
/

SELECT CustomerManagement.GetCustomerBalance(12)
AS Customer_Balance
FROM Dual;

-- Scenario 2
-- Employee Management Package

CREATE OR REPLACE PACKAGE EmployeeManagement AS

    PROCEDURE HireEmployee(
        p_ID NUMBER,
        p_Name VARCHAR2,
        p_Position VARCHAR2,
        p_Salary NUMBER,
        p_Department VARCHAR2,
        p_HireDate DATE
    );

    PROCEDURE UpdateEmployeeSalary(
        p_ID NUMBER,
        p_Salary NUMBER
    );

    FUNCTION CalculateAnnualSalary(
        p_ID NUMBER
    ) RETURN NUMBER;

END EmployeeManagement;
/

CREATE OR REPLACE PACKAGE BODY EmployeeManagement AS

    PROCEDURE HireEmployee(
        p_ID NUMBER,
        p_Name VARCHAR2,
        p_Position VARCHAR2,
        p_Salary NUMBER,
        p_Department VARCHAR2,
        p_HireDate DATE
    )
    IS
    BEGIN

        INSERT INTO Employees
        VALUES(
            p_ID,
            p_Name,
            p_Position,
            p_Salary,
            p_Department,
            p_HireDate
        );

        COMMIT;

        DBMS_OUTPUT.PUT_LINE('Employee Hired.');

    END;

    PROCEDURE UpdateEmployeeSalary(
        p_ID NUMBER,
        p_Salary NUMBER
    )
    IS
    BEGIN

        UPDATE Employees
        SET Salary = p_Salary
        WHERE EmployeeID = p_ID;

        COMMIT;

        DBMS_OUTPUT.PUT_LINE('Salary Updated.');

    END;

    FUNCTION CalculateAnnualSalary(
        p_ID NUMBER
    )

    RETURN NUMBER

    IS

        v_Salary NUMBER;

    BEGIN

        SELECT Salary
        INTO v_Salary
        FROM Employees
        WHERE EmployeeID = p_ID;

        RETURN v_Salary * 12;

    END;

END EmployeeManagement;
/

-- Verify Scenario 2

BEGIN
    EmployeeManagement.HireEmployee(
        11,
        'Steve Rogers',
        'Developer',
        70000,
        'IT',
        SYSDATE
    );
END;
/

BEGIN
    EmployeeManagement.UpdateEmployeeSalary(
        11,
        75000
    );
END;
/

SELECT EmployeeManagement.CalculateAnnualSalary(11)
AS Annual_Salary
FROM Dual;

-- Scenario 3
-- Account Operations Package

CREATE OR REPLACE PACKAGE AccountOperations AS

    PROCEDURE OpenAccount(
        p_AccountID NUMBER,
        p_CustomerID NUMBER,
        p_AccountType VARCHAR2,
        p_Balance NUMBER
    );

    PROCEDURE CloseAccount(
        p_AccountID NUMBER
    );

    FUNCTION GetTotalBalance(
        p_CustomerID NUMBER
    ) RETURN NUMBER;

END AccountOperations;
/

CREATE OR REPLACE PACKAGE BODY AccountOperations AS

    PROCEDURE OpenAccount(
        p_AccountID NUMBER,
        p_CustomerID NUMBER,
        p_AccountType VARCHAR2,
        p_Balance NUMBER
    )
    IS
    BEGIN

        INSERT INTO Accounts
        VALUES(
            p_AccountID,
            p_CustomerID,
            p_AccountType,
            p_Balance,
            SYSDATE
        );

        COMMIT;

        DBMS_OUTPUT.PUT_LINE('Account Opened.');

    END;

    PROCEDURE CloseAccount(
        p_AccountID NUMBER
    )
    IS
    BEGIN

        DELETE FROM Accounts
        WHERE AccountID = p_AccountID;

        COMMIT;

        DBMS_OUTPUT.PUT_LINE('Account Closed.');

    END;

    FUNCTION GetTotalBalance(
        p_CustomerID NUMBER
    )

    RETURN NUMBER

    IS

        v_Total NUMBER;

    BEGIN

        SELECT SUM(Balance)
        INTO v_Total
        FROM Accounts
        WHERE CustomerID = p_CustomerID;

        RETURN NVL(v_Total,0);

    END;

END AccountOperations;
/

-- Verify Scenario 3

BEGIN
    AccountOperations.OpenAccount(
        111,
        12,
        'Savings',
        15000
    );
END;
/

SELECT AccountOperations.GetTotalBalance(12)
AS Total_Balance
FROM Dual;

BEGIN
    AccountOperations.CloseAccount(111);
END;
/

SELECT *
FROM Accounts
WHERE AccountID = 111;