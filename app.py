from flask import Flask, render_template, request, jsonify
import random

app = Flask(__name__)

# Your custom words and category
CATEGORY = "Fruits"
WORDS = ["APPLE", "BANANA", "CHERRY", "DURIAN", "ELDERBERRY", "ORANGE", "KIWI", "MANGO"]

def place_word(grid, word):
    size = len(grid)
    directions = [
        (0, 1),   # right
        (1, 0),   # down
        (1, 1),   # diagonal down-right
        (-1, 1),  # diagonal up-right
        (0, -1),  # left
        (-1, 0),  # up
        (-1, -1), # diagonal up-left
        (1, -1)   # diagonal down-left
    ]
    
    for _ in range(100):  # try 100 times to place the word
        x = random.randint(0, size - 1)
        y = random.randint(0, size - 1)
        
        if grid[y][x] == ' ' or grid[y][x] == word[0]:
            path = [(y, x)]
            for letter in word[1:]:
                valid_moves = []
                for dy, dx in directions:
                    new_y, new_x = y + dy, x + dx
                    if (0 <= new_y < size and 0 <= new_x < size and 
                        (grid[new_y][new_x] == ' ' or grid[new_y][new_x] == letter) and
                        (new_y, new_x) not in path):
                        valid_moves.append((new_y, new_x))
                
                if not valid_moves:
                    break
                
                y, x = random.choice(valid_moves)
                path.append((y, x))
            
            if len(path) == len(word):
                for i, (y, x) in enumerate(path):
                    grid[y][x] = word[i]
                return True
    
    return False

def generate_grid(words, size=10):
    grid = [[' ' for _ in range(size)] for _ in range(size)]
    
    for word in words:
        if not place_word(grid, word):
            print(f"Warning: Couldn't place '{word}'")
    
    # Fill empty spaces with random letters
    for i in range(size):
        for j in range(size):
            if grid[i][j] == ' ':
                grid[i][j] = random.choice('ABCDEFGHIJKLMNOPQRSTUVWXYZ')
    
    return grid

@app.route('/')
def index():
    grid = generate_grid(WORDS)
    return render_template('game.html', grid=grid, category=CATEGORY, words=WORDS)

@app.route('/check_word', methods=['POST'])
def check_word():
    word = request.json['word']
    if word in WORDS:
        return jsonify({"valid": True})
    return jsonify({"valid": False})

if __name__ == '__main__':
    app.run(debug=True)