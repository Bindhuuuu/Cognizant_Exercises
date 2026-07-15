-- Customers Table
CREATE TABLE Customers (
    CustomerID NUMBER PRIMARY KEY,
    Name VARCHAR2(100) NOT NULL,
    DOB DATE NOT NULL,
    Balance NUMBER(12,2) DEFAULT 0,
    IsVIP CHAR(1) DEFAULT 'N',
    LastModified DATE DEFAULT SYSDATE
);

-- Accounts Table
CREATE TABLE Accounts (
    AccountID NUMBER PRIMARY KEY,
    CustomerID NUMBER NOT NULL,
    AccountType VARCHAR2(20) NOT NULL,
    Balance NUMBER(12,2) DEFAULT 0,
    LastModified DATE DEFAULT SYSDATE,
    CONSTRAINT FK_Accounts_Customers
        FOREIGN KEY (CustomerID)
        REFERENCES Customers(CustomerID)
);

-- Transactions Table
CREATE TABLE Transactions (
    TransactionID NUMBER PRIMARY KEY,
    AccountID NUMBER NOT NULL,
    TransactionDate DATE DEFAULT SYSDATE,
    Amount NUMBER(12,2) NOT NULL,
    TransactionType VARCHAR2(20) NOT NULL,
    CONSTRAINT FK_Transactions_Accounts
        FOREIGN KEY (AccountID)
        REFERENCES Accounts(AccountID)
);

-- Loans Table
CREATE TABLE Loans (
    LoanID NUMBER PRIMARY KEY,
    CustomerID NUMBER NOT NULL,
    LoanAmount NUMBER(12,2),
    InterestRate NUMBER(5,2),
    StartDate DATE,
    EndDate DATE,
    CONSTRAINT FK_Loans_Customers
        FOREIGN KEY (CustomerID)
        REFERENCES Customers(CustomerID)
);

-- Employees Table
CREATE TABLE Employees (
    EmployeeID NUMBER PRIMARY KEY,
    Name VARCHAR2(100) NOT NULL,
    Position VARCHAR2(50),
    Salary NUMBER(12,2),
    Department VARCHAR2(50),
    HireDate DATE
);

-- Audit Log Table
CREATE TABLE AuditLog (
    AuditID NUMBER PRIMARY KEY,
    TransactionID NUMBER,
    Action VARCHAR2(100),
    LogDate DATE DEFAULT SYSDATE
);

-- Error Log Table
CREATE TABLE ErrorLog (
    LogID NUMBER PRIMARY KEY,
    ErrorMessage VARCHAR2(500),
    LogDate DATE DEFAULT SYSDATE
);