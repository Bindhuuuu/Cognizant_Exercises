public class VirtualThreadsExample {
    public static void main(String[] args) {
        for (int i = 1; i <= 10; i++) {
            int threadNumber = i;
            Thread.startVirtualThread(() -> {
                System.out.println("Hello from Virtual Thread " + threadNumber);
            });
        }

        try {
            Thread.sleep(1000);
        } catch (InterruptedException e) {
            System.out.println(e);
        }
    }
}