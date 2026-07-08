package employee;

public class EmployeeTest {

    public static void main(String[] args) {

        EmployeeManager manager = new EmployeeManager();

        manager.addEmployee(new Employee(101, "Rahul", "Manager", 60000));
        manager.addEmployee(new Employee(102, "Priya", "Developer", 50000));
        manager.addEmployee(new Employee(103, "Amit", "Tester", 45000));

        System.out.println("\nEmployee List:");

        manager.displayEmployees();

        System.out.println("\nSearching Employee:");

        Employee employee = manager.searchEmployee(102);

        if (employee != null)
            System.out.println(employee);
        else
            System.out.println("Employee Not Found.");

        System.out.println("\nDeleting Employee:");

        manager.deleteEmployee(102);

        System.out.println("\nEmployee List After Deletion:");

        manager.displayEmployees();

    }

}