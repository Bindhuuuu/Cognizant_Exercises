public class MVCTest {

    public static void main(String[] args) {

        Student student = new Student(
                "Ram Tej",
                "AP23002023",
                "A");

        StudentView view = new StudentView();

        StudentController controller =
                new StudentController(student, view);

        System.out.println("Initial Student Details");
        controller.updateView();

        System.out.println();

        controller.setStudentName("Rahul");
        controller.setStudentGrade("A+");

        System.out.println("Updated Student Details");
        controller.updateView();

    }

}