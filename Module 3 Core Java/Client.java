import java.io.DataInputStream;
import java.io.DataOutputStream;
import java.net.Socket;

public class Client {
    public static void main(String[] args) {
        try {
            Socket socket = new Socket("localhost", 5000);

            DataInputStream dis = new DataInputStream(socket.getInputStream());
            DataOutputStream dos = new DataOutputStream(socket.getOutputStream());

            dos.writeUTF("Hello Server!");

            String message = dis.readUTF();
            System.out.println("Server: " + message);

            dis.close();
            dos.close();
            socket.close();
        } catch (Exception e) {
            System.out.println(e);
        }
    }
}