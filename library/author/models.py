from django.db import models


class Author(models.Model):
    """
        This class represents an Author. \n
        Attributes:
        -----------
        param name: Describes name of the author
        type name: str max_length=20
        param surname: Describes last name of the author
        type surname: str max_length=20
        param patronymic: Describes middle name of the author
        type patronymic: str max_length=20
    """
    name = models.CharField(blank=True, max_length=20)
    surname = models.CharField(blank=True, max_length=20)
    patronymic = models.CharField(blank=True, max_length=20)
    books = models.ManyToManyField("book.Book", related_name='authors')
    id = models.AutoField(primary_key=True)

    def __str__(self):
        """
        Magic method is redefined to show all information about Author.
        :return: author id, author name, author surname, author patronymic
        """
        return f"\'id\': {self.pk}, \'name\': \'{self.name}\'," \
               f" \'surname\': \'{self.surname}\', \'patronymic\': \'{self.patronymic}\'"

    def __repr__(self):
        """
        This magic method is redefined to show class and id of Author object.
        :return: class, id
        """
        return f"Author(id={self.pk})"

    @staticmethod
    def get_by_id(author_id):
        """
        :param author_id: SERIAL: the id of a Author to be found in the DB
        :return: author object or None if a user with such ID does not exist
        """
        try:
            return Author.objects.get(pk=author_id)
        except Author.DoesNotExist:
            return None

    @staticmethod
    def validate_author_data(name, surname, patronymic):
        """
        Validates author data and returns errors if any.
        :param name: author name
        :param surname: author surname
        :param patronymic: author patronymic
        :return: error message string or None if valid
        """

        if not name or not surname or not patronymic:
            return "All fields are required."

        if len(name) > 20 or len(surname) > 20 or len(patronymic) > 20:
            return "Max length is 20 characters."

        return None

    @staticmethod
    def delete_by_id(author_id):
        """
        :param author_id: an id of a author to be deleted
        :type author_id: int
        :return: True if object existed in the db and was removed or False if it didn't exist
        """

        try:
            author = Author.objects.get(pk=author_id)
            if author.books.exists():
                return False
            author.delete()
            return True
        except Author.DoesNotExist:
            return False

    @staticmethod
    def create(name, surname, patronymic):
        """
        param name: Describes name of the author
        type name: str max_length=20
        param surname: Describes surname of the author
        type surname: str max_length=20
        param patronymic: Describes patronymic of the author
        type patronymic: str max_length=20
        :return: a new author object which is also written into the DB
        """

        error = Author.validate_author_data(name, surname, patronymic)
        if error:
            return None

        if Author.objects.filter(
                name=name,
                surname=surname,
                patronymic=patronymic
        ).exists():
            return None

        author = Author(name=name, surname=surname, patronymic=patronymic)
        author.save()
        return author

    def update(self, name=None, surname=None, patronymic=None):
        """
        Updates author in the database with the specified parameters.\n
        param name: Describes name of the author
        type name: str max_length=20
        param surname: Describes surname of the author
        type surname: str max_length=20
        param patronymic: Describes patronymic of the author
        type patronymic: str max_length=20
        :return: None
        """

        if name and len(name) <= 20:
            self.name = name
        if surname and len(surname) <= 20:
            self.surname = surname
        if patronymic and len(patronymic) <= 20:
            self.patronymic = patronymic
        self.save()

    @staticmethod
    def get_all():
        """
        returns data for json request with QuerySet of all authors
        """
        return Author.objects.all()
