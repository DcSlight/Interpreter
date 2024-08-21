"""Explain the term "lazy evaluation" in the context of the following program: """

"""
הקשר בין Lazy evaluation לבין generators הוא שLazy evaluation 
זוהי אסטרטגיה שבה אובייקטים מסוימים אינם מיוצרים עד שהם נדרשים,
 גישה זו משפיעה הן על ניהול הזיכרון 
 והן על זמן ריצת הפונקציות. Generators הם תומכים בגישת הLazy evaluation בכך 
 שהם מתנהגים כמו פונקציות שמחזירות ערכים,
  אבל הם זוכרים את המצב הפנימי שלהם ולכן יודעים להחזיר כל פעם את האלמנט הבא שברצף.
  בתרגיל זה ב Eager Evaluation כל הערכים חוזרים בתחילת הקוד ורק לאחר מכן נעשה שימוש בהם
  לעומת זאת, ב Lazy Evaluation עד שלא צריך את הערך הבא הוא לא מחושב
"""

def generate_values():
    print('Generating values...')
    yield 1
    yield 2
    yield 3


def square(x):
    print(f'Squaring {x}')
    return x * x


print('Eager evaluation:')
values = list(generate_values())
squared_values = [square(x) for x in values]
print(squared_values)

print('\nLazy evaluation:')
squared_values = [square(x) for x in generate_values()]
print(squared_values)
