package com.cognizant.springlearn.dao;

import java.util.List;

import org.springframework.context.support.ClassPathXmlApplicationContext;
import org.springframework.stereotype.Repository;

import com.cognizant.springlearn.model.Employee;

@Repository
public class EmployeeDao {

    @SuppressWarnings("unchecked")
    public List<Employee> getAllEmployees() {

        ClassPathXmlApplicationContext context =
                new ClassPathXmlApplicationContext("employee.xml");

        List<Employee> employees =
                (List<Employee>) context.getBean("employeeList");

        context.close();

        return employees;
    }
}