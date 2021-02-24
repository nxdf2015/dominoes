# Write your code here
import random

dominos = [ [i,j] for i in range(0,7) for j in range(i, 7)]



def init():
    random.shuffle(dominos)
    player = dominos[:7]
    computer = dominos[7:14]
    stock = dominos[14:]
    snake = []
    return {
        "player" : player,
        "computer" : computer,
        "stock" : stock,
        "snake" : snake
    }

def find_max_double(pieces):
    doubles = [ c for c in pieces if c[0] == c[1]]
    if len(doubles):
        return max(doubles)
    else:
        return False

def remove_piece(pieces,piece_remove):
    return [p for p in pieces if not p == piece_remove]



def update_game(game,player,value):
    game["snake"].append(max_double)
    game.update({ player : remove_piece(game.get(player), max_double)})
    return game

def show(game,player):
    return f"""Stock pieces: {game["stock"]}
Computer pieces: {game["computer"]}
Player pieces: {game["player"]}
Domino snake: {game["snake"]}
Status: {player}

    """

def find_max(game):
    while True:
        double_player = find_max_double(game.get("player"))
        double_computer = find_max_double(game.get("computer"))
        if not(double_computer or double_player):
            game=init()
        elif not double_player:
            return ("computer",double_computer,game)
        elif not double_computer:
            return ("player", double_player, game)
        else:
            if double_player < double_computer:
                return ("computer",double_computer,game)
            else:
                 return ("player",double_player, game)




game = init()



(current_player, max_double, game) = find_max(game)


game = update_game(game, current_player, max_double)

current_player = "computer" if current_player == "player" else "player"

print(show(game,current_player))

