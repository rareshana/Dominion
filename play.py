import main

game = main.Game(2) #２人プレイの設定

printtest = [print(game.field.treasurepile[i]) for i in range(3)]
printtest2 = [print(len(game.field.treasurepile[i])) for i in range(3)]

printtest = [print(game.field.victorypile[i]) for i in range(3)]
printtest2 = [print(len(game.field.victorypile[i])) for i in range(3)]