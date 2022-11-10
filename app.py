from flask import Flask, request, render_template
from PIL import Image, ImageFilter
from pprint import PrettyPrinter
# from dotenv import load_dotenv
import json
import os
import random
import requests

# load_dotenv()


app = Flask(__name__)

@app.route('/')
def homepage():
    """A homepage with handy links for your convenience."""
    return render_template('home.html')

################################################################################
# COMPLIMENTS ROUTES
################################################################################

list_of_compliments = [
    'awesome',
    'beatific',
    'blithesome',
    'conscientious',
    'coruscant',
    'erudite',
    'exquisite',
    'fabulous',
    'fantastic',
    'gorgeous',
    'indubitable',
    'ineffable',
    'magnificent',
    'outstanding',
    'propitioius',
    'remarkable',
    'spectacular',
    'splendiferous',
    'stupendous',
    'super',
    'upbeat',
    'wondrous',
    'zoetic'
]

@app.route('/compliments')
def compliments():
    """Shows the user a form to get compliments."""
    return render_template('compliments_form.html')

@app.route('/compliments_results')
def compliments_results():
    """Show the user some compliments."""
    wants_compliment = request.args.get('wants_compliments')
    num_compliments = request.args.get('num_compliments')
    num_compliments = int(num_compliments)
    if wants_compliment == 'yes':
        list_compliments = random.sample(list_of_compliments, k=num_compliments)

    context = {
        'name': request.args.get('users_name'),
        "compliments": list_compliments
    }

    return render_template('compliments_results.html', **context)


################################################################################
# ANIMAL FACTS ROUTE
################################################################################

animal_to_fact = {
    'koala': 'Koala fingerprints are so close to humans\' that they could taint crime scenes.',
    'parrot': 'Parrots will selflessly help each other out.',
    'mantis shrimp': 'The mantis shrimp has the world\'s fastest punch.',
    'lion': 'Female lions do 90 percent of the hunting.',
    'narwhal': 'Narwhal tusks are really an "inside out" tooth.'
}

@app.route('/animal_facts')
def animal_facts():
    """Show a form to choose an animal and receive facts."""
    animal = request.args.get('animal')
    if animal == 'koala':
        animal_fact = "Koala fingerprints are so close to humans\' that they could taint crime scenes."
    elif animal == 'parrot':
        animal_fact = "Parrots will selflessly help each other out."
    elif animal == 'mantis shrimp':
        animal_fact = "The mantis shrimp has the world\'s fastest punch."
    elif animal == 'lion':
        animal_fact = "Female lions do 90 percent of the hunting."
    elif animal == 'narwhal':
        animal_fact = "Narwhal tusks are really an 'inside out' tooth."
    else:
        animal_fact = "I don't have any facts about that animal. Please try again!"

    context = {
        'animals': list(animal_to_fact.keys()),
        "fact": animal_fact
    }
    return render_template('animal_facts.html', **context)


# ################################################################################
# # IMAGE FILTER ROUTE
# ################################################################################

filter_types_dict = {
    'blur': ImageFilter.BLUR,
    'contour': ImageFilter.CONTOUR,
    'detail': ImageFilter.DETAIL,
    'edge enhance': ImageFilter.EDGE_ENHANCE,
    'emboss': ImageFilter.EMBOSS,
    'sharpen': ImageFilter.SHARPEN,
    'smooth': ImageFilter.SMOOTH
}

def save_image(image, filter_type):
    """Save the image, then return the full file path of the saved image."""
    # Append the filter type at the beginning (in case the user wants to 
    # apply multiple filters to 1 image, there won't be a name conflict)
    new_file_name = f"{filter_type}-{image.filename}"
    image.filename = new_file_name
    # Construct full file path
    file_path = os.path.join(app.root_path, 'static/images', new_file_name)
    # Save the image
    image.save(file_path)
    return file_path


def apply_filter(file_path, filter_name):
    """Apply a Pillow filter to a saved image."""
    i = Image.open(file_path)
    i.thumbnail((500, 500))
    i = i.filter(filter_types_dict.get(filter_name))
    i.save(file_path)


@app.route('/image_filter', methods=['GET', 'POST'])
def image_filter():
    """Filter an image uploaded by the user, using the Pillow library."""
    filter_types = filter_types_dict.keys()

    if request.method == 'POST':
        # Get the user's chosen filter type (whichever one they chose in the form) and save
        filter_type = request.form.get('filter_type')
        
        # Get the image file submitted by the user
        image = request.files.get('users_image')

        # call `save_image()` on the image & the user's chosen filter type, save the returned value as variable
        new_file_path = save_image(image, filter_type)

        # Call `apply_filter()` on the file path & filter type
        filename = apply_filter(new_file_path, filter_type)

        image_url = f'./static/images/{image.filename}'

        context = {
            "filters": list(filter_types),
            "image_url": image_url
    
        }

        return render_template('image_filter.html', **context)

    else: 
        context = {
            "filters": list(filter_types),
        }
        return render_template('image_filter.html', **context)


################################################################################
# GIF SEARCH ROUTE
################################################################################

@app.route('/gif_search', methods=['GET', 'POST'])
def gif_search():
    """Show a form to search for GIFs and show resulting GIFs from Tenor API."""
    if request.method == 'POST':
        search = request.form.get('search_query')
        quantity = request.form.get('quantity')
        limit = int(quantity)
        apikey = "AIzaSyBWZkd9EYKL356BTQFOtgmJJvFmUHaMlvc"
        response = requests.get(
        f"https://tenor.googleapis.com/v2/search?q={search}&key={apikey}&limit={limit}")
        gifs = json.loads(response.content).get('results')
        context = {
            'gifs': gifs
        }
        return render_template('gif_search.html', **context)
    else:
        return render_template('gif_search.html')

if __name__ == '__main__':
    app.config['ENV'] = 'development'
    app.run(debug=True, port=3000)
