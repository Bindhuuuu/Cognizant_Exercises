public class ObserverTest {

    public static void main(String[] args) {

        StockMarket stockMarket = new StockMarket();

        Observer mobileUser = new MobileApp("Bhavya");
        Observer webUser = new WebApp("Rahul");

        stockMarket.registerObserver(mobileUser);
        stockMarket.registerObserver(webUser);

        System.out.println("First Stock Update");
        stockMarket.setStock("TCS", 3800.50);

        System.out.println();

        stockMarket.removeObserver(webUser);

        System.out.println("Second Stock Update");
        stockMarket.setStock("Infosys", 1650.75);

    }

}