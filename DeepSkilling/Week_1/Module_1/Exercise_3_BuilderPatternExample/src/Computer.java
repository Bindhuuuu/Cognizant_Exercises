public class Computer {
    private String cpu;
    private int ram;
    private int storage;
    private String gpu;
    private String operatingSystem;
    // Private constructor
    private Computer(Builder builder) {
        this.cpu = builder.cpu;
        this.ram = builder.ram;
        this.storage = builder.storage;
        this.gpu = builder.gpu;
        this.operatingSystem = builder.operatingSystem;
    }
    public void displayDetails() {
        System.out.println("Computer Configuration");
        System.out.println("----------------------");
        System.out.println("CPU: " + cpu);
        System.out.println("RAM: " + ram + " GB");
        System.out.println("Storage: " + storage + " GB");
        System.out.println("GPU: " + gpu);
        System.out.println("Operating System: " + operatingSystem);
        System.out.println();
    }
    // Static Nested Builder Class
    public static class Builder {
        private String cpu;
        private int ram;
        private int storage;
        private String gpu = "Not Included";
        private String operatingSystem = "No OS";
        public Builder(String cpu, int ram, int storage) {
            this.cpu = cpu;
            this.ram = ram;
            this.storage = storage;
        }
        public Builder setGPU(String gpu) {
            this.gpu = gpu;
            return this;
        }
        public Builder setOperatingSystem(String operatingSystem) {
            this.operatingSystem = operatingSystem;
            return this;
        }
        public Computer build() {
            return new Computer(this);
        }
    }
}