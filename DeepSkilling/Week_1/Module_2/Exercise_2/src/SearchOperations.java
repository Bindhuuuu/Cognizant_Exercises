public class SearchOperations {

    // Linear Search
    public static Product linearSearch(Product[] products, String name) {
        for (Product product : products) {
            if (product.getProductName().equalsIgnoreCase(name)) {
                return product;
            }
        }
        return null;
    }

    // Binary Search (Array must be sorted by productName)
    public static Product binarySearch(Product[] products, String name) {

        int left = 0;
        int right = products.length - 1;

        while (left <= right) {

            int mid = (left + right) / 2;

            int compare = products[mid].getProductName().compareToIgnoreCase(name);

            if (compare == 0) {
                return products[mid];
            }
            else if (compare < 0) {
                left = mid + 1;
            }
            else {
                right = mid - 1;
            }
        }

        return null;
    }
}