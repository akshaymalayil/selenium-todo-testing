import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class TodoAppTests(unittest.TestCase):

    def setUp(self):
        self.driver = webdriver.Chrome()
        self.driver.get("file:///C:/Users/abhij/stqa/index.html")

#updated
    def test_add_task(self):
        input_field = self.driver.find_element(By.ID, "new-todo")
        input_field.send_keys("Test Task")

        add_button = self.driver.find_element(By.XPATH, "//button[text()='Add Task']")
        add_button.click()

        # Wait for the task to be added to the list
        WebDriverWait(self.driver, 20).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "#todo-list li"))
        )

        tasks = self.driver.find_elements(By.CSS_SELECTOR, "#todo-list li")
        self.assertEqual(len(tasks), 1)
        self.assertEqual(tasks[0].text.strip(), "Test Task")


    def test_delete_task(self):
        input_field = self.driver.find_element(By.ID, "new-todo")
        input_field.send_keys("Task to Delete")
        input_field.send_keys(Keys.RETURN)

        # Wait for the task to be added to the list
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "#todo-list li"))
        )

        delete_button = self.driver.find_element(By.CSS_SELECTOR, ".delete-btn")
        delete_button.click()

        # Wait for the task to be removed from the list
        WebDriverWait(self.driver, 10).until(
            EC.invisibility_of_element_located((By.CSS_SELECTOR, "#todo-list li"))
        )

        tasks = self.driver.find_elements(By.CSS_SELECTOR, "#todo-list li")
        self.assertEqual(len(tasks), 0)

    def test_empty_task(self):
        input_field = self.driver.find_element(By.ID, "new-todo")
        input_field.send_keys("")
        input_field.send_keys(Keys.RETURN)
        tasks = self.driver.find_elements(By.CSS_SELECTOR, "#todo-list li")
        self.assertEqual(len(tasks), 0)

    def test_long_task(self):
        long_task = "This is a very long task " * 10
        input_field = self.driver.find_element(By.ID, "new-todo")
        input_field.send_keys(long_task)
        input_field.send_keys(Keys.RETURN)

        # Wait for the long task to be added to the list
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "#todo-list li"))
        )

        task = self.driver.find_element(By.CSS_SELECTOR, "#todo-list li")
        self.assertTrue(long_task in task.text)

    def test_multiple_tasks(self):
        input_field = self.driver.find_element(By.ID, "new-todo")
        for i in range(50):
            input_field.send_keys(f"Task {i}")
            input_field.send_keys(Keys.RETURN)

        # Wait for all tasks to be added to the list
        WebDriverWait(self.driver, 10).until(
            lambda driver: len(driver.find_elements(By.CSS_SELECTOR, "#todo-list li")) == 50
        )

        tasks = self.driver.find_elements(By.CSS_SELECTOR, "#todo-list li")
        self.assertEqual(len(tasks), 50)

    def tearDown(self):
        self.driver.quit()

if __name__ == "__main__":
    unittest.main()
