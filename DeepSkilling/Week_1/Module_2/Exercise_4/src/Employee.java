public class Employee {

    private int employeeId;
    private String name;
    private String position;
    private double salary;

    // Constructor
    public Employee(int employeeId, String name, String position, double salary) {
        this.employeeId = employeeId;
        this.name = name;
        this.position = position;
        this.salary = salary;
    }

    public int getEmployeeId() {
        return employeeId;
    }

    @Override
    public String toString() {
        return "Employee ID: " + employeeId +
                ", Name: " + name +
                ", Position: " + position +
                ", Salary: ₹" + salary;
    }
}