import pytesseract
from PIL import Image
from django.shortcuts import render
from django.conf import settings
import requests
from .models import Menu, Dish
from .forms import MenuUploadForm

def process_menu_image(menu_image):
    # Perform OCR
    image = Image.open(menu_image)
    text = pytesseract.image_to_string(image)
    dishes = parse_menu_text(text)  # Custom function to extract dishes from text
    return dishes

def generate_image_via_api(prompt):
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
    if request.method == "POST":
        form = MenuUploadForm(request.POST, request.FILES)
        if form.is_valid():
            menu_image = form.cleaned_data["menu_image"]
            menu = Menu.objects.create(title="Uploaded Menu")
            dishes = process_menu_image(menu_image)

            for dish_name, description in dishes:
                image_url = generate_image_via_api(f"{dish_name}, {description}")
                dish = Dish.objects.create(
                    menu=menu, name=dish_name, description=description
                )
                # Save image locally
                if image_url:
                    response = requests.get(image_url)
                    image_path = f"media/dish_images/{dish_name}.png"
                    with open(image_path, "wb") as f:
                        f.write(response.content)
                    dish.generated_image = image_path
                    dish.save()

            return render(request, "menu_images_app/menu_result.html", {"menu": menu})
    else:
        form = MenuUploadForm()

    return render(request, "menu_images_app/upload_menu.html", {"form": form})
