public class Ex42 {
    public static void main(String[] args) {
		long base = Long.valueOf(args[0]);
		int exp = Integer.valueOf(args[1]);
		long result = bar(base, exp);
		System.out.println("" +  base + ", " + exp + " = " + result);
    }

	public static long foo(long base, int exp) {
		if (exp == 0) {
			return 1;
		}
		if (base == 0) {
			return 0;
		}
		if (exp > 0) {
			return base * foo(base, exp - 1);
		} else {
			return foo(base, exp + 1) / base;
		}
	}

	public static long bar(long base, int bar) {
		if (bar <= 0) {
			throw new IllegalArgumentException("exception");
		}
		if (bar == 1) {
			return base;
		}
		return base * ( 1 + bar(base, bar - 1));
	}
}
