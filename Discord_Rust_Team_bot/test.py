str = "peter"

if "id-" in str:
    substring = str.split("id-")[1]

    print(substring)
else:
    print(str)