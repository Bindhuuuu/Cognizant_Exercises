public class Task {

    private int taskId;
    private String taskName;
    private String status;

    public Task(int taskId, String taskName, String status) {
        this.taskId = taskId;
        this.taskName = taskName;
        this.status = status;
    }

    public int getTaskId() {
        return taskId;
    }

    @Override
    public String toString() {
        return "Task ID: " + taskId +
                ", Task Name: " + taskName +
                ", Status: " + status;
    }
}