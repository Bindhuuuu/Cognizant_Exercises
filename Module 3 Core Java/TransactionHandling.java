import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.PreparedStatement;

public class TransactionHandling {
    public static void main(String[] args) {
        String url = "jdbc:mysql://localhost:3306/studentdb";
        String username = "root";
        String password = "your_password";

        try {
            Connection con = DriverManager.getConnection(url, username, password);

            con.setAutoCommit(false);

            PreparedStatement debit = con.prepareStatement(
                "UPDATE accounts SET balance = balance - ? WHERE id = ?");
            debit.setInt(1, 1000);
            debit.setInt(2, 1);
            debit.executeUpdate();

            PreparedStatement credit = con.prepareStatement(
                "UPDATE accounts SET balance = balance + ? WHERE id = ?");
            credit.setInt(1, 1000);
            credit.setInt(2, 2);
            credit.executeUpdate();

            con.commit();
            System.out.println("Transaction Successful.");

            con.close();
        } catch (Exception e) {
            System.out.println("Transaction Failed.");
            System.out.println(e);
        }
    }
}