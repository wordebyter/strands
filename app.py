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
    directions = ['horizontal', 'vertical', 'diagonal']

    while not placed:
        direction = random.choice(directions)
        if direction == 'horizontal':
            row = random.randint(0, size - 1)
            col = random.randint(0, size - word_length)
            if all(grid[row][col + i] in ['', word[i]] for i in range(word_length)):
                for i in range(word_length):
                    grid[row][col + i] = word[i]
                placed = True
        elif direction == 'vertical':
            row = random.randint(0, size - word_length)
            col = random.randint(0, size - 1)
            if all(grid[row + i][col] in ['', word[i]] for i in range(word_length)):
                for i in range(word_length):
                    grid[row + i][col] = word[i]
                placed = True
        elif direction == 'diagonal':
            row = random.randint(0, size - word_length)
            col = random.randint(0, size - word_length)
            if all(grid[row + i][col + i] in ['', word[i]] for i in range(word_length)):
                for i in range(word_length):
                    grid[row + i][col + i] = word[i]
                placed = True

def fill_empty_spaces(grid):
    for row in range(len(grid)):
        for col in range(len(grid[row])):
            if grid[row][col] == '':
                grid[row][col] = random.choice(string.ascii_uppercase)

@app.route('/', methods=['GET', 'POST'])
def index():
    size = 10
    words = ['PYTHON', 'FLASK', 'GRID', 'SEARCH']
    grid = generate_grid(size, words)
    return render_template('index.html', grid=grid, words=words)

if __name__ == '__main__':
    app.run(debug=True)
