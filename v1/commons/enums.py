from enum import Enum


class WordPhrase(Enum):
    grammar = 'grammar'
    semantic_expression = 'semantic_expression'

    @classmethod
    def choices(cls):
        return (
            (key.value, key.name)
            for key in cls
        )


class SourceType(Enum):
    newspaper = 'newspaper'
    official_text = 'official_text'
    journal = 'journal'
    internet_info = "internet_info"
    book = 'book'
    article = 'article'
    other = 'other'

    @classmethod
    def choices(cls):
        return (
            (key.value, key.name)
            for key in cls
        )


class UserRole(Enum):
    admin = 'admin'
    customer = 'customer'

    @classmethod
    def choices(cls):
        return (
            (key.value, key.name)
            for key in cls
        )


class AuthorType(Enum):
    man = 'man'
    woman = 'woman'

    @classmethod
    def choices(cls):
        return (
            (key.value, key.name)
            for key in cls
        )
