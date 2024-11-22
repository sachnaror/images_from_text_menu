# Import necessary libraries
import pytesseract
from PIL import Image
from django.shortcuts import render, redirect
from django.conf import settings
import requests
from .models import Menu, Dish
from .forms import MenuImageForm

def process_menu_image(menu_image):
    """
    Process the uploaded menu image using OCR (pytesseract)
    and return a list of dishes extracted from the image.
    """
    # Open the uploaded image
    image = Image.open(menu_image)

    # Extract text using pytesseract
    text = pytesseract.image_to_string(image)

    # Parse the text to extract dishes (custom logic required)
    dishes = parse_menu_text(text)
    return dishes

def parse_menu_text(text):
    """
    Parse the extracted text from the menu image to extract dish names and descriptions.
    """
    # Example parsing logic: split text by lines and treat each line as a dish
    lines = text.splitlines()
    dishes = []
    for line in lines:
        if line.strip():  # Skip empty lines
            # Basic logic to split name and description (customize as needed)
            parts = line.split("-", 1)
            dish_name = parts[0].strip()
            dish_description = parts[1].strip() if len(parts) > 1 else ""
            dishes.append({"name": dish_name, "description": dish_description})
    return dishes

def generate_image_via_api(prompt):
    """
    Generate an image based on the dish name and description via an API (e.g., OpenAI DALL-E).
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
    Handle the menu image upload and display generated dish images.
    """
    if request.method == 'POST':
        form = MenuImageForm(request.POST, request.FILES)
        if form.is_valid():
            # Save the uploaded menu image
            menu_image_instance = form.save()
            menu_image_path = menu_image_instance.menu_image.path

            # Process the image and extract dishes
            dishes = process_menu_image(menu_image_path)

            # Save menu and dishes to the database
            menu = Menu.objects.create(title="Uploaded Menu")
            for dish in dishes:
                generated_image_url = generate_image_via_api(f"{dish['name']}: {dish['description']}")
                Dish.objects.create(
                    menu=menu,
                    name=dish["name"],
                    description=dish["description"],
                    generated_image=generated_image_url
                )

            return redirect('menu_results')  # Redirect to results page
    else:
        form = MenuImageForm()
    return render(request, 'app1/upload_menu.html', {'form': form})

def menu_result(request):
    """
    Display the result page showing the generated menu and its dishes.
    """
    menu = Menu.objects.last()  # Get the latest menu uploaded
    dishes = Dish.objects.filter(menu=menu)  # Get dishes linked to the latest menu

    return render(request, "app1/menu_result.html", {"menu": menu, "dishes": dishes})
