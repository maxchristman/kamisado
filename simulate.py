from kamisado import GameConfig

winners = []
for _ in range(10000):
    gc = GameConfig('random', 'random', 'standard', 0)
    gc.start()
    winners.append(gc.game.winner.color)

black_winners = winners.count('black')
white_winners = winners.count('white')
print("Black won at a rate of", black_winners/(white_winners+black_winners))