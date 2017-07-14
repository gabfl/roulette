
import random
import time
import locale
import sys

import argparse
from tabulate import tabulate

from .vars.numbers import *
from .vars.bets import *
from .utils import config

# Parse arguments
parser = argparse.ArgumentParser()
parser.add_argument("-t", "--type", type=str, help="Roulette type", choices=['french', 'american'], default='french')
parser.add_argument("-b", "--bank", type=int, help="Set bank amount")
parser.add_argument("-i", "--minimum_bet", type=int, help="Minimum bet allowed", default=1)
parser.add_argument("-x", "--maximum_bet", type=int, help="Maximum bet allowed", default=10000)
args = parser.parse_args()

# Currency locale
locale.setlocale(locale.LC_ALL, '')

# Get config
conf = config.getConfig()

# Override bank if necessary
if args.bank:
    config.update('bank', args.bank)

# Vars
currentBank = float(conf['bank'])  # Set the default bank
withColors = addColors(french if args.type == 'french' else american)  # Create the roulette wheel with colors


def showBank():
    """
        Show current bank
    """

    global currentBank

    print('* Current bank: %s' % (amountToCurrency(currentBank)))


def updateBank(amount):
    """
        Update the bank with losses or winnings
    """

    global currentBank

    # Set vars
    currentBank = currentBank + amount
    word = 'loss' if amount < 0 else 'winnings'

    # Update bank in config
    config.update('bank', currentBank)

    print('* After accounting for your %s of %s, your bank is now %s' % (word, amountToCurrency(amount), amountToCurrency(currentBank)))


def checkBankStatus():
    """
        Check if the user has money in the bank
    """

    global currentBank

    if currentBank <= 0:
        print()
        print('You are out of money!')
        print('You can add money to your bank with the flag `--bank [amount]`')
        print()
        sys.exit()


def amountToCurrency(amount):
    """
        Shows an amount in the user currency locale or default to `$`
    """

    try:
        return locale.currency(amount, grouping=True)
    except ValueError:  # If the locale does not support currency formatting
        return '$' + str(round(amount, 2))


def getMaxPossibleBet():
    """
        Will return the maximum bet allowed for this game
    """

    global currentBank

    if currentBank < args.maximum_bet:
        return currentBank

    return args.maximum_bet


def wheel():
    """
        Will define the winning number and return a list with the complete game

        Example:
        [(2, 'black'), (25, 'red'), ...... , (10, 'black'), (5, 'red'), (24, 'black'), (16, 'red'), (33, 'black')]
            ↑ Ball initial hit         ↑ looping thru the wheel                                       ↑ winning
    """

    global withColors

    start = random.randint(1, len(withColors) - 1)
    runs = random.randint(2, 5)
    winner = random.randint(1, len(withColors))

    wheel = []
    for run in range(0, runs):
        if run == 0:  # First turn
            thisloop = withColors[start:]
        elif run == runs - 1:  # Last turn
            thisloop = withColors[:winner]
        else:  # Intermediate
            thisloop = withColors

        wheel = wheel + thisloop

    return wheel


def game():
    """
        Spin the wheel, show the ball position and return the winning position

        Return example: `(10, 'black')`
    """

    # Get random wheel
    w = wheel()

    seq = ('/', '-', '\\', '_')
    for i, item in enumerate(w):
        numer, color = item
        print('   %s  %s  %s' % (str(seq[i % 4]), getColorIcon(color), str(numer)), end='\r')
        sleep(i, len(w))

    # Hide game
    print(' ' * 20, end='\r')

    # Get winning position
    winning = w[-1]

    return winning


def getOutcome(betAmount, bet, specificChoice=None):
    """
        Initiate a game with a bet amount and a bet type and calculate the outcome
    """

    # Spin the wheel and get the winning position
    winning = game()

    number, color = winning
    print()
    print('* Winning position: %s  %s' % (getColorIcon(color), str(number)))
    # print()

    if (specificChoice and number == specificChoice) or (specificChoice is None and number in bet['winningSpaces']):
        if isUnicodeSupported():
            print('  ... you won!  ' + u"\U0001F4B0" '  ' * 3)
        else:
            print('  ... you won!')

        a, b = bet['payout']
        updateBank(betAmount * a / b)
    else:
        print('  ... you lost!')

        # Update bank
        updateBank(betAmount * -1)


def getColorIcon(color):
    """
        If unicode is supported, it will return an icon for the number color.
        If not, will return a letter (B, R or G)
    """

    if isUnicodeSupported():
        if color == 'red':
            return u"\U0001F534"
        elif color == 'black':
            return u"\u2B24"
        elif color == 'green':
            return u"\U0001F49A"

    return color[:1].upper()


def sleep(iteration, total):
    """
        While displaying each number and color, will sleep less and less to simulate the wheel slowing down
        at the end of the game
    """

    # Calcule percentage of wheel rotation
    pct = iteration / total * 100

    if iteration == total - 2:  # 2nd to last one
        s = 0.4
    elif iteration == total - 1:  # Last one
        s = 1
    elif pct < 50:
        s = 0.05
    elif pct < 70:
        s = 0.09
    elif pct < 85:
        s = 0.1
    elif pct < 90:
        s = 0.15
    elif pct < 95:
        s = 0.18
    elif pct < 99:
        s = 0.2
    else:  # Default
        s = 0.25

    time.sleep(s)


def isUnicodeSupported():
    """
        Returns `True` if stdout supports unicode
    """

    return sys.stdout.encoding.lower().startswith('utf-')


def betsTable():
    """
        Prints a human readable bets table
    """

    global bets

    table = []
    for key, bet in enumerate(bets):
        a, b = bet['payout']
        table.append([
            key + 1,
            bet['name'],
            str(a) + ' to ' + str(b),
        ])

    # Show bets table
    print (tabulate(table, headers=['#', 'Bet', 'Payout']))


def isBetTypeValid(betNumber):
    """
        Check if the bet chosen is valid
    """

    global bets

    try:
        # Will trigger an error if the number is invalid
        getBet(betNumber)

        return True
    except ValueError:  # Number out of range
        return False
    except IndexError:  # Not a number
        return False


def getBet(betNumber):
    """
        Returns a bet dict for a specific bet
    """

    return bets[int(betNumber) - 1]


def isBetAmountValid(betAmount):
    """
        Check if a bet amount is between the minimum and maximum allowed amounts
    """

    if betAmount and betAmount >= float(args.minimum_bet) and betAmount <= getMaxPossibleBet():
        return True

    return False


def isSpecificChoiceValid(choice):
    global american, french

    # Convert choice to int except for `00`
    if choice != '00':
        choice = int(choice)

    if args.type == 'french':
        if choice in list(french):
            return True
    elif args.type == 'american':
        if choice in list(american):
            return True

    return False


def play(previousBetNumber=None, previousBetAmount=None):
    """
        Inititate a game
    """

    # Check bank status
    checkBankStatus()

    try:
        # Show bets table
        print()
        betsTable()

        # Show bank
        print()
        showBank()

        # Choose a bet number
        valid = False
        while valid == False:
            if previousBetNumber:
                previousBet = getBet(previousBetNumber)
                betNumber = input('* Choose a bet number (just press [ENTER] to play again `%s`): ' % (previousBet['name']))

                # Default to previous bet
                if betNumber == '':
                    betNumber = previousBetNumber
            else:
                betNumber = input('* Choose a bet number: ')

            # Check if the bet type is valid
            valid = isBetTypeValid(betNumber)

        # Display bet name
        bet = getBet(betNumber)
        print('* Bet chosen: %s' % (bet['name']))

        # Optionally pick a specific wheel position
        specificChoice = None
        if bet['type'] == 'pickone':
            valid = False
            while valid == False:
                specificChoice = input('* Pick a number from the wheel: ')

                # Check if the bet type is valid
                valid = isSpecificChoiceValid(specificChoice)

        # Choose a bet number
        valid = False
        while valid == False:
            if previousBetAmount and previousBetAmount < getMaxPossibleBet():
                betAmount = input('* Place your bets: (min: %s, max: %s) (just press [ENTER] to play again %s): ' % (amountToCurrency(args.minimum_bet), amountToCurrency(getMaxPossibleBet()), amountToCurrency(previousBetAmount)))

                # Default to previous bet
                if betAmount == '':
                    betAmount = previousBetAmount
            else:
                betAmount = input('* Place your bets: (min: %s, max: %s): ' % (amountToCurrency(args.minimum_bet), amountToCurrency(getMaxPossibleBet())))

            # Check if the bet amount is valid
            if betAmount:
                valid = isBetAmountValid(float(betAmount))

        # Initiate the game
        getOutcome(int(betAmount), bet, specificChoice)

        # Start another game
        time.sleep(2)
        play(betNumber, float(betAmount))
    except KeyboardInterrupt:
        print()
        showBank()
        print('* Your bank is saved.')
        print('* Game interrupted')


def main():
    play()


if __name__ == '__main__':
    main()