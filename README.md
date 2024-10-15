# selenium-todo-testing
A simple web-based To-Do List application with automated tests. Built using HTML, CSS, JavaScript, Selenium, and pytest, with test results available in an HTML report format.

Steps to Run the Project

1. Clone the Repository
  git clone https://github.com/your-username/simple-todo-app.git
  cd simple-todo-app

2. Install Python Make sure Python is installed on your system. You can download it from [python.org](https://www.python.org/)

3. Set Up a Virtual Environment
   python -m venv venv

4. Activate the Virtual Environment
  .\venv\Scripts\activate

5. Install Required Packages
  pip install selenium
  pip install pytest
  pip install pytest-html

6. Download WebDriver Download the appropriate WebDriver (e.g., ChromeDriver for Chrome) and ensure it's in your system's PATH. 

7. Running the To-Do App Open the index.html file in a web browser:
  path/to/your/index.html
![image](https://github.com/user-attachments/assets/070a8632-1a37-4abc-9dbd-fa50dbb86a20)


9. Running Automated Tests with pytest Run the tests using the following command:
   pytest todo_tests.py

10. Generate Test Report in HTML Format To create an HTML report for the test results, use:
    python -m pytest todo_tests.py --html=report.html

11. View the HTML Test Report Open the report.html file in a web browser to see the detailed test results.
      ![image](https://github.com/user-attachments/assets/30020f94-d835-49a5-aca7-380972bed330)
