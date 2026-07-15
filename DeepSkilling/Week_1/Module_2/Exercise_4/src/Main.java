public class Main {

    public static void main(String[] args) {

        EmployeeArray employeeArray = new EmployeeArray(10);

        employeeArray.addEmployee(new Employee(101, "Bhavya", "Software Engineer", 60000));
        employeeArray.addEmployee(new Employee(102, "Rahul", "Tester", 45000));
        employeeArray.addEmployee(new Employee(103, "Anjali", "Manager", 80000));

        System.out.println("\n----- Employee List -----");
        employeeArray.displayEmployees();

        System.out.println("\n----- Search Employee -----");

        Employee employee = employeeArray.searchEmployee(102);

        if (employee != null)
            System.out.println(employee);
        else
            System.out.println("Employee not found.");

        System.out.println("\n----- Delete Employee -----");

        employeeArray.deleteEmployee(102);

        System.out.println("\n----- Employee List After Deletion -----");

        employeeArray.displayEmployees();
    }
}