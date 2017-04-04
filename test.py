class PrimeFactor(object):
   
    #number で対象の数を、 max_count で返す因数の数を指定する
    def __init__(self, number, max_count):
        self.number = number
        self.max_count = max_count

    #クラスをジェネレータ化する
    def __iter__(self):
        count = 0
        for i in range(2, self.number):
            if self.number % i == 0:
                count += 1
                #指定された数だけ因数が返されたらイテレータ処理を終了するために StopIteration() 例外をあげる
                if count > self.max_count:
                    raise StopIteration()
                yield i
				
pf = PrimeFactor(number = 100, max_count = 5)

pf = iter(pf)

print(next(pf))

print(next(pf))