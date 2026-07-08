package proxy;

public class ProxyTest {

    public static void main(String[] args) {

        Image image = new ProxyImage("Nature.jpg");

        System.out.println("Image Created");

        System.out.println();

        image.display();

        System.out.println();

        image.display();
    }
}