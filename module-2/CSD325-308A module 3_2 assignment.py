"""
Program: Chō-han Game (Brownfield Modification)
Author: Placeholder Initials: AR
Assignment: Module 3 Brownfield + Flowchart(s)
Date: 2025-11-05

MODIFICATIONS:
1. Input prompt changed to 'AR:'.
2. House cut increased from 10% to 12%.
3. Added a rule: If the dice roll is 2 or 7, the user receives a 10 mon bonus,
   and a message is displayed.
4. All changes are documented below.
"""

import random

# --- Constants ---
HOUSE_CUT = 0.12  # Changed from 0.10 to 0.12 (12%)
BONUS_ROLLS = [2, 7]
BONUS_AMOUNT = 10

# --- Function Definitions ---

def roll_dice():
    """Simulates rolling two dice (2d6)."""
    die1 = random.randint(1, 6)
    die2 = random.randint(1, 6)
    return die1 + die2

def get_roll_type(total):
    """Determines if the roll is Chō (Even) or Han (Odd)."""
    if total % 2 == 0:
        return "Chō (Even)"
    else:
        return "Han (Odd)"

# --- Main Game Loop ---

def play_chohan():
    """Runs the main Chō-han game logic."""
    purse = 100 # Starting Mon

    print("-------------------------------------------------------")
    print("Welcome to Chō-han (Even-Odd Dice Game)!")
    print(f"Starting purse: {purse} mon.")
    # New instruction notice added
    print("NOTICE: If the dice roll total is a 2 or a 7, you get a 10 mon bonus!")
    print(f"The house takes a {HOUSE_CUT * 100:.0f}% cut from all winnings.")
    print("-------------------------------------------------------")

    while purse > 0:
        print(f"\nCurrent Purse: {purse} mon")

        # Get bet amount from user
        try:
            # Change 1: Input prompt changed to initials
            bet = int(input("AR: Place your bet (mon): "))
        except ValueError:
            print("Invalid input. Please enter a whole number.")
            continue

        if bet <= 0:
            print("You must bet at least 1 mon.")
            continue
        if bet > purse:
            print(f"You only have {purse} mon. You cannot bet that much.")
            continue

        # Get user's choice
        choice_input = input("AR: Bet on Chō (Even) or Han (Odd)? (c/h): ").lower()
        if choice_input not in ['c', 'h']:
            print("Invalid choice. Please enter 'c' for Chō or 'h' for Han.")
            continue

        # Process the roll
        total_roll = roll_dice()
        roll_type = get_roll_type(total_roll)

        print(f"\nDealer rolls the dice... Total roll: {total_roll} ({roll_type})")

        # Check for Bonus Rolls (Change 3 & 4)
        if total_roll in BONUS_ROLLS:
            print(f"*** BONUS! Roll was {total_roll}. You receive a {BONUS_AMOUNT} mon bonus! ***")
            purse += BONUS_AMOUNT
            print(f"New Purse: {purse} mon")
            # Note: Bonus is added regardless of whether the user won or lost the bet.

        # Determine Win/Loss
        user_win = (choice_input == 'c' and roll_type.startswith("Chō")) or \
                   (choice_input == 'h' and roll_type.startswith("Han"))

        if user_win:
            # Calculate winnings and apply house cut (Change 2)
            winnings = bet
            cut = round(winnings * HOUSE_CUT)
            net_gain = winnings - cut
            purse += net_gain

            print(f"You WIN! You staked {bet} mon and won {winnings} mon.")
            print(f"House cut of {HOUSE_CUT * 100:.0f}% ({cut} mon) applied.")
            print(f"Your net gain is {net_gain} mon.")
        else:
            # Loss
            purse -= bet
            print(f"You LOSE. You lost your {bet} mon stake.")

    print("\n-------------------------------------------------------")
    print("Game Over! You ran out of mon.")
    print("-------------------------------------------------------")

if __name__ == "__main__":
    play_chohan()