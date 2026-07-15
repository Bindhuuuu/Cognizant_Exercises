public class TaskLinkedList {

    private Node head;

    // Add Task
    public void addTask(Task task) {

        Node newNode = new Node(task);

        if (head == null) {
            head = newNode;
            return;
        }

        Node current = head;

        while (current.next != null) {
            current = current.next;
        }

        current.next = newNode;
    }

    // Search Task
    public void searchTask(int taskId) {

        Node current = head;

        while (current != null) {

            if (current.task.getTaskId() == taskId) {
                System.out.println(current.task);
                return;
            }

            current = current.next;
        }

        System.out.println("Task not found.");
    }

    // Display Tasks
    public void displayTasks() {

        if (head == null) {
            System.out.println("No tasks available.");
            return;
        }

        Node current = head;

        while (current != null) {
            System.out.println(current.task);
            current = current.next;
        }
    }

    // Delete Task
    public void deleteTask(int taskId) {

        if (head == null) {
            System.out.println("List is empty.");
            return;
        }

        if (head.task.getTaskId() == taskId) {
            head = head.next;
            System.out.println("Task deleted successfully.");
            return;
        }

        Node current = head;

        while (current.next != null &&
               current.next.task.getTaskId() != taskId) {

            current = current.next;
        }

        if (current.next == null) {
            System.out.println("Task not found.");
        } else {
            current.next = current.next.next;
            System.out.println("Task deleted successfully.");
        }
    }
}