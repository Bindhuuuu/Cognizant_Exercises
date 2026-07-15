public class Forecast {

    // Recursive method to calculate future value
    public static double calculateFutureValue(double presentValue, double growthRate, int years) {

        // Base case
        if (years == 0) {
            return presentValue;
        }

        // Recursive case
        return calculateFutureValue(presentValue, growthRate, years - 1) * (1 + growthRate);
    }
}