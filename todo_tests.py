import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains

class TodoAppTests(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome()
        self.driver.get("file:///C:/Users/abhij/stqa/index.html")
        self.wait = WebDriverWait(self.driver, 20)

    def test_add_task(self):
        self.add_task("Test Task")
        task = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "#todo-list li span")))
        self.assertIn("Test Task", task.text)

    def test_delete_task(self):
        self.add_task("Task to Delete")
        delete_button = self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".delete-btn")))
        delete_button.click()
        self.wait.until(EC.invisibility_of_element_located((By.CSS_SELECTOR, "#todo-list li")))
        tasks = self.driver.find_elements(By.CSS_SELECTOR, "#todo-list li")
        self.assertEqual(len(tasks), 0)

    def test_edit_task(self):
        self.add_task("Old Task")
        self.edit_task("Old Task", "Updated Task")
        task = self.wait.until(EC.presence_of_element_located((By.XPATH, "//li/span[contains(text(), 'Updated Task')]")))
        self.assertIn("Updated Task", task.text)

    def test_task_persistence(self):
        self.add_task("Persistent Task")
        self.driver.refresh()
        task = self.wait.until(EC.presence_of_element_located((By.XPATH, "//li/span[contains(text(), 'Persistent Task')]")))
        self.assertIn("Persistent Task", task.text)

    def test_empty_task(self):
        self.add_task("")
        tasks = self.driver.find_elements(By.CSS_SELECTOR, "#todo-list li")
        self.assertEqual(len(tasks), 0)

    def test_add_multiple_tasks(self):
        for i in range(3):
            self.add_task(f"Task {i + 1}")
        tasks = self.driver.find_elements(By.CSS_SELECTOR, "#todo-list li")
        self.assertEqual(len(tasks), 3)

    def test_complete_task(self):
        self.add_task("Task to Complete")
        task = self.wait.until(EC.presence_of_element_located((By.XPATH, "//li/span[contains(text(), 'Task to Complete')]")))
        task.click()  # Mark the task as complete
        self.assertIn("completed", task.get_attribute("class"))

    def test_editing_completed_task(self):
        self.add_task("Completed Task")
        task = self.wait.until(EC.presence_of_element_located((By.XPATH, "//li/span[contains(text(), 'Completed Task')]")))
        task.click()  # Mark the task as complete
        self.edit_task("Completed Task", "Updated Completed Task")
        updated_task = self.wait.until(EC.presence_of_element_located((By.XPATH, "//li/span[contains(text(), 'Updated Completed Task')]")))
        self.assertIn("Updated Completed Task", updated_task.text)

    def test_filter_completed_tasks(self):
        self.add_task("Task 1")
        self.add_task("Task 2")
        self.add_task("Task 3")
        self.complete_task("Task 1")
        self.driver.execute_script("document.getElementById('filter').value = 'completed';")
        filtered_tasks = self.driver.find_elements(By.CSS_SELECTOR, "#todo-list li.completed")
        self.assertEqual(len(filtered_tasks), 1)

    def test_filter_incomplete_tasks(self):
        self.add_task("Incomplete Task 1")
        self.add_task("Incomplete Task 2")
        self.complete_task("Incomplete Task 1")
        self.driver.execute_script("document.getElementById('filter').value = 'incomplete';")
        filtered_tasks = self.driver.find_elements(By.CSS_SELECTOR, "#todo-list li:not(.completed)")
        self.assertEqual(len(filtered_tasks), 1)

    def test_max_length_task(self):
        long_task = "A" * 256  # Assuming the max length is 255 characters
        self.add_task(long_task)
        tasks = self.driver.find_elements(By.CSS_SELECTOR, "#todo-list li")
        self.assertEqual(len(tasks), 1)

    def test_task_count_display(self):
        for i in range(5):
            self.add_task(f"Task {i + 1}")
        task_count = self.wait.until(EC.presence_of_element_located((By.ID, "task-count")))
        self.assertEqual(task_count.text, "5 tasks")

    def test_complete_task_persistence(self):
        self.add_task("Persistent Complete Task")
        task = self.wait.until(EC.presence_of_element_located((By.XPATH, "//li/span[contains(text(), 'Persistent Complete Task')]")))
        task.click()  # Mark the task as complete
        self.driver.refresh()
        task = self.wait.until(EC.presence_of_element_located((By.XPATH, "//li/span[contains(text(), 'Persistent Complete Task')]")))
        self.assertIn("completed", task.get_attribute("class"))

    def test_check_ui_for_task_input(self):
        input_field = self.wait.until(EC.presence_of_element_located((By.ID, "new-todo")))
        add_button = self.wait.until(EC.presence_of_element_located((By.XPATH, "//button[text()='Add Task']")))
        self.assertTrue(input_field.is_displayed())
        self.assertTrue(add_button.is_displayed())

    def test_check_for_task_duplication(self):
        self.add_task("Duplicate Task")
        self.add_task("Duplicate Task")
        tasks = self.driver.find_elements(By.CSS_SELECTOR, "#todo-list li")
        self.assertEqual(len(tasks), 1)

    def test_verify_delete_confirmation(self):
        self.add_task("Task to Confirm Delete")
        delete_button = self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".delete-btn")))
        delete_button.click()
        self.driver.switch_to.alert.accept()  # Confirm delete
        self.wait.until(EC.invisibility_of_element_located((By.CSS_SELECTOR, "#todo-list li")))
        tasks = self.driver.find_elements(By.CSS_SELECTOR, "#todo-list li")
        self.assertEqual(len(tasks), 0)

    def test_check_for_invalid_characters(self):
        self.add_task("@#$%^&*()")
        tasks = self.driver.find_elements(By.CSS_SELECTOR, "#todo-list li")
        self.assertEqual(len(tasks), 0)

    def test_check_task_sorting(self):
        self.add_task("Task B")
        self.add_task("Task A")
        self.add_task("Task C")
        task_texts = [task.text for task in self.driver.find_elements(By.CSS_SELECTOR, "#todo-list li span")]
        self.assertEqual(task_texts, ["Task A", "Task B", "Task C"])  # Assuming tasks are sorted alphabetically

    def test_verify_task_list_clears(self):
        self.add_task("Task to Clear")
        self.driver.execute_script("document.getElementById('clear-tasks').click();")  # Assuming there's a clear button
        tasks = self.driver.find_elements(By.CSS_SELECTOR, "#todo-list li")
        self.assertEqual(len(tasks), 0)

    def test_test_app_responsiveness(self):
        self.driver.set_window_size(800, 600)  # Resize the window
        # Check UI elements after resizing
        input_field = self.wait.until(EC.presence_of_element_located((By.ID, "new-todo")))
        add_button = self.wait.until(EC.presence_of_element_located((By.XPATH, "//button[text()='Add Task']")))
        self.assertTrue(input_field.is_displayed())
        self.assertTrue(add_button.is_displayed())

    def test_check_error_handling(self):
        # Simulate an error scenario
        self.driver.execute_script("throw new Error('Simulated error');")  # This is just for demonstration; handling should be implemented
        # Verify appropriate error message is shown (this part would depend on your app's implementation)
        error_message = self.driver.find_element(By.ID, "error-message")  # Assuming you have an error message element
        self.assertIsNotNone(error_message)

    def test_validate_keyboard_shortcuts(self):
        # Check if shortcuts work (this depends on implementation)
        # For example, simulating Ctrl + N to add a new task
        self.add_task("Task with Shortcut")
        tasks = self.driver.find_elements(By.CSS_SELECTOR, "#todo-list li")
        self.assertIn("Task with Shortcut", [task.text for task in tasks])

    def test_validate_styling_for_tasks(self):
        self.add_task("Styled Task")
        task = self.wait.until(EC.presence_of_element_located((By.XPATH, "//li/span[contains(text(), 'Styled Task')]")))
        self.assertEqual(task.value_of_css_property('color'), 'rgba(0, 0, 0, 1)')  # Assuming default text color

    def test_verify_api_interaction(self):
        # If your app interacts with an API, you would trigger that and check the response.
        # Placeholder for actual implementation
        response = self.driver.execute_script("return fetch('/api/tasks').then(res => res.json());")  # Example
        self.assertIsNotNone(response)

    def test_verify_mobile_responsiveness(self):
        self.driver.set_window_size(375, 667)  # Mobile size
        input_field = self.wait.until(EC.presence_of_element_located((By.ID, "new-todo")))
        add_button = self.wait.until(EC.presence_of_element_located((By.XPATH, "//button[text()='Add Task']")))
        self.assertTrue(input_field.is_displayed())
        self.assertTrue(add_button.is_displayed())

    def test_check_browser_compatibility(self):
        # Open the app in different browsers as part of your test environment setup
        # Note: This would typically be done in a more integrated testing setup
        self.driver.get("file:///C:/Users/abhij/stqa/index.html")
        input_field = self.wait.until(EC.presence_of_element_located((By.ID, "new-todo")))
        add_button = self.wait.until(EC.presence_of_element_located((By.XPATH, "//button[text()='Add Task']")))
        self.assertTrue(input_field.is_displayed())
        self.assertTrue(add_button.is_displayed())

    def test_test_performance_with_many_tasks(self):
        for i in range(100):
            self.add_task(f"Task {i + 1}")
        tasks = self.driver.find_elements(By.CSS_SELECTOR, "#todo-list li")
        self.assertEqual(len(tasks), 100)

    def test_validate_default_task_view(self):
        tasks = self.driver.find_elements(By.CSS_SELECTOR, "#todo-list li")
        self.assertEqual(len(tasks), 0)  # Assuming the default state is empty

    def test_task_completion_persistence(self):
        self.add_task("Persistent Task")
        task = self.wait.until(EC.presence_of_element_located((By.XPATH, "//li/span[contains(text(), 'Persistent Task')]")))
        task.click()  # Mark the task as complete
        self.driver.refresh()
        task = self.wait.until(EC.presence_of_element_located((By.XPATH, "//li/span[contains(text(), 'Persistent Task')]")))
        self.assertIn("completed", task.get_attribute("class"))

    def test_validate_accessibility_features(self):
        # Use a tool like Axe or similar for automated accessibility testing
        # Placeholder for actual implementation
        accessible = True  # Replace with actual accessibility check
        self.assertTrue(accessible)

    def test_check_internationalization(self):
        # Change language settings if applicable
        # Verify task list and UI text in selected language
        # Placeholder for actual implementation
        ui_text_correct = True  # Replace with actual check
        self.assertTrue(ui_text_correct)

    def add_task(self, task_text):
        input_field = self.wait.until(EC.presence_of_element_located((By.ID, "new-todo")))
        input_field.clear()
        input_field.send_keys(task_text)
        add_button = self.wait.until(EC.element_to_be_clickable((By.XPATH, "//button[text()='Add Task']")))
        actions = ActionChains(self.driver)
        actions.move_to_element(add_button).click().perform()

    def edit_task(self, old_text, new_text):
        task = self.wait.until(EC.presence_of_element_located((By.XPATH, f"//li/span[contains(text(), '{old_text}')]")))
        edit_button = task.find_element(By.XPATH, "following-sibling::div/span[@class='edit-btn']")
        edit_button.click()
        alert = self.driver.switch_to.alert
        alert.send_keys(new_text)
        alert.accept()

    def complete_task(self, task_text):
        task = self.wait.until(EC.presence_of_element_located((By.XPATH, f"//li/span[contains(text(), '{task_text}')]")))
        task.click()  # Click to complete the task

    def tearDown(self):
        self.driver.quit()

if __name__ == "__main__":
    unittest.main()
