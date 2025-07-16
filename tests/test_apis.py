import sys
import os
from unittest.mock import patch, MagicMock
import unittest
from requests.exceptions import Timeout
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from apis import genai_fitness_plan

###############
#### tests ####
###############

class APITests(unittest.TestCase):
    @patch('apis.genai.GenerativeModel') 
    def test_genai_fitness_plan_response(self, mock_model_class):
        mock_model_instance = MagicMock()
        mock_model_class.return_value = mock_model_instance

        mock_model_instance.generate_content.return_value.text = "This is a fitness plan"
        result = genai_fitness_plan("25", "70", "gain muscle")
        self.assertEqual(result, "This is a fitness plan")
        mock_model_instance.generate_content.assert_called_once()

if __name__ == '__main__':
    unittest.main()