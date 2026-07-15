package com.cognizant;

import static org.junit.Assert.assertEquals;

import org.junit.Test;

public class CalculatorTest {

    @Test
    public void testAdd() {
        Calculator calculator = new Calculator();
        assertEquals(10, calculator.add(4, 6));
    }

    @Test
    public void testSubtract() {
        Calculator calculator = new Calculator();
        assertEquals(5, calculator.subtract(10, 5));
    }

    @Test
    public void testMultiply() {
        Calculator calculator = new Calculator();
        assertEquals(20, calculator.multiply(4, 5));
    }

    @Test
    public void testDivide() {
        Calculator calculator = new Calculator();
        assertEquals(5, calculator.divide(20, 4));
    }
}