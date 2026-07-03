import java.util.Arrays;
import java.util.List;

record Person(String name, int age) {}

public class RecordsExample {
    public static void main(String[] args) {
        Person p1 = new Person("Rahul", 20);
        Person p2 = new Person("Priya", 25);
        Person p3 = new Person("Arjun", 17);

        System.out.println("Person Details:");
        System.out.println(p1);
        System.out.println(p2);
        System.out.println(p3);

        List<Person> people = Arrays.asList(p1, p2, p3);

        System.out.println("\nPeople with age 18 or above:");
        people.stream()
              .filter(person -> person.age() >= 18)
              .forEach(System.out::println);
    }
}