import random
from operator import itemgetter

dominos = [[i, j] for i in range(0, 7) for j in range(i, 7)]


def init():
    random.shuffle(dominos)
    player = dominos[:7]
    computer = dominos[7:14]
    stock = dominos[14:]
    snake = []
    return {
        "player": player,
        "computer": computer,
        "stock": stock,
        "snake": snake
    }


def find_max_double(pieces):
    doubles = [c for c in pieces if c[0] == c[1]]
    if len(doubles):
        return max(doubles)
    else:
        return False


def remove_piece(pieces, piece_remove):
    return [p for p in pieces if not p == piece_remove]


def update_game(game, player, value):
    game["snake"].append(max_double)
    game.update({player: remove_piece(game.get(player), max_double)})
    return game


def show(game, player):
    return f"""Stock pieces: {game["stock"]}
Computer pieces: {game["computer"]}
Player pieces: {game["player"]}
Domino snake: {game["snake"]}
Status: {player}
    """


def render_piece(pieces):
    return "\n".join([f"{i}:{p}" for i, p in enumerate(pieces, start=1)])


def render_snake(pieces):
    snake = [str(p) for p in pieces]
    if len(snake) > 3:
        snake = [snake[0], snake[-1]]
    return " ".join(snake)


def render_message_status(status, draw, win):
    if draw:
        return "The game is over. It's a draw!"
    elif win:
        if status == "player":
            winner = "you"
        else:
            winner = "the computer"
        return f"The game is over. {winner} won!"
    else:
        return "It's your turn to make a move. Enter your command." if status == "player" else "Computer is about to make a move. Press Enter to continue..."


def render_game(game, status, draw, win):
    data = {"stock_size": len(game["stock"]),
            "computer_size": len(game["computer"]),
            "snake": render_snake(game["snake"]),
            "player": render_piece(game["player"]),
            "status": render_message_status(status, draw, win)}
    return render(**data)


def render(**data):
    result = "=" * 70

    result += f"""

Stock size: {data["stock_size"]}
Computer pieces: {data["computer_size"]}

{data["snake"]}

Your pieces:
{data["player"]}

Status: {data["status"]}"""

    return result


def find_max(game):
    while True:
        double_player = find_max_double(game.get("player"))
        double_computer = find_max_double(game.get("computer"))
        if not (double_computer or double_player):
            game = init()
        elif not double_player:
            return ("computer", double_computer, game)
        elif not double_computer:
            return ("player", double_player, game)
        else:
            if double_player < double_computer:
                return ("computer", double_computer, game)
            else:
                return ("player", double_player, game)


def is_valid_id(game, player, id_text):
    return  0 <= abs(id_text) <= len(game[player])


def get_random_id(game):
    size = len(game["computer"])
    return random.randint(-size, size)

def is_valid_move(piece,snake,left=True):

    if left:
         snake_item = snake[0][0]
    else:
        snake_item = snake[-1][1]

    return snake_item in piece


def move_piece(piece,snake,left=True):
    if (left and not piece[1] == snake[0][0]) or (not (left  or   piece[0] == snake[-1][1])):
        return piece[::-1]
    else:
        return piece


def get_computer_piece(game):
    pieces = game["computer"]
    snake = game["snake"]
    count_value = [str(pieces).count(str(value)) for value in range(7)]
    scores = [[ piece , i, count_value[piece[0]] + count_value[piece[1]]]for i,piece in enumerate(pieces)]
    scores.sort(key=itemgetter(2))
    while len(scores) > 0:
        max_score = scores.pop()
        if is_valid_move(max_score[0],snake,True):
            return -max_score[1]
        elif is_valid_move(max_score[0],snake,False):
            return max_score[1]
    return 0




def select_piece(game, player):
    if player == "player":  # ask player to select a piece
        while True:
            try:
                # ask user choice

                id = int(input())  # id valid: number and less than number piece

                #select a piece
                #verify if piece is valid

                if id == 0:
                    return 0
                elif not is_valid_id(game,player,id ):
                    print("Invalid input. Please try again.")

                elif not is_valid_move(game[player][abs(id) - 1],game["snake"],id < 0):
                    print("Illegal move. Please try again.")

                else:
                    return id

            except ValueError as e:
                print("Invalid input. Please try again.")
    else:  # else select random piece in computer_piece
        input()
        return get_computer_piece(game)




def game_draw(pieces):
    first = pieces[0][0]
    last = pieces[-1][1]

    if first == last:
        count = sum([piece.count(first) for piece in pieces])
        return count == 8
    else:
        return False


# initialize game dominoes player computer
game = init()

(current_player, max_double, game) = find_max(game)

game = update_game(game, current_player, max_double)

current_player = "computer" if current_player == "player" else "player"

win = False
draw = False

print(render_game(game, current_player, draw, win))

while not (win or draw):  # loop game
    # select a piece

    id_domino_selected = select_piece(game, current_player)


    if id_domino_selected == 0 and len(game["stock"]) > 0:

        #remove piece from stock if id_domino == 0

            piece = game["stock"].pop()
            game[current_player].append(piece)

    else:
        # remove piece from game[player] and add piece to the snake
        piece = game[current_player].pop(abs(id_domino_selected) - 1)
        piece = move_piece(piece,game["snake"], id_domino_selected < 0)
        if id_domino_selected < 0:
            game["snake"].insert(0, piece)
        else:
            game["snake"].append(piece)

    win = len(game[current_player]) == 0  # current_player win
    draw = game_draw(game["snake"])  # game draw

    if not win:
        current_player = "computer" if current_player == "player" else "player"

    print(render_game(game, current_player, draw, win))
