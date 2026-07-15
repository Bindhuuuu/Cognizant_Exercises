public class BuilderTest {

    public static void main(String[] args) {

        // Gaming Computer
        Computer gamingPC = new Computer.Builder("Intel i9", 32, 1000)
                .setGPU("NVIDIA RTX 4080")
                .setOperatingSystem("Windows 11")
                .build();

        // Office Computer
        Computer officePC = new Computer.Builder("Intel i5", 16, 512)
                .setOperatingSystem("Windows 10")
                .build();

        // Basic Computer
        Computer basicPC = new Computer.Builder("AMD Ryzen 3", 8, 256)
                .build();

        gamingPC.displayDetails();
        officePC.displayDetails();
        basicPC.displayDetails();
    }
}