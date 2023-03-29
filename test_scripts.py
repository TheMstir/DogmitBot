import random

with open('dogmitGPTHumor.txt', 'r', encoding='utf-8') as file:
    lf = file.read().count('\n')
    dice = random.randint(1, lf)
    mess = file.read().split('\n')
    humor = mess[dice]
return humor