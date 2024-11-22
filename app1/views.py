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

def upload_menu(request):
    """
    Handle the menu upload process: display the upload form, process the uploaded image,
    extract dishes, and generate AI-generated images for each dish.
    """
    if request.method == "POST":
        form = MenuUploadForm(request.POST, request.FILES)
        if form.is_valid():
            menu_image = form.cleaned_data["menu_image"]
            menu = Menu.objects.create(title="Uploaded Menu")  # Create a new menu
            dishes = process_menu_image(menu_image)  # Process the image to get dish names and descriptions

            # For each dish, generate an image and save it in the database
            for dish_name, description in dishes:
                image_url = generate_image_via_api(f"{dish_name}, {description}")
                dish = Dish.objects.create(
                    menu=menu, name=dish_name, description=description
                )
                # Save the generated image locally and associate with the dish
                if image_url:
                    response = requests.get(image_url)
                    image_path = f"media/dish_images/{dish_name}.png"
                    with open(image_path, "wb") as f:
                        f.write(response.content)
                    dish.generated_image = image_path  # Save image path in the database
                    dish.save()

            return render(request, "app1/menu_result.html", {"menu": menu, "dishes": dishes})
    else:
        form = MenuUploadForm()  # If GET request, show the upload form

    return render(request, "app1/upload_menu.html", {"form": form})


def menu_result(request):
    """
    Display the result page showing the generated menu and its dishes.
    """
    # You can pass the menu and dishes to the template for display
    menu = Menu.objects.last()  # Assuming the last menu is the one to display
    dishes = Dish.objects.filter(menu=menu)  # Get all dishes related to the last menu

    return render(request, "app1/menu_result.html", {"menu": menu, "dishes": dishes})
