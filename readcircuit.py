#Quirk stores circuits as json in the page element, so we will use selenium to grab the url's html
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.action_chains import ActionChains
#tkinter is weirdly useful for reading the clipboard.
import tkinter as tk


print('Hand over the link:')
x = input()
print("thanks") 


#Get webdriver and then open the link (that will be given by the user)
driver = webdriver.Firefox()
driver.get(x)

#Click the export button so you can then click the copy button
expbutton = driver.find_element(value="export-button")
expbutton.click()
copybutton = driver.find_element(value="export-json-copy-button")
copybutton.click()
root = tk.Tk()
root.withdraw()  # to hide the window
variable = root.clipboard_get()
print(variable)
