public class Main {

    public static void main(String[] args) {

        TaskLinkedList list = new TaskLinkedList();

        list.addTask(new Task(101, "Design Database", "Pending"));
        list.addTask(new Task(102, "Develop Backend", "In Progress"));
        list.addTask(new Task(103, "Testing", "Pending"));

        System.out.println("----- Task List -----");
        list.displayTasks();

        System.out.println("\n----- Search Task -----");
        list.searchTask(102);

        System.out.println("\n----- Delete Task -----");
        list.deleteTask(102);

        System.out.println("\n----- Updated Task List -----");
        list.displayTasks();
    }
}