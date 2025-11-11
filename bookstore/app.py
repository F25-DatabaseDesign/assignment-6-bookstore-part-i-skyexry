from flask import Flask, render_template, request, redirect, url_for, make_response


# instantiate the app
app = Flask(__name__)

# Create a list called categories. The elements in the list should be lists that contain the following information in this order:
#   categoryId
#   categoryName
#   An example of a single category list is: [1, "Biographies"]

# categories: [categoryId, categoryName]
categories = [
    [1, "Physics & Astronomy"],
    [2, "Biology & Life"],
    [3, "Earth & Environment"],
    [4, "Math & Data in Nature"],
]


# Create a list called books. The elements in the list should be lists that contain the following information in this order:
#   bookId     (you can assign the bookId - preferably a number from 1-16)
#   categoryId (this should be one of the categories in the category dictionary)
#   title
#   author
#   isbn
#   price      (the value should be a float)
#   image      (this is the filename of the book image.  If all the images, have the same extension, you can omit the extension)
#   readNow    (This should be either 1 or 0.  For each category, some of the books (but not all) should have this set to 1.
#   An example of a single category list is: [1, 1, "Madonna", "Andrew Morton", "13-9780312287863", 39.99, "madonna.png", 1]

# books: [bookId, categoryId, title, author, isbn, price, image, readNow]
books = [
    [1, 1, "Quantum Paths", "Lena Schwarz",
     "9780000000001", 24.95, "quantum_paths.png", 1],
    [2, 1, "Gravity Waves", "Kai Thompson",
     "9780000000002", 27.50, "gravity_waves.png", 0],
    [3, 1, "Starlight Lab", "Noah Patel",
     "9780000000003", 22.00, "starlight_lab.png", 1],
    [4, 1, "The Dark Universe", "Iris Romero",
     "9780000000004", 29.00, "dark_universe.png", 0],

    [5, 2, "Hidden Cells", "Mira Chen",
     "9780000000005", 23.50, "hidden_cells.png", 1],
    [6, 2, "Evolutionary Code", "Daniel Ruiz",
     "9780000000006", 26.00, "evolution_code.png", 0],
    [7, 2, "Microbe Worlds", "Sara Kim",
     "9780000000007", 21.00, "microbe_worlds.png", 1],
    [8, 2, "Patterns of Life", "Omar Haddad",
     "9780000000008", 25.00, "pattern_of_life.png", 0],

    [9, 3, "Restless Planet", "Elena Rossi",
     "9780000000009", 24.00, "restless_planet.png", 1],
    [10, 3, "Climate Signals", "Jonas Weber",
     "9780000000010", 27.00, "climate_signals.png", 0],
    [11, 3, "Deep Ocean", "Priya Nair",
     "9780000000011", 23.00, "deep_ocean.png", 1],
    [12, 3, "Shifting Plates", "Arjun Mehta",
     "9780000000012", 26.50, "shifting_plates.png", 0],

    [13, 4, "Nature in Numbers", "Hana Sato",
     "9780000000013", 22.50, "nature_numbers.png", 1],
    [14, 4, "Randomness Everywhere", "Leo Garcia",
     "9780000000014", 24.50, "randomness.png", 0],
    [15, 4, "Networks of Life", "Aisha Malik",
     "9780000000015", 25.00, "networks_of_life.png", 1],
    [16, 4, "Data of the Cosmos", "Victor Nguyen",
     "9780000000016", 27.50, "data_of_the_cosmos.png", 0],
]


STORE_NAME = "Dark Matter Books"


# set up routes
@app.route('/')
# def home():
#     #Link to the index page.  Pass the categories as a parameter
#     return render_template()

def home():
    # index page: show all categories and (optionally) featured/read-now books
    read_now_books = [b for b in books if b[7] == 1]
    return render_template(
        "index.html",
        store_name=STORE_NAME,
        categories=categories,
        books=books,
        readNowBooks=read_now_books,
    )


@app.route('/category')
# def category():
#     # Store the categoryId passed as a URL parameter into a variable

#     # Create a new list called selected_books containing a list of books that have the selected category

#     # Link to the category page.  Pass the selectedCategory, categories and books as parameters
#     return render_template()

def category():
    # categoryId passed as URL parameter, e.g. /category?categoryId=1
    category_id = request.args.get("categoryId", type=int)

    # if no id given, default to first category
    if category_id is None:
        category_id = categories[0][0]

    # books in the selected category
    selected_books = [b for b in books if b[1] == category_id]

    return render_template(
        "category.html",
        store_name=STORE_NAME,
        selectedCategory=category_id,
        categories=categories,
        books=selected_books,
    )


@app.route('/search')
# def search():
#     #Link to the search results page.
#     return render_template()

def search():
    # simple search over title and author: /search?q=planet
    query = request.args.get("q", "").strip()
    results = []

    if query:
        q = query.lower()
        results = [
            b for b in books
            if q in b[2].lower() or q in b[3].lower()
        ]

    return render_template(
        "search.html",
        store_name=STORE_NAME,
        query=query,
        categories=categories,
        books=results,
    )
    

@app.errorhandler(Exception)
# def handle_error(e):
#     """
#     Output any errors - good for debugging.
#     """
#     return render_template('error.html', error=e) # render the edit template

def handle_error(e):
    """
    Output any errors - good for debugging.
    """
    return render_template("error.html", error=e)
    

if __name__ == "__main__":
    app.run(debug = True)
