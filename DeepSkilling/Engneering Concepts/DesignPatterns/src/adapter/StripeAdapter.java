package adapter;

public class StripeAdapter implements PaymentProcessor {

    private StripeGateway stripe;

    public StripeAdapter() {

        stripe = new StripeGateway();

    }

    @Override
    public void processPayment(double amount) {

        stripe.payAmount(amount);

    }

}