public class SinCos {
	public static void main(String[] args) {
		for (double x = 0.0; x < 1.0; x += 0.05) {
			System.out.println("x " + x + ": " + Math.sin(x) + "," + sin(x));
		}
	}

	public static double sin(double x) {
		if (-0.005 < x && x < 0.005) {
			return x - (x * x * x) / 6;
		}
		return 2 * sin(x/2) * cos(x/2);
	}

	public static double cos(double x) {
		if (-0.005 < x && x < 0.005) {
			return 1 - (x * x) / 2;
		}
		return 1 - 2 * sin(x/2) * sin(x/2);
	}
}
