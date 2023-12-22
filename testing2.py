dict_1 = {1:'a',
          'b':2
          }

for i in dict_1:
    print(i)


class Test():
    def __init__(self):
        self.test = 'abc'

testing = Test()

dict_2 = {'test':testing.test}
print('adicionado no dict ', testing.test)

testing.test = 'bcd'
print('mudando a var ', testing.test)
print(dict_2)

for chave,valor in dict_2.items():
    globals()[chave] = valor

print('chamando no globals ', test)
