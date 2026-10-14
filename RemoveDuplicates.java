import java.util.LinkedHashSet;
import java.util.Set;

public class RemoveDuplicates {

    /**
     * Removes duplicate characters from a given string/name while preserving character order.
     * Example: "programming" -> "progami"
     * Example: "John Doe" -> "John De"
     *
     * @param str Input string
     * @return String with duplicate characters removed
     */
    public static String removeDuplicateChars(String str) {
        if (str == null || str.isEmpty()) {
            return str;
        }

        StringBuilder sb = new StringBuilder();
        Set<Character> seen = new LinkedHashSet<>();

        for (char ch : str.toCharArray()) {
            if (seen.add(ch)) {
                sb.append(ch);
            }
        }

        return sb.toString();
    }

    /**
     * Removes duplicate words from a given string/name while preserving word order.
     * Example: "John John Doe" -> "John Doe"
     *
     * @param str Input string containing space-separated words
     * @return String with duplicate words removed
     */
    public static String removeDuplicateWords(String str) {
        if (str == null || str.trim().isEmpty()) {
            return str;
        }

        String[] words = str.split("\\s+");
        Set<String> seen = new LinkedHashSet<>();

        for (String word : words) {
            seen.add(word);
        }

        return String.join(" ", seen);
    }

    public static void main(String[] args) {
        // Test Case 1: Duplicate characters in a name
        String name = "programming";
        System.out.println("Original String: " + name);
        System.out.println("After removing duplicate characters: " + removeDuplicateChars(name));
        System.out.println();

        // Test Case 2: Full name with repeated characters
        String fullName = "Alexander Alexander";
        System.out.println("Original String: " + fullName);
        System.out.println("After removing duplicate characters: " + removeDuplicateChars(fullName));
        System.out.println("After removing duplicate words: " + removeDuplicateWords(fullName));
        System.out.println();

        // Test Case 3: Name with duplicate words
        String wordName = "John Doe John Doe";
        System.out.println("Original String: " + wordName);
        System.out.println("After removing duplicate words: " + removeDuplicateWords(wordName));
    }
}
