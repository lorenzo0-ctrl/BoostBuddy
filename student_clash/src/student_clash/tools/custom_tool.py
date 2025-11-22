from crewai.tools import BaseTool
from typing import Type
from pydantic import BaseModel, Field
import requests
import logging

logger = logging.getLogger(__name__)

class FoodSearchInput(BaseModel):
    """Input for the food search tool."""
    food_name: str = Field(description="The name of the food to search for (e.g., 'greek yogurt 0', 'avocado').", min_length=1)

def search_food_facts(food_name: str) -> str:
    """
    Queries the Open Food Facts API to find nutritional data for a food item.
    Returns a summary of macronutrients per 100g.
    """
    url = "https://it.openfoodfacts.org/cgi/search.pl"
    params = {
        "search_terms": food_name,
        "search_simple": 1,
        "action": "process",
        "json": 1,
        "page_size": 1
    }

    try:
        logger.info(f"Searching for food: {food_name}")
        response = requests.get(url, params=params, timeout=15)
        response.raise_for_status()

        data = response.json()
        
        if not data.get('products'):
            logger.warning(f"No products found for: {food_name}")
            return f"No products found for '{food_name}' in the Open Food Facts database."

        product = data['products'][0]
        nutrients = product.get('nutriments', {})

        calories = nutrients.get('energy-kcal_100g', 'N/D')
        protein = nutrients.get('proteins_100g', 'N/D')
        fat = nutrients.get('fat_100g', 'N/D')
        carbs = nutrients.get('carbohydrates_100g', 'N/D')
        
        product_name = product.get('product_name', food_name)
        
        summary = (
            f"Nutritional Data for **{product_name}** (per 100g):\n"
            f"  - Calories: {calories} kcal\n"
            f"  - Protein: {protein} g\n"
            f"  - Fat: {fat} g\n"
            f"  - Carbohydrates: {carbs} g\n"
            f"Source: Open Food Facts"
        )
        logger.info(f"Search completed for: {product_name}")
        return summary

    except requests.exceptions.Timeout:
        logger.error(f"Timeout searching for: {food_name}")
        return f"Timeout: the search for '{food_name}' took too long."
    except requests.exceptions.HTTPError as e:
        logger.error(f"HTTP error: {e.response.status_code}")
        return f"API error (HTTP {e.response.status_code}): unable to retrieve data."
    except requests.exceptions.RequestException as e:
        logger.error(f"Connection error: {e}")
        return f"Connection error: {e}"
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        return f"Error processing data: {e}"
class OpenFoodFactsTool(BaseTool):
    name: str = "Open Food Facts Search"
    description: str = (
        "A useful tool to search and retrieve precise nutritional data (calories, macros) "
        "for specific foods by querying the public Open Food Facts API."
    )
    args_schema: Type[BaseModel] = FoodSearchInput 

    def _run(self, food_name: str) -> str:
        """Runs the tool. Calls the search_food_facts function."""
        return search_food_facts(food_name)

open_food_facts_tool = OpenFoodFactsTool()