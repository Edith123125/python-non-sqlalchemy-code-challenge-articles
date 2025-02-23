class Article:
    all = []  # Stores all articles

    def __init__(self, author, magazine, title):# initialization
        if not isinstance(author, Author):
            raise TypeError("Author must be an instance of the Author class")
        if not isinstance(magazine, Magazine):
            raise TypeError("Magazine must be an instance of the Magazine class")
        if not isinstance(title, str) or not (5 <= len(title) <= 50):#checks the tittle is a string and its length is 5-50characters.
            raise ValueError("Title must be a string between 5 and 50 characters")

        self._author = author
        self._magazine = magazine
        self._title = title
        Article.all.append(self)

    @property
    def title(self): # immutability check
        return self._title  

    @property
    def author(self):
        return self._author

    @author.setter
    def author(self, new_author):
        if not isinstance(new_author, Author):
            raise TypeError("New author must be an instance of the Author class")
        self._author = new_author # association where author is linked to an article and can be changed.

    @property
    def magazine(self):
        return self._magazine

    @magazine.setter
    def magazine(self, new_magazine):
        if not isinstance(new_magazine, Magazine):
            raise TypeError("New magazine must be an instance of the Magazine class")
        self._magazine = new_magazine # association where each article belongs to one magazine and can be updated.


class Author:
    def __init__(self, name):
        if not isinstance(name, str) or not name.strip():
            raise ValueError("Name must be a non-empty string")
        self._name = name

    @property
    def name(self):
        """Name is immutable"""
        return self._name  

    def articles(self): # Returns all articles written by this author.
                        # aggregation...deleting the author does not remove their articles.
        return [article for article in Article.all if article.author == self]

    def magazines(self): # returns the magazines the author has contributed to.
        return list(set(article.magazine for article in self.articles()))

    def add_article(self, magazine, title): # a new article for the author is created  
        return Article(self, magazine, title)

    def topic_areas(self): # this gives a magazine categories that has been contributed by the author.
        categories = list(set(mag.category for mag in self.magazines()))
        return categories if categories else None  # if no articles exist we get None.


class Magazine:
    all = []  # all magazines are stored here.

    def __init__(self, name, category):
        if not isinstance(name, str) or not (2 <= len(name) <= 16):
            raise ValueError("Name must be a string between 2 and 16 characters")
        if not isinstance(category, str) or not category.strip():  # category validation where the category must be non-empty string.
                                                                    # strip prevents  non-string values like numbers and None and no blabkspaces. 
            raise ValueError("Category must be a non-empty string")

        self._name = name
        self._category = category
        Magazine.all.append(self)

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, new_name):
        if isinstance(new_name, str) and 2 <= len(new_name) <= 16:
            self._name = new_name
        else:
            raise ValueError("New name must be a string between 2 and 16 characters")

    @property
    def category(self):
        return self._category

    @category.setter
    def category(self, new_category):
        if isinstance(new_category, str) and new_category.strip():
            self._category = new_category
        else:
            raise ValueError("New category must be a non-empty string")

    def articles(self): # returns a list of articles in the magazine.
        return [article for article in Article.all if article.magazine == self]

    def contributors(self): # returns a list of contributors in the magazine.
        return list(set(article.author for article in self.articles()))

    def article_titles(self): # returns a list of article tittle. 
        titles = [article.title for article in self.articles()]
        return titles if titles else None  

    def contributing_authors(self): # here we get authors who have written more than two articles in the magazine.
        author_counts = {}
        for article in self.articles():
            author_counts[article.author] = author_counts.get(article.author, 0) + 1
        top_authors = [author for author, count in author_counts.items() if count > 2]
        return top_authors if top_authors else None  

    @classmethod
    def top_publisher(cls): 
        if not cls.all: # returs the magazine which has most articles.
            return None
        return max(cls.all, key=lambda mag: len(mag.articles()), default=None) # with max now we get the top publisher. 
