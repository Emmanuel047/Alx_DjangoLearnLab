#List all books in a library.
library_name = "Central Library"
library = Library.objects.get(name=library_name)
books_in_library = library.Book.all()

for book in books_in_library:
    print(book.title)


#Query all books by a specific author.
author_name = "J.K. Rowling"
books_by_author = Book.objects.filter(author__name=author_name)

for book in books_by_author:
    print(book.title)


#Retrieve the librarian for a library.
library_name = "Central Library"
library = Library.objects.get(name=library_name)
librarian = Librarian.objects.get(library=library)

print(librarian.name)
