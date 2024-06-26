from flask import Flask, render_template, request
import random
import string

app = Flask(__name__)

def generate_grid(size, words):
    grid = [['' for _ in range(size)] for _ in range(size)]
    for word in words:
        place_word_in_grid(grid, word)
    fill_empty_spaces(grid)
    return grid

def place_word_in_grid(grid, word):
    size = len(grid)
    word_length = len(word)
    placed = False
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1)]  # All possible directions

    while not placed:
        start_row = random.randint(0, size - 1)
        start_col = random.randint(0, size - 1)
        
        if grid[start_row][start_col] == '':
            grid[start_row][start_col] = word[0]
            current_row, current_col = start_row, start_col
            
            for i in range(1, word_length):
                random.shuffle(directions)
                placed_letter = False
                for dr, dc in directions:
                    new_row, new_col = current_row + dr, current_col + dc
                    if 0 <= new_row < size and 0 <= new_col < size and grid[new_row][new_col] in ['', word[i]]:
                        grid[new_row][new_col] = word[i]
                        current_row, current_col = new_row, new_col
                        placed_letter = True
                        break
                if not placed_letter:
                    break  # If we couldn't place the letter, break out of the loop

            if placed_letter:
                placed = True
            else:
                # Reset the part of the word placed so far
                grid[start_row][start_col] = ''
                for dr, dc in directions:
                    new_row, new_col = start_row + dr, start_col + dc
                    if 0 <= new_row < size and 0 <= new_col < size:
                        if grid[new_row][new_col] == word[0]:
                            grid[new_row][new_col] = ''

def fill_empty_spaces(grid):
    for row in range(len(grid)):
        for col in range(len(grid[row])):
            if grid[row][col] == '':
                grid[row][col] = random.choice(string.ascii_uppercase)

@app.route('/', methods=['GET', 'POST'])
def index():
    size = 10
    theme = "SLITHERY"
    words = ['SLITHERY', 'ANACONDA', 'RATTLESNAKE', 'COTTONMOUTH', 'SNAKES']
    grid = generate_grid(size, words)
    return render_template('index.html', grid=grid, words=words, theme=theme)

if __name__ == '__main__':
    app.run(debug=True)
