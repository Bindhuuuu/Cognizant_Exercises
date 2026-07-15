public class StrategyTest {

    public static void main(String[] args) {

        PaymentContext paymentContext =
                new PaymentContext(new CreditCardPayment());

        paymentContext.executePayment(5000);

        paymentContext.setPaymentStrategy(new PayPalPayment());

        paymentContext.executePayment(2500);

    }

}