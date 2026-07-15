public class Logger {

    // Create only one instance
    private static Logger instance;

    // Private constructor
    private Logger() {
        System.out.println("Logger Instance Created");
    }

    // Public method to access instance
    public static Logger getInstance() {

        if (instance == null) {
            instance = new Logger();
        }

        return instance;
    }

    public void log(String message) {
        System.out.println("Log: " + message);
    }
}