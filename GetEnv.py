#! /usr/bin/env python3


def getValueOfVar(varName: str):
    try:
        lines = open(".env", "r").readlines()
        for line in lines:
            line = line.strip()
            keys = line.split('=')
            if len(keys) != 2:
                continue
            if keys[0] == varName:
                return keys[1]
        return None
    except Exception as error:
        print("ERROR: " + str(error))
        return None
