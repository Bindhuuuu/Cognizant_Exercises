class Car {

    String make;
    String model;
    int year;

    void displayDetails() {
        System.out.println("Make : " + make);
        System.out.println("Model: " + model);
        System.out.println("Year : " + year);
        System.out.println();
    }

    public static void main(String[] args) {

        Car car1 = new Car();
        car1.make = "Toyota";
        car1.model = "Fortuner";
        car1.year = 2024;

        Car car2 = new Car();
        car2.make = "Hyundai";
        car2.model = "Creta";
        car2.year = 2023;

        car1.displayDetails();
        car2.displayDetails();
    }
}