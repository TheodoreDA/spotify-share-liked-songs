#! /usr/bin/env python3

def enterLogin():
    while 1:
        login = input("Please enter your Spotify login: ")
        if login != "":
            break
    return login


def enterPassword():
    while 1:
        password = input("Please enter your Spotify password: ")
        if password != "":
            break
    return password
