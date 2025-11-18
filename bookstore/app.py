from flask import Flask, render_template, request, redirect, url_for, make_response


# instantiate the app
app = Flask(__name__)

# Create a list called categories. The elements in the list should be lists that contain the following information in this order:
#   categoryId
#   categoryName
#   An example of a single category list is: [1, "Biographies"]

categories = [
    [1, "Brahms"],
    [2, "Chopin"],
    [3, "Reger"],
    [4, "Schumann"],
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

books = [
    # ---------- Brahms ----------
    [1, 1, "Ballades, Op. 10",
     "Johannes Brahms", "978-0000000010", 24.99,
     "Ballades_op_10.jpg", 1],

    [2, 1, "Waltzes, Op. 39",
     "Johannes Brahms", "978-0000000039", 19.99,
     "Waltzes_op_39.jpg", 0],

    [3, 1, "Violin Sonata in a minor",
     "Johannes Brahms", "978-0000000101", 21.99,
     "Violin_Sonata_a_minor.jpg", 1],

    [4, 1, "Brahms am Werk",
     "Johannes Brahms", "978-0000000102", 27.99,
     "Brahms_am_Werk.jpg", 0],

    # ---------- Chopin ----------
    [5, 2, "Ballade in F major, Op. 38",
     "Frédéric Chopin", "978-0000000038", 18.99,
     "Ballade_F_major_op_38.jpg", 1],

    [6, 2, "Ballade in g minor, Op. 23",
     "Frédéric Chopin", "978-0000000023", 18.99,
     "Ballade_g_minor_op_23.jpg", 0],

    [7, 2, "Nocturne in G major, Op. 37 No. 2",
     "Frédéric Chopin", "978-0000000037", 16.99,
     "Nocturne_G_major_op_37_no_2.jpg", 1],

    [8, 2, "Waltz in a minor (with facsimile)",
     "Frédéric Chopin", "978-0000000301", 14.99,
     "Waltz_a_minor_with_facsimile.jpg", 0],

    # ---------- Reger ----------
    [9, 3, "Clarinet Quintet in A major, Op. 146",
     "Max Reger", "978-0000000146", 26.99,
     "Clarinet_Quintet_in_A_major_op_146.jpg", 1],

    [10, 3, "Clarinet Sonata, Op. 107",
     "Max Reger", "978-0000000107", 22.99,
     "Clarinet_Sonata_op_107.jpg", 0],

    [11, 3, "Fantasia and Fugue on B-A-C-H, Op. 46",
     "Max Reger", "978-0000000046", 23.99,
     "Fantasia_and_Fugue_on_B-A-C-H_op_46.jpg", 1],

    [12, 3, "Max Reger – Accordarbeiter",
     "Max Reger", "978-0000000200", 25.99,
     "Max_Reger_Accordarbeiter.jpg", 0],

    # ---------- Schumann ----------
    [13, 4, "Papillons, Op. 2",
     "Robert Schumann", "978-0000000002", 17.99,
     "Papillons_op_2.jpg", 1],

    [14, 4, "Spring Night (from Song Cycle Op. 39)",
     "Robert Schumann", "978-0000000039", 16.99,
     "Spring_night_from_Song_Cycle_op_39.jpg", 0],

    [15, 4, "Piano Quartet in E-flat major, Op. 47",
     "Robert Schumann", "978-0000000047", 24.99,
     "Piano_Quartet_E_flat_major_op_47.jpg", 1],

    [16, 4, "15 bekannte Originalstücke",
     "Robert Schumann", "978-0000000015", 19.99,
     "15_bekannte_Originalstücke.jpg", 0],
]


# set up routes
@app.route('/')
def home():
    # Link to the index page.  Pass the categories as a parameter
    # return render_template()

    # Return the index page with the categories list
    return render_template("index.html", categories=categories)

@app.route('/category')
def category():
    # Store the categoryId passed as a URL parameter into a variable
    category_id = request.args.get("categoryId", type=int)

    if category_id is None:
        # If no categoryId provided, go back to home
        return redirect(url_for("home"))

    # Create a new list called selected_books containing a list of books that have the selected category
    selected_books = [b for b in books if b[1] == category_id]


    # Link to the category page.  Pass the selectedCategory, categories and books as parameters
    # return render_template()
    return render_template(
        "category.html",
        categories=categories,
        books=selected_books,
        selectedCategoryId=category_id,
        selectedCategory=category_id,  # in case your template uses this name
    )

# @app.route('/search')
# def search():
#     #Link to the search results page.
#     # return render_template()
#     return render_template("search.html")

@app.route('/search', methods=['GET', 'POST'])
def search():
    # 从表单里取搜索关键字（POST）或 QueryString（GET）
    if request.method == "POST":
        term = request.form.get("search", "").strip()
    else:
        term = request.args.get("search", "").strip()

    # 这里如果暂时不做真正搜索，可以先只把 term 传给模板
    return render_template("search.html",
                           categories=categories,
                           term=term)


@app.errorhandler(Exception)
def handle_error(e):
    """
    Output any errors - good for debugging.
    """
    return render_template('error.html', error=e) # render the edit template

# @app.errorhandler(Exception)
# def handle_error(e):
#     # 如果你想在终端里看到具体错误，保留这一行打印
#     print(e)

#     return render_template(
#         "error.html",
#         categories=categories   # 让 header 里的下拉菜单还能用
#     ), 500

if __name__ == "__main__":
    app.run(debug = True)