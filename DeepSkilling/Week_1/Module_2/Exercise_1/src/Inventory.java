import java.util.HashMap;

public class Inventory {

    private HashMap<Integer, Product> products = new HashMap<>();

    // Add Product
    public void addProduct(Product product) {
        products.put(product.getProductId(), product);
        System.out.println("Product added successfully.");
    }

    // Update Product
    public void updateProduct(int productId, int quantity, double price) {

        Product product = products.get(productId);

        if (product != null) {
            product.setQuantity(quantity);
            product.setPrice(price);
            System.out.println("Product updated successfully.");
        } else {
            System.out.println("Product not found.");
        }
    }

    // Delete Product
    public void deleteProduct(int productId) {

        if (products.remove(productId) != null) {
            System.out.println("Product deleted successfully.");
        } else {
            System.out.println("Product not found.");
        }
    }

    // Display Products
    public void displayProducts() {

        if (products.isEmpty()) {
            System.out.println("Inventory is empty.");
            return;
        }

        System.out.println("\nInventory:");

        for (Product product : products.values()) {
            System.out.println(product);
        }
    }
}