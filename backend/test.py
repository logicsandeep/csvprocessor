import requests
from bs4 import BeautifulSoup

def print_unicode_grid_from_published_gdoc(published_url):
    # STEP 1: Get HTML content from the published Google Doc
    response = requests.get(published_url)
    response.raise_for_status()
    html = response.text

    # STEP 2: Extract visible text using BeautifulSoup
    soup = BeautifulSoup(html, "html.parser")
    text = soup.get_text()

    # STEP 3: Parse the lines
    data = []
    for line in text.splitlines():
        parts = line.strip().split()
        if len(parts) != 3:
            continue
        char, x_str, y_str = parts
        try:
            x, y = int(x_str), int(y_str)
            data.append((char, x, y))
        except ValueError:
            continue

    if not data:
        print("No valid data found.")
        return

    # STEP 4: Determine grid size
    max_x = max(x for _, x, _ in data)
    max_y = max(y for _, _, y in data)

    # STEP 5: Create and fill the grid
    grid = [[' ' for _ in range(max_x + 1)] for _ in range(max_y + 1)]
    for char, x, y in data:
        grid[y][x] = char

    # STEP 6: Print the grid
    for row in grid:
        print(''.join(row))

# Usage
#url = "https://docs.google.com/document/d/e/2PACX-1vQGUck9HIFCyezsrBSnmENk5ieJuYwpt7YHYEzeNJkIb9OSDdx-ov2nRNReKQyey-cwJOoEKUhLmN9z/pub"
url = "https://docs.google.com/document/d/e/2PACX-1vRMx5YQlZNa3ra8dYYxmv-QIQ3YJe8tbI3kqcuC7lQiZm-CSEznKfN_HYNSpoXcZIV3Y_O3YoUB1ecq/pub"
print_unicode_grid_from_published_gdoc(url)
