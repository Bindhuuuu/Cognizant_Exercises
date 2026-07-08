package observer;

public class ObserverTest {

    public static void main(String[] args) {

        StockMarket stockMarket = new StockMarket();

        Observer mobile = new MobileApp();
        Observer web = new WebApp();

        stockMarket.registerObserver(mobile);
        stockMarket.registerObserver(web);

        stockMarket.setStock("TCS", 4200);

        System.out.println();

        stockMarket.setStock("Infosys", 1650);

    }

}