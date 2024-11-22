import pytesseract
from PIL import Image
from django.conf import settings
import requests
from .models import Menu, Dish
from .forms import MenuUploadForm
from django.shortcuts import render, redirect
from django.http import HttpResponse

def process_menu_image(menu_image):
    try:
        image = Image.open(menu_image)
        text = pytesseract.image_to_string(image)
        # Clean up the text if necessary (strip unnecessary spaces or unwanted characters)
        dishes = parse_menu_text(text)  # Custom function to extract dishes from text
        return dishes
    except Exception as e:
        # Add logging for better tracking of issues
        print(f"Error processing menu image: {e}")
        return []

def generate_image_via_api(prompt):
    api_url = "https://api.openai.com/v1/images/generations"
    headers = {"Authorization": f"Bearer {settings.OPENAI_API_KEY}"}
    data = {
        "prompt": prompt,
        "n": 1,
        "size": "512x512",
    }
    try:
        response = requests.post(api_url, json=data, headers=headers)
        response.raise_for_status()  # Raises an exception for HTTP errors
        if response.status_code == 200:
            return response.json()["data"][0]["url"]
        else:
            print(f"API Error: {response.text}")
    except requests.exceptions.RequestException as e:
        print(f"Error during API request: {e}")
    return None



def upload_menu(request):
    if request.method == "POST":
        form = MenuUploadForm(request.POST, request.FILES)
        if form.is_valid():
            menu_image = form.cleaned_data["menu_image"]
            menu = Menu.objects.create(title="Uploaded Menu")
            dishes = process_menu_image(menu_image)

            if not dishes:
                return HttpResponse("No dishes found in the menu image. Please upload a valid menu image.")

            # Prepare list of dish objects to send to template
            dish_list = []
            for dish_name, description in dishes:
                image_url = generate_image_via_api(f"{dish_name}, {description}")
                dish = Dish.objects.create(
                    menu=menu, name=dish_name, description=description
                )

                if image_url:
                    response = requests.get(image_url)
                    image_path = f"media/dish_images/{dish_name}.png"
                    with open(image_path, "wb") as f:
                        f.write(response.content)
                    dish.generated_image = image_path
                    dish.save()

                dish_list.append(dish)

            return render(request, "menu_images_app/menu_result.html", {"menu": menu, "dishes": dish_list})
    else:
        form = MenuUploadForm()

    return render(request, "menu_images_app/upload_menu.html", {"form": form})
