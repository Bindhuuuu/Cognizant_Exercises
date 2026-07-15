package com.cognizant.springlearn.model;

import java.util.Date;
import java.util.List;

public class Employee {

    private int id;
    private String name;
    private double salary;
    private boolean permanent;
    private Date dateOfBirth;
    private Department department;
    private List<Skill> skillList;

    public Employee() {
    }

    public Employee(int id, String name, double salary, boolean permanent,
                    Date dateOfBirth, Department department, List<Skill> skillList) {
        this.id = id;
        this.name = name;
        this.salary = salary;
        this.permanent = permanent;
        this.dateOfBirth = dateOfBirth;
        this.department = department;
        this.skillList = skillList;
    }

    public int getId() {
        return id;
    }

    public void setId(int id) {
        this.id = id;
    }

    public String getName() {
        return name;
    }

    public void setName(String name) {
        this.name = name;
    }

    public double getSalary() {
        return salary;
    }

    public void setSalary(double salary) {
        this.salary = salary;
    }

    public boolean isPermanent() {
        return permanent;
    }

    public void setPermanent(boolean permanent) {
        this.permanent = permanent;
    }

    public Date getDateOfBirth() {
        return dateOfBirth;
    }

    public void setDateOfBirth(Date dateOfBirth) {
        this.dateOfBirth = dateOfBirth;
    }

    public Department getDepartment() {
        return department;
    }

    public void setDepartment(Department department) {
        this.department = department;
    }

    public List<Skill> getSkillList() {
        return skillList;
    }

    public void setSkillList(List<Skill> skillList) {
        this.skillList = skillList;
    }

    @Override
    public String toString() {
        return "Employee [id=" + id +
                ", name=" + name +
                ", salary=" + salary +
                ", permanent=" + permanent +
                ", dateOfBirth=" + dateOfBirth +
                ", department=" + department +
                ", skillList=" + skillList + "]";
    }
}