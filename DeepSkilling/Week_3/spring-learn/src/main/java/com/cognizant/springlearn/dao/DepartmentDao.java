package com.cognizant.springlearn.dao;

import java.util.List;

import org.springframework.context.support.ClassPathXmlApplicationContext;
import org.springframework.stereotype.Repository;

import com.cognizant.springlearn.model.Department;

@Repository
public class DepartmentDao {

    @SuppressWarnings("unchecked")
    public List<Department> getAllDepartments() {

        ClassPathXmlApplicationContext context =
                new ClassPathXmlApplicationContext("employee.xml");

        List<Department> departments =
                (List<Department>) context.getBean("departmentList");

        context.close();

        return departments;
    }
}