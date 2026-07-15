package com.cognizant.ormlearn;

import java.time.LocalDate;
import java.util.List;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.CommandLineRunner;
import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;

import com.cognizant.ormlearn.model.Country;
import com.cognizant.ormlearn.model.Department;
import com.cognizant.ormlearn.model.Employee;
import com.cognizant.ormlearn.service.CountryService;
import com.cognizant.ormlearn.service.DepartmentService;
import com.cognizant.ormlearn.service.EmployeeService;
import com.cognizant.ormlearn.service.StockService;

@SpringBootApplication
public class OrmLearnApplication implements CommandLineRunner {

    @Autowired
    private CountryService countryService;

    @Autowired
    private StockService stockService;

    @Autowired
    private DepartmentService departmentService;

    @Autowired
    private EmployeeService employeeService;

    public static void main(String[] args) {
        SpringApplication.run(OrmLearnApplication.class, args);
    }

    @Override
    public void run(String... args) {

        System.out.println("----- Country List -----");

        List<Country> countries = countryService.getAllCountries();

        for (Country country : countries) {
            System.out.println(country);
        }

        System.out.println("\n----- Country by Code -----");

        Country country = countryService.getCountry("IN");

        System.out.println(country);

        System.out.println("\n----- Add New Country -----");

        Country newCountry = new Country();
        newCountry.setCode("SG");
        newCountry.setName("Singapore");

        countryService.addCountry(newCountry);

        System.out.println("Country Added Successfully");

        System.out.println("\n----- Update Country -----");

        Country updateCountry = countryService.getCountry("SG");
        updateCountry.setName("Singapore Updated");

        countryService.updateCountry(updateCountry);

        System.out.println("Country Updated Successfully");

        System.out.println("\n----- Delete Country -----");

        countryService.deleteCountry("SG");

        System.out.println("Country Deleted Successfully");

        System.out.println("\n----- Search Country -----");

        List<Country> searchCountries = countryService.searchCountry("Uni");

        for (Country c : searchCountries) {
            System.out.println(c);
        }

        System.out.println("\n----- Search Country (Sorted) -----");

        countryService.searchCountrySorted("Uni")
                .forEach(System.out::println);

        System.out.println("\n----- Search Country Starts With -----");

        countryService.searchCountryStartsWith("A")
                .forEach(System.out::println);

        System.out.println("\n----- Search Country Ends With -----");

        countryService.searchCountryEndsWith("a")
                .forEach(System.out::println);

        System.out.println("\n----- Search Exact Country -----");

        System.out.println(countryService.searchCountryExact("India"));

        // ==========================
        // STOCK QUERY METHODS
        // ==========================

        System.out.println("\n----- Stocks Between Dates -----");

        stockService.getStocksBetween(
                LocalDate.of(2019, 9, 1),
                LocalDate.of(2019, 9, 3))
                .forEach(System.out::println);

        System.out.println("\n----- Stocks Closing Greater Than 500 -----");

        stockService.getStocksGreaterThan(500)
                .forEach(System.out::println);

        System.out.println("\n----- Top 3 Highest Volume -----");

        stockService.getTop3Volume()
                .forEach(System.out::println);

        System.out.println("\n----- Netflix Stock Prices -----");

        stockService.getNetflixStocks()
                .forEach(System.out::println);

        // ==========================
        // MANY TO ONE
        // ==========================

        System.out.println("\n----- Employee and Department -----");

        Employee employee = employeeService.getEmployee(1);

        System.out.println("Employee : " + employee.getName());
        System.out.println("Department : " + employee.getDepartment().getName());

        // ==========================
        // ONE TO MANY
        // ==========================

        System.out.println("\n----- Department Employees -----");

        Department department = departmentService.getDepartment(1);

        System.out.println("Department : " + department.getName());

        department.getEmployees().forEach(emp ->
                System.out.println(emp.getName()));

        // ==========================
        // MANY TO MANY
        // ==========================

        System.out.println("\n----- Employee Skills -----");

        employee.getSkills().forEach(skill ->
                System.out.println(skill.getName()));
        
	     // ==========================
	     // HQL QUERY
	     // ==========================
	
	     System.out.println("\n----- HQL Query (Salary > 50000) -----");
	
	     employeeService.getEmployeesBySalary(50000)
	             .forEach(System.out::println);
	
	     // ==========================
	     // NATIVE QUERY
	     // ==========================
	
	     System.out.println("\n----- Native SQL Query -----");
	
	     employeeService.getAllEmployeesNative()
	             .forEach(System.out::println);
    }
}