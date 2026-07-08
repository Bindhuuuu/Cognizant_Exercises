package employee;

public class EmployeeManager {

    private Employee[] employees = new Employee[10];
    private int count = 0;

    // Add Employee
    public void addEmployee(Employee employee) {

        if (count < employees.length) {

            employees[count] = employee;
            count++;

            System.out.println("Employee Added Successfully.");

        } else {

            System.out.println("Array is Full.");

        }

    }

    // Search Employee
    public Employee searchEmployee(int id) {

        for (int i = 0; i < count; i++) {

            if (employees[i].getEmployeeId() == id)
                return employees[i];

        }

        return null;

    }

    // Traverse Employees
    public void displayEmployees() {

        for (int i = 0; i < count; i++) {

            System.out.println(employees[i]);

        }

    }

    // Delete Employee
    public void deleteEmployee(int id) {

        int index = -1;

        for (int i = 0; i < count; i++) {

            if (employees[i].getEmployeeId() == id) {

                index = i;
                break;

            }

        }

        if (index == -1) {

            System.out.println("Employee Not Found.");
            return;

        }

        for (int i = index; i < count - 1; i++) {

            employees[i] = employees[i + 1];

        }

        employees[count - 1] = null;
        count--;

        System.out.println("Employee Deleted Successfully.");

    }

}