import java.lang.reflect.Method;

class Student {
    public void display() {
        System.out.println("Hello from Reflection!");
    }
}

public class ReflectionExample {
    public static void main(String[] args) {
        try {
            Class<?> cls = Class.forName("Student");

            System.out.println("Class Name: " + cls.getName());

            Method[] methods = cls.getDeclaredMethods();
            System.out.println("Methods:");

            for (Method method : methods) {
                System.out.println(method.getName());
            }

            Object obj = cls.getDeclaredConstructor().newInstance();
            Method method = cls.getMethod("display");
            method.invoke(obj);

        } catch (Exception e) {
            System.out.println(e);
        }
    }
}