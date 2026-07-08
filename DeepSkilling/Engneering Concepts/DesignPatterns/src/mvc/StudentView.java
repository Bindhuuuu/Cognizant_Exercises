package mvc;

public class StudentView {

    public void displayStudentDetails(Student student) {

        System.out.println("Student Details");
        System.out.println("----------------");
        System.out.println("Name : " + student.getName());
        System.out.println("ID : " + student.getId());
        System.out.println("Grade : " + student.getGrade());

    }

}