from django import template
from check_swear import SwearingCheck


register = template.Library()
sch = SwearingCheck() # create filter

@register.filter()
def censor(value: str):
    try:
        start_check = sch.predict(value)
        if start_check[0]:
            new_words = []
            list_word = value.split()
            for word in list_word:
                result_check = sch.predict_proba(word)
                if result_check[0] < 0.55:
                    new_words.append(word)
                else:
                    len_word = len(word)
                    change_word = word[:1]
                    for item in range(len_word):
                      change_word += '*'
                    new_words.append(change_word)
            total_result = ' '.join(new_words)
        else:
            total_result = value
    except TypeError:
        print('Ошибка типа данных!')
        total_result = value
    return total_result