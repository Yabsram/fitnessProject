import sys
import os
from unittest.mock import patch, MagicMock, Mock
import unittest
from requests.exceptions import Timeout
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from apis import genai_fitness_plan, get_recipes

###############
#### tests ####
###############

class APITests(unittest.TestCase):
    @patch('apis.genai.GenerativeModel') 
    def test_genai_fitness_plan_response(self, mock_model_class):
        mock_model = MagicMock()
        mock_model_class.return_value = mock_model

        mock_model.generate_content.return_value.text = "This is a fitness plan"
        result = genai_fitness_plan("25", "70", "gain muscle")
        self.assertEqual(result, "This is a fitness plan")
        mock_model.generate_content.assert_called_once()

    @patch('apis.requests.get') 
    def test_get_recipes(self, mock_get):
        mock_response = Mock()
        mock_response.json.return_value = {
            "results": [
                {
                    "title": "Food1",
                    "img": "https://img.jpg",
                },
                {
                    "title": "Food2",
                    "img": "https://img2.jpg",
                }
            ]
        }

        mock_get.return_value = mock_response

        params = {"apiKey":"SPOONACULAR_KEY", "query" : "pasta" ,"diet" : "Whole30", "intolerances": ["Egg"]}
        response = get_recipes("https://api.spoonacular.com/recipes/complexSearch", params=params)
        self.assertDictEqual(response, mock_response.json.return_value)
        mock_response.json.assert_called_once()


if __name__ == '__main__':
    unittest.main()