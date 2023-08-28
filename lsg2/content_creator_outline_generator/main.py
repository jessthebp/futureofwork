import argparse
import os

# users can input: pagetype, surferseo or clearscope keywords, keyword, brand
# output: a dictionary outline of the page

def get_args():
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('--pagetype', type=str, help='pagetype')
    parser.add_argument('--keyword', type=str, help='keyword')
    parser.add_argument('--brand', type=str, help='brand')
    parser.add_argument('--locations', type=str, help='locations',nargs='+')
    parser.add_argument('--secondarykws', type=str, help='surferseo keywords',nargs='+')
    args = parser.parse_args()
    return args


import re

def extract_data(input_str):
    # Split by newline or comma
    input_list = re.split(r'\n|, |,', input_str)
    print(input_list)
    # Regular expression to match keyword and number
    text_pattern = re.compile(r'([A-Za-z]+?.+)')
    number_pattern = re.compile(r'(\d+)(?:/(\d+)(?:-\d+)?)?')

    result = {}
    i = 0
    while i < len(input_list) - 1:
        text_match = text_pattern.match(input_list[i])
        number_match = number_pattern.match(input_list[i+1])

        if text_match and number_match:
            keyword = input_list[i].strip()
            if number_match.group(2):  # If there's a number after the slash
                number = int(number_match.group(2))
            else:
                number = int(number_match.group(1))
            result[keyword] = number
            i += 2
        else:
            i += 1

    return result

# Test
input_str1 = '''electric cars for sale
4/2–6
electric cars
28/7–22
electric vehicles
1/4–19
heated steering wheel
0/2–6
electric car
26/1–6'''

input_str2 = 'electric cars for sale, 4/2–6, electric cars, 28/7–22, electric vehicles,1/4–19, heated steering wheel, 0/2–6, electric car, 26/1–6'


def main():
    args = get_args()
    print(args)
    print(args.pagetype)
    # print(args.surferseo)
    # print(args.clearscope)
    print(args.keyword)
    print(args.brand)
    from api_use import outline_generator
    from api_use import get_site_content
    from api_use import ContentAssistant
    new_prompt = "What are some questions someone searching for the term {primary_kw}  might have? What are specific issues someone might have to do with {primary_kw}?"
    keyword_list = extract_data(str(args.secondarykws))
    # Instantiate the class with your OpenAI API key
    api_key = os.getenv("OPENAI_API_KEY")
    print(api_key)
    content_assistant = ContentAssistant(api_key)

    brand, primary_kw = args.brand, args.keyword

    messages, response = content_assistant.get_answer(new_prompt,  brand, primary_kw, keyword_list, length=800, temp=0,)


    messages, response = content_assistant.continue_conversation(messages, response, brand, primary_kw, keyword_list, length=1500, temp=0 )
    print(messages, response)
    # messages, response = localize_content(messages, response, brand, primary_kw, keyword_list, location,  length=500, temp=0)

    # save final response to file
    with open(f'/output/{primary_kw}output.txt', 'w') as f:
        f.write(str(response['content']))
        f.close()


if __name__ == '__main__':
    main()