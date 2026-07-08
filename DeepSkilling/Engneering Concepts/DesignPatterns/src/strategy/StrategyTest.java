package strategy;

public class StrategyTest {

    public static void main(String[] args) {

        PaymentContext payment;

        payment = new PaymentContext(new CreditCardPayment());
        payment.executePayment(2500);

        payment = new PaymentContext(new PayPalPayment());
        payment.executePayment(5000);

    }

}