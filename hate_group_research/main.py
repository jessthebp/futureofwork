# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


def get_builtwith_data(url):
    import urllib.request, json
    from urllib.request import Request, urlopen
    request_url = Request("https://api.builtwith.com/free1/api.json?KEY=e24f2bc8-f0b5-439e-9155-f438d71a5701&LOOKUP={domaininput}".format(domaininput=url))
    money_request_url = Request("https://api.builtwith.com/v20/api.json?KEY=e24f2bc8-f0b5-439e-9155-f438d71a5701&LOOKUP={domaininput}".format(domaininput=url))
    # request_url = "https://api.builtwith.com/free1/api.json?KEY=e24f2bc8-f0b5-439e-9155-f438d71a5701&LOOKUP={domaininput}".format(domaininput)
    # response_body = urlopen(request_url).read()
    # print(response_body)
    print(money_request_url)
    with urllib.request.urlopen(money_request_url) as request:
        data = json.load(request)
        print(data)

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print_hi('PyCharm')
    # get url from console
    input_url = input("Enter a url: ")
    get_builtwith_data(input_url)

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
