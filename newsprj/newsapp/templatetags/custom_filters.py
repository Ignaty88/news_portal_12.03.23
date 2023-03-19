from django import template

register = template.Library()



BAD_WORDS = ['Редиски',
             'редиски',
             ]

# @register.filter()
# def censor(NEW_WORD):
#
#     for word in BAD_WORDS:
#         if word.title() in BAD_WORDS:
#             repl_word = word[0] + (len(word) - 1) * '*'
#             NEW_WORD = NEW_WORD.replace(word, repl_word)
#
#         return NEW_WORD
@register.filter()
def censor(text: str):
    text_list = text.split()
    for i in range(len(text_list)):
        for c in BAD_WORDS:
            if text_list[i].find(c) >= 0:
                repl_word = c[0] + (len(c) - 1) * '*'
                text_list[i] = text_list[i].replace(c, repl_word)
    return ' '.join(text_list)