import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

@pytest.fixture(scope="module")
def driver():
    driver = webdriver.Chrome()
    driver.get('file:///C:/Users/abhij/stqa/todo_list/index.html')
    yield driver
    driver.quit()

def test_add_task(driver):
    task_input = driver.find_element(By.ID, 'taskInput')
    task_input.send_keys('Test Task 1')
    driver.find_element(By.XPATH, '//button[text()="Add Task"]').click()
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//li[contains(text(), 'Test Task 1')]"))
    )
    task_list = driver.find_element(By.ID, 'taskList')
    assert 'Test Task 1' in task_list.text, "Task was not added successfully."





def test_mark_task_as_completed(driver):
    task_item = driver.find_element(By.XPATH, "//li[contains(text(), 'Test Task 1')]")
    task_item.click()
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//li[contains(@class, 'completed')]"))
    )
    assert 'completed' in task_item.get_attribute('class'), "Task was not marked as completed."

def test_delete_task(driver):
    delete_button = driver.find_element(By.XPATH, "//li[contains(text(), 'Test Task 1')]//button[text()='Delete']")
    delete_button.click()
    WebDriverWait(driver, 10).until(
        EC.invisibility_of_element_located((By.XPATH, "//li[contains(text(), 'Test Task 1')]"))
    )
    task_list = driver.find_element(By.ID, 'taskList')
    assert 'Test Task 1' not in task_list.text, "Task was not deleted successfully."