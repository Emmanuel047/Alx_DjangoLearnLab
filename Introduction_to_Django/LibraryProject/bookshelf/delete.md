from books.models import Book
    book = Book.objects.get(pk=1)
    book.delete()

#(1, {'bookshelf.Book': 1})