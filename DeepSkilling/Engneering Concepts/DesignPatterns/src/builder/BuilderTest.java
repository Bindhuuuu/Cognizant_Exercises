package builder;

public class BuilderTest {

    public static void main(String[] args) {

        Computer computer = new Computer.Builder()
                .setCPU("Intel i7")
                .setRAM("16 GB")
                .setStorage("512 GB SSD")
                .setGraphicsCard("NVIDIA RTX 4060")
                .setOperatingSystem("Windows 11")
                .build();

        computer.display();
    }
}