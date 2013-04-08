import java.io.File;


public class TreePrintFolder {
	static String[] pathchars = new String[] {
		"+","|","-","\\",
	};
	
	public static void main(String[] args) {
		File file = new File(args[1]);
		treePrint(file);
	}
	
	private static void treePrint(File file) {
		treePrint("", file);
	}
	
	/*
	 *  root
	 *  +---a
	 *  |	+---a1
	 *  |	|	+---a11
	 *  |	|	+---a12
	 *  |	|	\---a13
	 *  |	+---a2
	 *  |	\---a3
	 *  +---b
	 *  \---c
	 * 
	 */
	private static void treePrint(String prefix, File file) {
		
	}
}
