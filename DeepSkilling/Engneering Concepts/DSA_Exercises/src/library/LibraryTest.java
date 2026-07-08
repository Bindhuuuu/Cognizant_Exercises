package library;

import java.util.Arrays;
import java.util.Comparator;

public class LibraryTest {

    public static void main(String[] args) {

        Book[] books = {

                new Book(101, "Algorithms", "Thomas"),
                new Book(102, "Computer Networks", "Forouzan"),
                new Book(103, "Database Systems", "Navathe"),
                new Book(104, "Java Programming", "Herbert Schildt"),
                new Book(105, "Operating Systems", "Galvin")

        };

        System.out.println("Linear Search:");

        Book result1 = LibrarySearch.linearSearch(books, "Java Programming");

        if (result1 != null)
            System.out.println(result1);
        else
            System.out.println("Book Not Found");

        Arrays.sort(books, Comparator.comparing(Book::getTitle));

        System.out.println("\nBinary Search:");

        Book result2 = LibrarySearch.binarySearch(books, "Java Programming");

        if (result2 != null)
            System.out.println(result2);
        else
            System.out.println("Book Not Found");

    }

}