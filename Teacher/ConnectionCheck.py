import urllib.request, urllib.error


def internet_on():
    try:
        urllib.request.urlopen("http://www.google.com", timeout=1)
        return True
    except urllib.error.URLError as e:
        return False


"""
if internet_on():
    print("Y")
else:
    print("N")
"""
