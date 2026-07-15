public class Main {

    public static void main(String[] args) {

        Inventory inventory = new Inventory();

        Product p1 = new Product(101, "Laptop", 15, 65000);
        Product p2 = new Product(102, "Mouse", 50, 500);
        Product p3 = new Product(103, "Keyboard", 30, 1200);

        // Add Products
        inventory.addProduct(p1);
        inventory.addProduct(p2);
        inventory.addProduct(p3);

        // Display Inventory
        inventory.displayProducts();

        // Update Product
        inventory.updateProduct(102, 60, 550);

        // Delete Product
        inventory.deleteProduct(103);

        // Display Updated Inventory
        inventory.displayProducts();
    }
}