package inventory;

public class InventoryTest {

    public static void main(String[] args) {

        InventoryManager manager = new InventoryManager();

        manager.addProduct(new Product(101, "Laptop", 10, 55000));
        manager.addProduct(new Product(102, "Mouse", 50, 600));
        manager.addProduct(new Product(103, "Keyboard", 20, 1200));

        System.out.println("\nCurrent Inventory:");
        manager.displayProducts();

        System.out.println("\nUpdating Product...");
        manager.updateProduct(101, 15, 53000);

        System.out.println("\nInventory After Update:");
        manager.displayProducts();

        System.out.println("\nDeleting Product...");
        manager.deleteProduct(102);

        System.out.println("\nFinal Inventory:");
        manager.displayProducts();
    }
}