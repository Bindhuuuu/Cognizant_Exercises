package search;

import java.util.Arrays;
import java.util.Comparator;

public class SearchTest {

    public static void main(String[] args) {

        Product[] products = {

                new Product(101, "Laptop", "Electronics"),
                new Product(102, "Mouse", "Accessories"),
                new Product(103, "Keyboard", "Accessories"),
                new Product(104, "Monitor", "Electronics"),
                new Product(105, "Printer", "Office")

        };

        // Linear Search
        System.out.println("Linear Search:");
        Product result1 = SearchOperations.linearSearch(products, "Keyboard");

        if (result1 != null)
            System.out.println(result1);
        else
            System.out.println("Product Not Found");

        // Sort array for Binary Search
        Arrays.sort(products, Comparator.comparing(Product::getProductName));

        // Binary Search
        System.out.println("\nBinary Search:");
        Product result2 = SearchOperations.binarySearch(products, "Keyboard");

        if (result2 != null)
            System.out.println(result2);
        else
            System.out.println("Product Not Found");

    }
}