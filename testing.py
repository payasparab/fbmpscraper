import unittest
from html_to_df import (
    convert_html_path_to_readable, 
    convert_html_to_prices,
    beautify_data 
)

class TestMyModule(unittest.TestCase):
    
    def test_add(self):
        self.assertEqual(add(3, 5), 8)
        self.assertEqual(add(-1, 1), 0)
        self.assertEqual(add(-1, -1), -2)
        
    def test_subtract(self):
        self.assertEqual(subtract(3, 5), -2)
        self.assertEqual(subtract(5, 3), 2)
        self.assertEqual(subtract(3, 3), 0)

# This block allows the tests to be run with the command "python -m unittest test_my_module.py"
if __name__ == '__main__':
    unittest.main()
To run the tests, you can use the command:

Copy code
python -m unittest test_my_module.py
This will execute the tests in test_my_module.py and print the results to the console.

You can expand on this basic structure by adding more test methods to TestMyModule or by creating additional test classes. Remember, each test method should ideally test a single "unit" of functionality, and its name should be descriptive of what it tests.





