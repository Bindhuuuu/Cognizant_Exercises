public class Main {

    public static void displayOrders(Order[] orders) {

        for (Order order : orders) {
            System.out.println(order);
        }
    }

    public static void main(String[] args) {

        Order[] orders1 = {
                new Order(101, "Bhavya", 2500),
                new Order(102, "Rahul", 1200),
                new Order(103, "Anjali", 5600),
                new Order(104, "Kiran", 3400),
                new Order(105, "Sneha", 1800)
        };

        System.out.println("----- Original Orders -----");
        displayOrders(orders1);

        BubbleSort.sort(orders1);

        System.out.println("\n----- After Bubble Sort -----");
        displayOrders(orders1);

        // New array for Quick Sort
        Order[] orders2 = {
                new Order(101, "Bhavya", 2500),
                new Order(102, "Rahul", 1200),
                new Order(103, "Anjali", 5600),
                new Order(104, "Kiran", 3400),
                new Order(105, "Sneha", 1800)
        };

        QuickSort.sort(orders2, 0, orders2.length - 1);

        System.out.println("\n----- After Quick Sort -----");
        displayOrders(orders2);
    }
}