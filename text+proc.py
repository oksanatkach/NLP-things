import re


def count_regex(s):
    two_d = r'[0-9]{2}'
    four_d = r'[0-9]{4}'
    months = r'January|February|March|April|May|June|July|August|September|October|November|December'
    short_months = r'Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec'
    ws = r'rst|nd|th (of )?'

    ar_a = r'( a |A |"a )'
    ar_an = r'( an |An |"an )'
    ar_the = r'( the |The |"the )'
    dates = '(' +\
            two_d + '/' + two_d + '/' + four_d\
            + ')|(' +\
            two_d + '/' + two_d + '/' + two_d\
            + ')|(' +\
            two_d + '(' + ws + '| )' + '(' + months + '|' + short_months + ')(,)? ' + '(' + four_d + '|' + two_d + ')'\
            + ')|(' +\
            '(' + months + '|' + short_months + ') ' + two_d + '(' + ws + '| ) ' + four_d\
            + ')|(' + \
            '(' + months + '|' + short_months + ') ' + two_d + '(' + ws + '| )' + four_d + ')'

    return len(re.findall(ar_a, s)), len(re.findall(ar_an, s)), len(re.findall(ar_the, s)), len(re.findall(dates, s))


inp = open('input_text_proc.txt', 'r').read().strip().split('\n')[1:]
outp = open('output_text_proc.txt', 'r').read().strip().split('\n')

# counts = count_regex(s)
# for num in counts:
#     print num

digits = r'[0-9]{1,4}'
months = r'January|February|March|April|May|June|July|August|September|October|November|December'
short_months = r'Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec'
ws = r'rst|nd|th (of )?'
dates = '(' + \
        digits + '/' + digits + '/' + digits \
        + ')|(' + \
        digits + '/' + digits + '/' + digits \
        + ')|(' + \
        digits + '(' + ws + '| |, )' + '(' + months + '|' + short_months + ')(,)? ' + digits \
        + ')|(' + \
        '(' + months + '|' + short_months + ') ' + digits + '(' + ws + '| |, ) ' + digits \
        + ')|(' + \
        '(' + months + '|' + short_months + ') ' + digits + '(' + ws + '| |, )' + digits + ')'

s = '20th of March, 1999'

# print re.search('(' + months + '|' + short_months + ') ' + two_d + '(' + ws + '| |, )' + four_d, s).group()
print re.search(dates, s).group()
