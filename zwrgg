import streamlit as st
import requests
import io
from PIL import Image
import numpy as np
from ultralytics import YOLO

# Load YOLOv8 model once on app start
model = YOLO('yolov8n.pt')  # feel free to change to yolov8m.pt or your own custom weights

# Spoonacular API key - replace with your actual key
SPOONACULAR_API_KEY = "65866a9aa0624f5db8fd64db4097d235"

st.title("Zero Waste Recipe Generator")

input_method = st.radio("Choose input method:", ("Upload Image", "Type Ingredients"))

# Function to detect ingredients using YOLOv8 model locally
def detect_ingredients(image_bytes):
    img = Image.open(io.BytesIO(image_bytes)).convert('RGB')
    img_np = np.array(img)
    
    results = model(img_np)
    
    classes = set()
    for result in results:
        for c in result.boxes.cls:
            class_id = int(c)
            class_name = model.names[class_id]  # Access class names from model
            classes.add(class_name)
    return list(classes)

# Function to fetch recipes from the Spoonacular API based on ingredients
def fetch_recipes(ingredients):
    url = "https://api.spoonacular.com/recipes/findByIngredients"
    params = {
        "ingredients": ",".join(ingredients),
        "number": 5,
        "apiKey": SPOONACULAR_API_KEY
    }
    try:
        resp = requests.get(url, params=params)
        if resp.status_code == 200:
            return resp.json()
    except Exception:
        pass
    return []

detected_ingredients = []

if input_method == "Upload Image":
    uploaded_file = st.file_uploader("Upload leftover food image", type=["jpg", "png"])
    if uploaded_file:
        img_bytes = uploaded_file.read()
        st.image(Image.open(io.BytesIO(img_bytes)), caption="Your image")
        st.info("Detecting ingredients...")
        detected_ingredients = detect_ingredients(img_bytes)
        st.write("Detected Ingredients:", detected_ingredients)
        if not detected_ingredients:
            st.warning("No recognizable ingredients found in this image. Please try another image or enter ingredients manually.")

elif input_method == "Type Ingredients":
    raw = st.text_input("Enter ingredients (comma separated):")
    if raw:
        detected_ingredients = [i.strip() for i in raw.split(",") if i.strip()]
        st.write("Entered Ingredients:", detected_ingredients)

if detected_ingredients:
    st.info("Searching for recipes...")
    recipes = fetch_recipes(detected_ingredients)
    if recipes:
        for recipe in recipes:
            st.subheader(recipe['title'])
            st.image(recipe['image'])
            link = f"https://spoonacular.com/recipes/{recipe['title'].replace(' ', '-')}-{recipe['id']}"
            st.markdown(f"[See Full Recipe]({link})", unsafe_allow_html=True)
    else:
        st.warning("No recipes found for these ingredients.")
