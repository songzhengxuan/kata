package tutorial;
import java.math.BigDecimal;


public class BigDecBug {
	public static void main(String [] args) {
		BigDecimal a = new BigDecimal("0.1");
		BigDecimal b = a.add(new BigDecimal(0.1));
		String dblString = Double.toString(0.1);
		System.out.println(b);
		System.out.println(a);
		System.out.println(dblString);
	}

}
