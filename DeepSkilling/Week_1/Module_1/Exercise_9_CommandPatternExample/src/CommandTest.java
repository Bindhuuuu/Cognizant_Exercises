public class CommandTest {

    public static void main(String[] args) {

        Light light = new Light();

        Command lightOn = new LightOnCommand(light);
        Command lightOff = new LightOffCommand(light);

        RemoteControl remote = new RemoteControl();

        System.out.println("Turning ON the Light");
        remote.setCommand(lightOn);
        remote.pressButton();

        System.out.println();

        System.out.println("Turning OFF the Light");
        remote.setCommand(lightOff);
        remote.pressButton();

    }

}