package singleton;

public class Logger {

    // Step 1: Create a private static instance
    private static Logger instance;

    // Step 2: Private constructor
    private Logger() {
        System.out.println("Logger Instance Created");
    }

    // Step 3: Public method to get the instance
    public static Logger getInstance() {
        if (instance == null) {
            instance = new Logger();
        }
        return instance;
    }

    // Logging method
    public void log(String message) {
        System.out.println("LOG: " + message);
    }
}