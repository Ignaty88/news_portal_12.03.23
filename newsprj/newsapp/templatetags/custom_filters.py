from django import template

register = template.Library()

# @register.filter()
# def censor(value):
#     bad_words = ['Редиски']
#
#     if not isinstance(value, str):
#         raise TypeError(f"Недопустимое значение '{type(value)}' Надо ввести строку ")
#
#     for word in value.split():
#         if word.lower() in bad_words:
#             value = value.replace(word, f"{word[0]}{'*' * (len(word)-1)}")
#         return value


@register.filter()
def censor(NEW_WORD):
    BAD_WORDS = ['Редиски']

    for word in BAD_WORDS:
        if word in BAD_WORDS:
            repl_word = word[0] + (len(word) - 1) * '*'
            NEW_WORD = NEW_WORD.replace(word, repl_word)

        return NEW_WORD
