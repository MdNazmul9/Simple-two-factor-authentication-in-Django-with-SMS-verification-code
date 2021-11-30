# importing the module
from easy_login import login

# initializing the username and password
username = ""
password = ""

# initializing the address of chrome web driver
address = ""

# creating an object of login
obj = login(username, password, addresses)

# calling the account in which we want to login
obj.Facebook()
obj.Instagram()
obj.Twitter()
obj.Linkedin()
obj.Reddit()
