import java.util.concurrent.Callable;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;
import java.util.concurrent.Future;

public class ExecutorServiceExample {
    public static void main(String[] args) {
        ExecutorService executor = Executors.newFixedThreadPool(3);

        Callable<String> task1 = () -> "Task 1 Completed";
        Callable<String> task2 = () -> "Task 2 Completed";
        Callable<String> task3 = () -> "Task 3 Completed";

        try {
            Future<String> result1 = executor.submit(task1);
            Future<String> result2 = executor.submit(task2);
            Future<String> result3 = executor.submit(task3);

            System.out.println(result1.get());
            System.out.println(result2.get());
            System.out.println(result3.get());
        } catch (Exception e) {
            System.out.println(e);
        }

        executor.shutdown();
    }
}