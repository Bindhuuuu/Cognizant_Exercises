package task;

public class TaskTest {

    public static void main(String[] args) {

        TaskManager manager = new TaskManager();

        manager.addTask(new Task(101, "Design UI", "Pending"));
        manager.addTask(new Task(102, "Develop Backend", "In Progress"));
        manager.addTask(new Task(103, "Testing", "Pending"));

        System.out.println("\nTask List:");

        manager.displayTasks();

        System.out.println("\nSearching Task:");

        Task task = manager.searchTask(102);

        if (task != null)
            System.out.println(task);
        else
            System.out.println("Task Not Found.");

        System.out.println("\nDeleting Task:");

        manager.deleteTask(102);

        System.out.println("\nTask List After Deletion:");

        manager.displayTasks();

    }

}