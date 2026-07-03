import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.PreparedStatement;

public class StudentDAO {
    static String url = "jdbc:mysql://localhost:3306/studentdb";
    static String username = "root";
    static String password = "your_password";

    public static void insertStudent(int id, String name, int age) {
        try {
            Connection con = DriverManager.getConnection(url, username, password);
            String sql = "INSERT INTO students VALUES (?, ?, ?)";
            PreparedStatement ps = con.prepareStatement(sql);

            ps.setInt(1, id);
            ps.setString(2, name);
            ps.setInt(3, age);

            ps.executeUpdate();
            System.out.println("Student inserted successfully.");

            con.close();
        } catch (Exception e) {
            System.out.println(e);
        }
    }

    public static void updateStudent(int id, String name) {
        try {
            Connection con = DriverManager.getConnection(url, username, password);
            String sql = "UPDATE students SET name = ? WHERE id = ?";
            PreparedStatement ps = con.prepareStatement(sql);

            ps.setString(1, name);
            ps.setInt(2, id);

            ps.executeUpdate();
            System.out.println("Student updated successfully.");

            con.close();
        } catch (Exception e) {
            System.out.println(e);
        }
    }

    public static void main(String[] args) {
        insertStudent(104, "Cognizant Modules", 21);
        updateStudent(104, "Cognizant Modules Completed");
    }
}