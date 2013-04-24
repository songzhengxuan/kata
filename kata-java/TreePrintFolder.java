import java.io.File;

public class TreePrintFolder {
    static char[] sPathChars = { '|', '+', '-', '\\', };

    public static void main(String[] args) {
        File file = new File(args[0]);
        treePrint(file);
    }

    private static void treePrint(File path) {
        treePrint("", path);
    }

    private static void treePrint(String prefix, File path) {
        if (path == null) {
            return;
        }
        System.out.println(prefix + path.getName());
        File[] children = path.listFiles();
        if (children != null && children.length > 0) {
            String newPrefix = prefix;
            if (prefix.length() >= 4) {
                String tail = prefix.substring(prefix.length() - 4);
                if ("\\---".equals(tail)) {
                    newPrefix = prefix.substring(0, prefix.length() - 4) + "    ";
                } else if ("|---".equals(tail)) {
                    newPrefix = prefix.substring(0, prefix.length() - 4) + "|   ";
                }
            }
            final String newPrefixForMiddleChild = newPrefix + "|---";
            for (int i = 0; i < children.length - 1; ++i) {
                treePrint(newPrefixForMiddleChild, children[i]);
            }
            final String newPrefixForLastChild = newPrefix + "\\---";
            treePrint(newPrefixForLastChild, children[children.length - 1]);
        }
    }

    private static void printLine(String line) {
        System.out.println(line);
    }

}
