package sorting;

public class SortingTest {

    public static void main(String[] args) {

        Order[] orders = {

                new Order(101, "Rahul", 2500),
                new Order(102, "Priya", 5000),
                new Order(103, "Amit", 1200),
                new Order(104, "Sneha", 4000)

        };

        System.out.println("Original Orders:");

        for (Order order : orders)
            System.out.println(order);

        // Bubble Sort
        SortingOperations.bubbleSort(orders);

        System.out.println("\nAfter Bubble Sort:");

        for (Order order : orders)
            System.out.println(order);

        // New Array for Quick Sort
        Order[] orders2 = {

                new Order(101, "Rahul", 2500),
                new Order(102, "Priya", 5000),
                new Order(103, "Amit", 1200),
                new Order(104, "Sneha", 4000)

        };

        SortingOperations.quickSort(orders2, 0, orders2.length - 1);

        System.out.println("\nAfter Quick Sort:");

        for (Order order : orders2)
            System.out.println(order);

    }
}