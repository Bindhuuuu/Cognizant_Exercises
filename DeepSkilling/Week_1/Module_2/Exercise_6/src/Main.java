import java.util.Arrays;
import java.util.Comparator;

public class Main {

    public static void main(String[] args) {

        Book[] books = {
                new Book(101, "Java Programming", "James Gosling"),
                new Book(102, "Data Structures", "Mark Allen"),
                new Book(103, "Operating Systems", "Galvin"),
                new Book(104, "Computer Networks", "Andrew Tanenbaum"),
                new Book(105, "Database Systems", "Elmasri")
        };

        // Linear Search
        System.out.println("----- Linear Search -----");

        Book result1 = LibrarySearch.linearSearch(books, "Operating Systems");

        if (result1 != null)
            System.out.println(result1);
        else
            System.out.println("Book not found.");

        // Sort array before Binary Search
        Arrays.sort(books, Comparator.comparing(Book::getTitle));

        // Binary Search
        System.out.println("\n----- Binary Search -----");

        Book result2 = LibrarySearch.binarySearch(books, "Operating Systems");

        if (result2 != null)
            System.out.println(result2);
        else
            System.out.println("Book not found.");
    }
}