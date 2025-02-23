import pytest

from classes.many_to_many import Article
from classes.many_to_many import Magazine
from classes.many_to_many import Author


class TestMagazine:
    """Magazine in many_to_many.py"""

    def test_has_name(self):
        """Magazine is initialized with a name"""
        magazine_1 = Magazine("Vogue", "Fashion")
        magazine_2 = Magazine("AD", "Architecture")

        assert magazine_1.name == "Vogue"
        assert magazine_2.name == "AD"

    def test_name_is_valid(self):
        """magazine name is a valid string between 2 and 16 characters"""
        magazine_1 = Magazine("Vogue", "Fashion")
        assert isinstance(magazine_1.name, str)
        assert 2 <= len(magazine_1.name) <= 16

        with pytest.raises(ValueError):
            magazine_1.name = "A"
        with pytest.raises(ValueError):
            magazine_1.name = "New Yorker Plus X"

    def test_category_is_valid(self):
        """magazine category is a valid string and not empty"""
        magazine_1 = Magazine("Vogue", "Fashion")
        assert isinstance(magazine_1.category, str)
        assert magazine_1.category != ""

        with pytest.raises(ValueError):
            magazine_1.category = ""

    def test_has_many_articles(self):
        """magazine has many articles"""
        author_1 = Author("Carry Bradshaw")
        magazine_1 = Magazine("Vogue", "Fashion")
        article_1 = Article(author_1, magazine_1, "How to wear a tutu with style")
        article_2 = Article(author_1, magazine_1, "Dating life in NYC")

        assert len(magazine_1.articles()) == 2
        assert article_1 in magazine_1.articles()
        assert article_2 in magazine_1.articles()

    def test_articles_of_type_articles(self):
        """magazine articles are of type Article"""
        author_1 = Author("Carry Bradshaw")
        magazine_1 = Magazine("Vogue", "Fashion")
        Article(author_1, magazine_1, "How to wear a tutu with style")
        assert isinstance(magazine_1.articles()[0], Article)

    def test_contributors_are_unique(self):
        """magazine contributors are unique and of type Author"""
        author_1 = Author("Carry Bradshaw")
        author_2 = Author("Nathaniel Hawthorne")
        magazine_1 = Magazine("Vogue", "Fashion")
        Article(author_1, magazine_1, "How to wear a tutu with style")
        Article(author_1, magazine_1, "How to be single and happy")
        Article(author_2, magazine_1, "Dating life in NYC")

        contributors = magazine_1.contributors()
        assert len(set(contributors)) == len(contributors)
        assert all(isinstance(author, Author) for author in contributors)

    def test_article_titles(self):
        """returns list of article titles written for that magazine"""
        author_1 = Author("Carry Bradshaw")
        magazine_1 = Magazine("Vogue", "Fashion")
        magazine_2 = Magazine("AD", "Architecture")
        Article(author_1, magazine_1, "How to wear a tutu with style")
        Article(author_1, magazine_2, "2023 Eccentric Design Trends")

        assert magazine_1.article_titles() == ["How to wear a tutu with style"]
        assert magazine_2.article_titles() == ["2023 Eccentric Design Trends"]

    def test_contributing_authors(self):
        """returns authors who have written more than 2 articles for the magazine"""
        author_1 = Author("Carry Bradshaw")
        author_2 = Author("Nathaniel Hawthorne")
        magazine_1 = Magazine("Vogue", "Fashion")
        Article(author_1, magazine_1, "How to wear a tutu with style")
        Article(author_1, magazine_1, "How to be single and happy")
        Article(author_1, magazine_1, "Dating life in NYC")
        Article(author_2, magazine_1, "Carrara Marble is so 2020")

        assert author_1 in magazine_1.contributing_authors()
        assert author_2 not in magazine_1.contributing_authors()

    def test_top_publisher(self):
        """returns the magazine with the most articles"""
        Magazine.all = []
        Article.all = []
        assert Magazine.top_publisher() is None

        author_1 = Author("Carry Bradshaw")
        magazine_1 = Magazine("Vogue", "Fashion")
        magazine_2 = Magazine("AD", "Architecture")

        Article(author_1, magazine_1, "How to wear a tutu with style")
        Article(author_1, magazine_1, "Dating life in NYC")
        Article(author_1, magazine_1, "How to be single and happy")
        Article(author_1, magazine_2, "2023 Eccentric Design Trends")

        assert Magazine.top_publisher() == magazine_1
        assert isinstance(Magazine.top_publisher(), Magazine)
