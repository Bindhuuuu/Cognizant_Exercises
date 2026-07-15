public class MobileApp implements Observer {

    private String userName;

    public MobileApp(String userName) {
        this.userName = userName;
    }

    @Override
    public void update(String stockName, double price) {
        System.out.println(userName +
                " (Mobile App): " +
                stockName +
                " price updated to ₹" +
                price);
    }

}