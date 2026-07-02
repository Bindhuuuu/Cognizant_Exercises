import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

public class LambdaExample {

    public static void main(String[] args) {

        List<String> names = new ArrayList<>();

        names.add("Rahul");
        names.add("Ankit");
        names.add("Priya");
        names.add("Sneha");

        Collections.sort(names, (a, b) -> a.compareTo(b));

        System.out.println("Sorted List:");

        names.forEach(System.out::println);
    }
}