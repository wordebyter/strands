from flask import Flask, render_template, request, jsonify
import random

app = Flask(__name__)

# Define multiple categories with corresponding words
CATEGORIES = {
    "Natural Plant Products": ["FRUITS", "APPLE", "CHERRY", "DURIAN", "ELDERBERRY", "ORANGE", "KIWI", "MANGO"],
    "Notable Lab Workers": ["CHEMISTS", "DALTON", "CURIE", "BUNSEN", "PAULING", "FRANKLIN", "KLAPROTH"],
    "Garments": ["CLOTHING", "OVERCOAT", "SCARFS", "MITTENS", "PONCHO", "JACKET", "SWEATER"],
    "Sound Makers": ["BAND", "GUITAR", "CLARINET", "TRUMPET", "VIOLIN", "TROMBONE", "CELLO", "HARP"],
    "Oceanic": ["MARINE", "SEAHORSE", "OCTOPUS", "STARFISH", "MANATEE", "KILLERWHALES"],
    "Renowned Authors": ["WRITERS", "SHAKESPEARE", "ORWELL", "TOLSTOY", "AUSTEN", "TWAIN", "HERING"],
    "Common Fixtures": ["FURNITURE", "CHAIR", "TABLE", "BEANBAG", "CABINET", "SHELF", "STOOL", "COUCH"],
    "Cooling Substances": ["DRINKS", "COFFEE", "JUICE", "WATER", "MILK", "SELTZER", "SMOOTHIES", "WHISKY"],
    "Famous Explorers": ["ADVENTURERS", "COLUMBUS", "MAGELLAN", "COOK", "POLO", "HUDSON", "CARTIER"],
    "El Classico": ["BOOKS", "ODYSSEY", "HAMLET", "DICKENS", "AUSTEN", "TWAIN", "ORWELL", "BRONTE"],
    "Household Computers": ["DEVICES", "RADIO", "DRYER", "LAPTOP", "TABLET", "PHONE", "PRINTER", "SPEAKER"]
}

def place_word(grid, word):
    height, width = len(grid), len(grid[0])
    directions = [
        (0, 1),   # right
        (1, 0),   # down
        (0, -1),  # left
        (-1, 0),  # up
        (1, 1),   # diagonal down-right
        (1, -1),  # diagonal down-left
        (-1, 1),  # diagonal up-right
        (-1, -1)  # diagonal up-left
    ]
    
    for _ in range(100):  # try 100 times to place the word
        x = random.randint(0, width - 1)
        y = random.randint(0, height - 1)
        
        if grid[y][x] == ' ':
            path = [(y, x)]
            placed = word[0]
            
            for letter in word[1:]:
                valid_moves = []
                random.shuffle(directions)
                
                for dy, dx in directions:
                    new_y, new_x = y + dy, x + dx
                    if (0 <= new_y < height and 0 <= new_x < width and 
                        grid[new_y][new_x] == ' ' and (new_y, new_x) not in path):
                        valid_moves.append((new_y, new_x))
                
                if not valid_moves:
                    break
                
                y, x = random.choice(valid_moves)
                path.append((y, x))
                placed += letter
            
            if len(placed) == len(word):
                for (y, x), letter in zip(path, word):
                    grid[y][x] = letter
                return True
    
    return False

def generate_grid(words):
    grid = [[' ' for _ in range(8)] for _ in range(6)]
    
    for word in words:
        if not place_word(grid, word):
            print(f"Warning: Couldn't place '{word}'")
            return None
    
    return grid

@app.route('/')
def index():
    category, words = random.choice(list(CATEGORIES.items()))
    grid = generate_grid(words)
    while grid is None:
        grid = generate_grid(words)
    return render_template('game.html', grid=grid, category=category, words=words)

@app.route('/check_word', methods=['POST'])
def check_word():
    word = request.json['word']
    category, words = request.json['category'], CATEGORIES[request.json['category']]
    if word in words:
        return jsonify({"valid": True, "isTheme": word == words[0]})
    return jsonify({"valid": False, "isTheme": False})

if __name__ == '__main__':
    app.run(debug=True)
