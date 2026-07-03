public class PatternMatchingSwitch {
    static void checkType(Object obj) {
        switch (obj) {
            case Integer i -> System.out.println(i + " is an Integer");
            case String s -> System.out.println(s + " is a String");
            case Double d -> System.out.println(d + " is a Double");
            case null -> System.out.println("Object is null");
            default -> System.out.println("Unknown Type");
        }
    }

    public static void main(String[] args) {
        checkType(100);
        checkType("Hello");
        checkType(25.5);
        checkType(true);
        checkType(null);
    }
}