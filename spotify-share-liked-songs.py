#! /usr/bin/env python3

from Prints import printIntroduction
from Prints import printConclusion
from Inputs import enterLogin
from Inputs import enterPassword


printIntroduction()
login = enterLogin()
password = enterPassword()
print("Login entered: " + login)
print("Password entered: " + password)
printConclusion()
