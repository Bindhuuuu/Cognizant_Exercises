public class QuickSort {

    public static void sort(Order[] orders, int low, int high) {

        if (low < high) {

            int pivotIndex = partition(orders, low, high);

            sort(orders, low, pivotIndex - 1);
            sort(orders, pivotIndex + 1, high);

        }
    }

    private static int partition(Order[] orders, int low, int high) {

        double pivot = orders[high].getTotalPrice();

        int i = low - 1;

        for (int j = low; j < high; j++) {

            if (orders[j].getTotalPrice() <= pivot) {

                i++;

                Order temp = orders[i];
                orders[i] = orders[j];
                orders[j] = temp;

            }
        }

        Order temp = orders[i + 1];
        orders[i + 1] = orders[high];
        orders[high] = temp;

        return i + 1;
    }
}