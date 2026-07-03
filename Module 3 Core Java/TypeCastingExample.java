public class TypeCastingExample {
    public static void main(String[] args) {
        double d = 25.75;
        int i = (int) d;
        System.out.println("Double value: " + d);
        System.out.println("Double to Int: " + i);

        int num = 100;
        double d2 = (double) num;
        System.out.println("Int value: " + num);
        System.out.println("Int to Double: " + d2);
    }
}