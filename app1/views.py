import pytesseract
from PIL import Image
from django.shortcuts import render
from django.conf import settings
import requests
from .models import Menu, Dish
from .forms import MenuUploadForm

def process_menu_image(menu_image):
    """
    Process the uploaded menu image using OCR (pytesseract)
    and return a list of dishes extracted from the image.
    """
    image = Image.open(menu_image)  # Open the uploaded image
    text = pytesseract.image_to_string(image)  # Extract text using pytesseract
    dishes = parse_menu_text(text)  # Custom function to parse text and extract dishes
    return dishes

def generate_image_via_api(prompt):
    """
    Generate an image based on the dish name and description via the OpenAI API.
    """
    api_url = "https://api.openai.com/v1/images/generations"
    headers = {"Authorization": f"Bearer {settings.OPENAI_API_KEY}"}
    data = {
        "prompt": prompt,
        "n": 1,
        "size": "512x512",
    }
    response = requests.post(api_url, json=data, headers=headers)
    if response.status_code == 200:
        return response.json()["data"][0]["url"]
    return None

from django.shortcuts import render
from .forms import MenuImageForm
from .models import DishImage
from django.conf import settings

def upload_menu(request):
    if request.method == 'POST':
        form = MenuImageForm(request.POST, request.FILES)
        if form.is_valid():
            menu_image = form.cleaned_data['menu_image']

            # Process the menu image here, generate the dish image
            # This is just a placeholder for your actual image processing code
            dish_image = process_menu_image(menu_image)

            # Assuming the dish image is saved and accessible via URL
            dish_image_url = settings.MEDIA_URL + 'dish_images/' + dish_image.filename

            return render(request, 'app1/upload_menu.html', {'form': form, 'dish_image_url': dish_image_url})
    else:
        form = MenuImageForm()

    return render(request, 'app1/upload_menu.html', {'form': form})


def menu_result(request):
    """
    Display the result page showing the generated menu and its dishes.
    """
    # You can pass the menu and dishes to the template for display
    menu = Menu.objects.last()  # Assuming the last menu is the one to display
    dishes = Dish.objects.filter(menu=menu)  # Get all dishes related to the last menu

    return render(request, "app1/menu_result.html", {"menu": menu, "dishes": dishes})
