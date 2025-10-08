import streamlit as st
import requests
import io
from PIL import Image

# ------- CONFIGURATION --------
# Replace with your actual Roboflow model details and key
ROBOFLOW_API_URL = "https://detect.roboflow.com/ingredient-j9nuw/1"
ROBOFLOW_API_KEY = "rf_ZEnnB5bWiOQAXdSJqnTKsh2Q8QB3"

# Replace with your actual Spoonacular key
SPOONACULAR_API_KEY = "65866a9aa0624f5db8fd64db4097d235"

# ------- APP TITLE AND UI --------
st.title("Zero Waste Recipe Generator")

input_method = st.radio("Choose input method:", ("Upload Image", "Type Ingredients"))

# ------- INGREDIENT DETECTION CODE --------
def detect_ingredients(image_bytes):
    response = requests.post(
        ROBOFLOW_API_URL,
        params={"api_key": ROBOFLOW_API_KEY},
        files={"file": image_bytes},
        headers={"accept": "application/json"}
    )
    try:
        result = response.json()
        return list({pred['class'] for pred in result.get("predictions", [])})
    except Exception:
        return []

# ------- RECIPE FETCHING CODE --------
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

# ------- MAIN FLOW --------
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

# ------- RECIPE GENERATION & DISPLAY --------
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
