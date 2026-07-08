package decorator;

public class SlackNotifierDecorator extends NotifierDecorator {

    public SlackNotifierDecorator(Notifier notifier) {

        super(notifier);

    }

    @Override
    public void send(String message) {

        notifier.send(message);

        System.out.println("Slack Notification: " + message);

    }

}