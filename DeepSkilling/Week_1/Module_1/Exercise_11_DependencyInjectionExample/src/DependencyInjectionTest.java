public class DependencyInjectionTest {

    public static void main(String[] args) {

        CustomerRepository repository = new CustomerRepositoryImpl();

        CustomerService customerService =
                new CustomerService(repository);

        customerService.displayCustomer(101);

        customerService.displayCustomer(102);

    }

}