package builder;

public class Computer {

    private String cpu;
    private String ram;
    private String storage;
    private String graphicsCard;
    private String operatingSystem;

    // Private constructor
    private Computer(Builder builder) {
        this.cpu = builder.cpu;
        this.ram = builder.ram;
        this.storage = builder.storage;
        this.graphicsCard = builder.graphicsCard;
        this.operatingSystem = builder.operatingSystem;
    }

    // Display method
    public void display() {
        System.out.println("Computer Configuration");
        System.out.println("----------------------");
        System.out.println("CPU : " + cpu);
        System.out.println("RAM : " + ram);
        System.out.println("Storage : " + storage);
        System.out.println("Graphics Card : " + graphicsCard);
        System.out.println("Operating System : " + operatingSystem);
    }

    // Static Builder class
    public static class Builder {

        private String cpu;
        private String ram;
        private String storage;
        private String graphicsCard;
        private String operatingSystem;

        public Builder setCPU(String cpu) {
            this.cpu = cpu;
            return this;
        }

        public Builder setRAM(String ram) {
            this.ram = ram;
            return this;
        }

        public Builder setStorage(String storage) {
            this.storage = storage;
            return this;
        }

        public Builder setGraphicsCard(String graphicsCard) {
            this.graphicsCard = graphicsCard;
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