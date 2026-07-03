import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

public class LambdaExpressionExample {
    public static void main(String[] args) {
        List<String> names = new ArrayList<>();

        names.add("Rahul");
        names.add("Priya");
        names.add("Arjun");
        names.add("Bhavya");

        Collections.sort(names, (a, b) -> a.compareTo(b));

        System.out.println("Sorted List:");
        for (String name : names) {
            System.out.println(name);
        }
    }
}