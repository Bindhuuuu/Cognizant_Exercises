package library;

public class LibrarySearch {

    // Linear Search
    public static Book linearSearch(Book[] books, String title) {

        for (Book book : books) {

            if (book.getTitle().equalsIgnoreCase(title))
                return book;

        }

        return null;
    }

    // Binary Search
    public static Book binarySearch(Book[] books, String title) {

        int left = 0;
        int right = books.length - 1;

        while (left <= right) {

            int mid = (left + right) / 2;

            int result = books[mid].getTitle().compareToIgnoreCase(title);

            if (result == 0)
                return books[mid];

            else if (result < 0)
                left = mid + 1;

            else
                right = mid - 1;
        }

        return null;
    }

}