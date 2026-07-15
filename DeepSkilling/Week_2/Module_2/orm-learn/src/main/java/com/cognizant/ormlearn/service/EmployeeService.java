package com.cognizant.ormlearn.service;

import java.util.List;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import com.cognizant.ormlearn.model.Employee;
import com.cognizant.ormlearn.repository.EmployeeRepository;

@Service
public class EmployeeService {

    @Autowired
    private EmployeeRepository employeeRepository;

    public List<Employee> getAllEmployees() {
        return employeeRepository.findAll();
    }

    @Transactional
    public Employee getEmployee(int id) {
        return employeeRepository.findById(id).orElse(null);
    }

    public List<Employee> getEmployeesBySalary(double salary) {
        return employeeRepository.getEmployeesBySalary(salary);
    }

    public List<Employee> getAllEmployeesNative() {
        return employeeRepository.getAllEmployeesNative();
    }
}