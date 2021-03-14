color = ["R", "G", "B", "K", "W", "Y"]
responseColors = ["W", "K"]
correct_response = "KKKK"

import itertools

class Game:
    def __init__(self):
        self.board = []
        self.codemaker = Codemaker()
        self.guesser = Guesser(self.board)

    def print_board(self):
        if self.board != []:
            print(self.board[-1])

    def playTurn(self,count):
        """
        Gets a guess (tuple - because itertools.product 
        returns a list of guesses that are tuples)
        from the guesser and then passes
        that guess to the user who gives a response (string)

        Both are then added to the board
        """
        self.print_board()
        guess = self.guesser.get_guess(count)
        response = self.codemaker.get_response(guess)
        row = Attempt(guess, response, count)
        self.board.append(row)
    
    def playGame(self):
        """
        Counts the number of turns.
        Calls playTurn(count).
        Checks if either the guesser or codemaker won
        """

        count = 0
        print("Choose a code made of 4 colors. Repetition is allowed")
        print("The colors are:\n R - Red\n G - Green\n B - Blue\n K - Black\n W - White\n Y - Yellow ")
        x = input("Press enter when ready!")
        del x

        while (True):
            count += 1
            self.playTurn(count)
            if(self.board[-1].response == correct_response):
                print("Guesser Won")
                break
            elif(len(self.board) == 10):
                print("CodeMaker Wins")
                break
class Attempt:
    def __init__(self, guess, response, turn):
        self.guess = guess
        self.response = response
        self.turn = turn
    def __str__(self):
        return f"{''.join(self.guess)} : {self.response} : {self.turn}"

class Codemaker:
    def get_response(self, guess):
        print("Type K for rigt color right location \nType W for right color wrong location")
        response = input(":")
        response = response.upper()
        sorted_response = ""

        """
        Sorts the user's response so that
        'K' is on the left and 'W' is on
        the right. 
        This is done so that when the guesser
        compares his pretend response to the
        user's response, all that's needed is an '=='
        """
        for letter in response:
            if letter == "K":
                sorted_response = "K" + sorted_response
            elif letter == "W":
                sorted_response = sorted_response + "W"
            else:
                print("Response is invalid\n")
                sorted_response = self.get_response(guess)

        return sorted_response

class Guesser:

    def __init__(self, board):
        self.board = board
        self.possible_codes = list(itertools.product(color,repeat=4))
    
    def pretend_response(self, guess, code):
        """
        Given the guess, this function pretends
        to be the user and gives an appropriate response.

        This is done so that when the guesser is given a response
        from the user, it can compare the real response to the responses
        of all possible codes and thereby delete codes that have different
        responses. Those codes with different responses can't be the code so
        it's thrown out. Quickly the length of the list of possible codes
        shrinks to 1.
        """

        code = list(code)
        guess = list(guess)
        response = ""

        for g_idx, g_color in enumerate(guess):
            if code[g_idx] == g_color:
                response = "K" + response
                code[g_idx] = ""
                guess[g_idx] = "-"

        for g_color in guess:
            for c_color in code:
                if g_color == c_color:
                    response = response + "W"
                    code[g_idx] = ""
        
        return "".join(response)

    def get_guess(self,turn):
        """
        On the first turn, the guesser guesses
        a basic guess 'RRGG'.
        On subsequent turns, the guesser compares
        the given response to possible responses (see above)
        to get a new guess.
        """

        if turn == 1:
            guess = ("R","R","G","G")
            self.possible_codes.remove(guess)

        else:
            self.possible_codes = [code for code in self.possible_codes
            if self.board[-1].response == self.pretend_response(self.board[-1].guess, code)]

            guess = self.possible_codes[0]
        
        print(" ".join(guess))
        return guess



game = Game()
game.playGame()
