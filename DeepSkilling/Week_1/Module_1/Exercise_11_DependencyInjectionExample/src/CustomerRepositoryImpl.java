public class CustomerRepositoryImpl implements CustomerRepository {

    @Override
    public String findCustomerById(int id) {

        if (id == 101) {
            return "Customer ID: 101, Name: Ramtej";
        }

        return "Customer not found.";

    }

}