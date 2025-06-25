import random
import time
from collections import defaultdict

class RockPaperScissorsAI:
    def __init__(self):
        self.player_history = []
        self.player_patterns = defaultdict(lambda: defaultdict(int))
        self.last_prediction = None
        
    def predict_player_move(self):
        """Predict the player's next move based on their patterns"""
        if not self.player_history:
            return random.choice(["rock", "paper", "scissors"])
            
        # Look for patterns in the player's moves
        last_move = self.player_history[-1]
        if len(self.player_history) >= 2:
            pattern = (self.player_history[-2], last_move)
            next_moves = self.player_patterns[pattern]
            
            if next_moves:
                most_likely = max(next_moves, key=next_moves.get)
                self.last_prediction = most_likely
                return most_likely
        
        # Fallback to random if not enough data
        return random.choice(["rock", "paper", "scissors"])
    
    def counter_move(self, predicted_move):
        """Choose a move that counters the predicted player move"""
        counter_strategy = {
            "rock": "paper",
            "paper": "scissors",
            "scissors": "rock"
        }
        return counter_strategy.get(predicted_move, random.choice(["rock", "paper", "scissors"]))
    
    def record_player_move(self, move):
        """Record the player's move for pattern analysis"""
        if len(self.player_history) >= 2:
            # Record the pattern: what move followed the previous two moves?
            pattern = tuple(self.player_history[-2:])
            self.player_patterns[pattern][move] += 1
        
        self.player_history.append(move)

# Game setup
HANDS = {
    "rock": "✊",
    "paper": "✋",
    "scissors": "✌️"
}

RULES = {
    "rock": "scissors",    # rock beats scissors
    "scissors": "paper",   # scissors beat paper
    "paper": "rock"        # paper beats rock
}

def determine_winner(player_choice, ai_choice):
    """Determine the winner of the round"""
    if player_choice == ai_choice:
        return "tie"
    elif RULES[player_choice] == ai_choice:
        return "player"
    else:
        return "ai"

def print_header():
    """Print the game header with instructions"""
    print("\033[1;36m" + "=" * 50)
    print("ROCK-PAPER-SCISSORS GAME".center(50))
    print("=" * 50 + "\033[0m")
    print(f"Choose: \033[1;33mrock {HANDS['rock']}\033[0m, \033[1;32mpaper {HANDS['paper']}\033[0m, or \033[1;31mscissors {HANDS['scissors']}\033[0m")
    print("Type 'quit' to exit the game")
    print("\033[1;35m" + "-" * 50 + "\033[0m")

def print_result(player_choice, ai_choice, result, scores):
    """Print the result of the round with visual effects"""
    # Display choices
    print(f"\n\033[1mYour choice: {HANDS[player_choice]} \033[1;33m{player_choice.upper()}\033[0m")
    print(f"AI's choice: {HANDS[ai_choice]} \033[1;35m{ai_choice.upper()}\033[0m")
    
    # Display result with color
    if result == "player":
        print("\033[1;32m" + ">> YOU WIN THIS ROUND! <<" + "\033[0m")
    elif result == "ai":
        print("\033[1;31m" + ">> AI WINS THIS ROUND! <<" + "\033[0m")
    else:
        print("\033[1;34m" + ">> IT'S A TIE! <<" + "\033[0m")
    
    # Display scores
    print(f"\n\033[1mSCORE: You {scores['player']} - {scores['ai']} AI\033[0m")
    print("\033[1;35m" + "-" * 50 + "\033[0m\n")

def main():
    # Initialize game
    ai = RockPaperScissorsAI()
    scores = {"player": 0, "ai": 0, "ties": 0}
    round_count = 0
    
    print_header()
    
    while True:
        round_count += 1
        print(f"\033[1;37mROUND {round_count}\033[0m")
        
        # Get player input with validation
        while True:
            player_choice = input("Your move: ").lower()
            if player_choice in ["rock", "paper", "scissors"]:
                break
            elif player_choice == "quit":
                print("\n\033[1;36mThanks for playing! Final scores:")
                print(f"You: {scores['player']} | AI: {scores['ai']} | Ties: {scores['ties']}\033[0m")
                return
            else:
                print("\033[1;31mInvalid choice. Please enter rock, paper, or scissors.\033[0m")
        
        # AI makes a move
        ai.record_player_move(player_choice)
        predicted_player_move = ai.predict_player_move()
        ai_choice = ai.counter_move(predicted_player_move)
        
        # Determine result
        result = determine_winner(player_choice, ai_choice)
        
        # Update scores
        if result == "player":
            scores["player"] += 1
        elif result == "ai":
            scores["ai"] += 1
        else:
            scores["ties"] += 1
        
        # Display result
        print_result(player_choice, ai_choice, result, scores)
        
        # Pause before next round
        time.sleep(1)

if __name__ == "__main__":
    main()