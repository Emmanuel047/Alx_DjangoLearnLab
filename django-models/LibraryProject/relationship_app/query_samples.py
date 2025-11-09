#List all books in a library.
Library.Objects.get(name=library_name)
books_in_library = Library.Book.all()

#Query all books by a specific author.
Book.Objects.filter(author_name=author_name)

#Retrieve the librarian for a library.
librari = Librarian.Objects.get(name="librarian_name")