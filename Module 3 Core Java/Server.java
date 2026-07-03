import java.io.DataInputStream;
import java.io.DataOutputStream;
import java.net.ServerSocket;
import java.net.Socket;

public class Server {
    public static void main(String[] args) {
        try {
            ServerSocket server = new ServerSocket(5000);
            System.out.println("Server is waiting for client...");

            Socket socket = server.accept();
            System.out.println("Client Connected.");

            DataInputStream dis = new DataInputStream(socket.getInputStream());
            DataOutputStream dos = new DataOutputStream(socket.getOutputStream());

            String message = dis.readUTF();
            System.out.println("Client: " + message);

            dos.writeUTF("Hello Client!");

            dis.close();
            dos.close();
            socket.close();
            server.close();
        } catch (Exception e) {
            System.out.println(e);
        }
    }
}