package com.cognizant;

import static org.junit.Assert.assertEquals;

import org.junit.After;
import org.junit.Before;
import org.junit.Test;

public class BankAccountTest {

    private BankAccount account;

    @Before
    public void setUp() {
        account = new BankAccount(1000);
        System.out.println("Setup Complete");
    }

    @After
    public void tearDown() {
        System.out.println("Test Finished");
    }

    @Test
    public void testDeposit() {

        // Arrange
        double amount = 500;

        // Act
        account.deposit(amount);

        // Assert
        assertEquals(1500, account.getBalance(), 0.001);
    }

    @Test
    public void testWithdraw() {

        // Arrange
        double amount = 300;

        // Act
        account.withdraw(amount);

        // Assert
        assertEquals(700, account.getBalance(), 0.001);
    }
}