import openai
import os
import re
import json




'''What are some questions someone searching for the term {primary_kw}  might have? What are specific issues someone might have to do with {primary_kw}?'''

'''What is the intent of a user searching for this keyword? What are secondary intents? What are the aspects of a good page that would cover these intents?'''

'''Write an outline about this subject in a python dictionary format with the key name being the head and the item as notes about the content. example of the format: {{"{primary_kw}: what you need to know': {"content": "introduction to the content and quick access to important info", "keywords":" needs to include keywords x, y, z, a, b, c'}, "our process: {"content":"this is about our process", "keywords:...etc"}} Brand is for {brand}. Keep in mind the questions and intent we discussed above: solve the main intent as soon as possible. Include at least 5 parts. Include an FAQ with questions/answers.  Include where different specific keywords listed previously (in the keywords list) would be put in as part of the content. Focus first on user intent.'''

'''If someone was searching from this specific location {location} what sections would you add to this outline? What would you change? Write an outline about this subject in a python dictionary format with the key name being the head and the item as notes about the content. example of the format: {{"{primary_kw}: what you need to know': {"content": "introduction to the content and quick access to important info", "keywords":" needs to include keywords x, y, z, a, b, c'}, "our process: {"content":"this is about our process", "keywords:...etc"}} Brand is for {brand}. Keep in mind the questions and intent we discussed above: solve the main intent as soon as possible. Include at least 5 parts. Include an FAQ with questions/answers.  Include where different specific keywords listed previously (in the keywords list) would be put in as part of the content. Focus first on user intent for the primary keyword and location.'''


def get_answer(new_prompt,brand="", primary_kw="", keyword_list="", length=1500, temp=0,):
    messages = [
        {
            "role": "user",
            "content": f"What are some questions someone searching for the term {primary_kw}  might have? What are specific issues someone might have to do with {primary_kw}?"
        },
        {
            "role": "user",
            "content": f"{keyword_list}"
        }, {
            "role": "user",
            "content": f"primary_kw: {primary_kw}"
        },
        {
            "role": "user",
            "content": "What is the intent of a user searching for this keyword? What are secondary intents? What are the aspects of a good page that would cover these intents? What content on {brand} would cover these intents?"
        }
    ]
    # print messages type
    print(type(messages))
    openai.api_key = os.getenv("OPENAI_API_KEY")
    #openai.api_key = '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'

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages,
        temperature=1,
        max_tokens=1686,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )

    return messages, response.choices[0].message

def continue_conversation(messages, response, brand="", primary_kw="", keyword_list="", length=1500, temp=0 ):
    message = messages
    response1 ={
            "role": "assistant",
            "content": "${response}"
        }
    response2 = {
            "role": "user",
            "content": "Write an outline about this subject in a python dictionary format with the key name being the head and the item as notes about the content. example of the format:\\{\\{\"\{$primary_kw}: what you need to know': \\{\"content\": \"introduction to the content and quick access to important info\", \"keywords\":\" needs to include keywords x, y, z, a, b, c'\\}, \"our process: \\{\"content\":\"this is about our process\", \"keywords:...etc\"\\}\\} Brand is for ${brand}. Keep in mind the questions and intent we discussed above: solve the main intent as soon as possible. Include at least 5 parts. Include an FAQ with questions/answers.  Include where different specific keywords listed previously (in the keywords list) would be put in as part of the content. Focus first on user intent."
        }
    response_content = str(response["content"]).replace("{", "\\{").replace("}", "\\}").replace("$", "\\$").replace("[", "\\[").replace("]", "\\]").replace("(", "\\(").replace(")", "\\)").replace("?", "\?").replace("*", "\*").replace("+", "\+").replace("|", "\|").replace("^", "\^").replace(".", "\.").replace("!", "\!").replace("-", "\-").replace(":", "\:").replace(";", "\;").replace("/", "\/").replace("#", "\#").replace("@", "\@")
    response1["content"] = response1["content"].replace("${response}", response_content)
    response2["content"] = response2["content"].replace("${brand}", brand)
    response2["content"] = response2["content"].replace("${primary_kw}", primary_kw)

    # zip response1, response2 to messages
    messages.append(response1)
    print(type(messages))
    print("messages", messages)
    messages.append(response2)
    print(type(messages))
    # if message is not a list, make it a list
    if type(message) != list:
        messages = [message]
    # openai.api_key = os.getenv("OPENAI_API_KEY")
    openai.api_key = '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'
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages,
        temperature=1,
        max_tokens=2086,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )

    return messages, response.choices[0].message


def localize_content(messages, response,  brand="", primary_kw="", keyword_list="", location="", length=500, temp=0):
    previous_response = response

    print("messages type", type(messages))
    print(type(messages[0]))
    previous_response["content"] = str(previous_response["content"]).replace("{", "\\{").replace("}", "\\").replace(":","\\:")
    # previous_response = '\'' + previous_response + '\''
    print("previous response", type(previous_response))
    print("previous response", previous_response)
    # convert previous response to dict
    # my_openai_obj.to_dict()['message']['content']
    previous_response = previous_response.to_dict()
    print("previous response", type(previous_response))
    print("previous response dict", previous_response)
    # get number of values in dict
    num_values = len(previous_response)
    print("num values", num_values)
    # get last value in dict
    last_value = previous_response["content"]
    value = previous_response["role"]

    print("last value", last_value)
    print("last value type", type(last_value))
    print("value", value)
    print("value type", type(value))

    messages.append(previous_response)
    print("messages", messages)
    print("messages type", type(messages))
    localtext = {
        "role": "user",
        "content": "If someone was searching from this specific location ${location} what sections would you add to this outline? Add two segments to this outline and return it. Focus first on user intent for the primary keyword and location."
    }
    localtext["content"] = str(localtext["content"]).replace("${location}", location)
    messages = messages.append(localtext)
    print("messages", messages)
    print("messages type", type(messages))
    # openai.api_key = os.getenv("OPENAI_API_KEY")
    openai.api_key = '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'
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages,
        temperature=1,
        max_tokens=1686,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )

    return messages, response.choices[0].message


new_prompt = "What are some questions someone searching for the term {primary_kw}  might have? What are specific issues someone might have to do with {primary_kw}?"

keyword_list =  """{'cars for sale',
                'type',
                'color',
                'mileage',
                'used cars',
                'listings starting $',
                '4',
                'body type',
                'nhtsa overall safety',
                'make',
                'transmission',
                'engine',
                'exterior color',
                'body type',
                'overall safety rating',
                'model',
                'doors',
                'drivetrain',
                'model',
                'rating',
                'fuel type',
                'fuel type',
                'make',
                '4 doors',
                'transmission',
                'vin',
                'exterior color',
                'safety rating',
                '4 doors',
                'vin',
                'drivetrain',
                'mileage',
                'color',
                'safety rating',
                'used cars sale',
                'filters panel update',
                'buying power based',
                '– 30 61,706',
                'provided experian autocheck',
                'accidents title show',
                'know buying',
                'years price mileage',
                'location years price',
                'owner found damage',
                'damage totaled condition',
                'due warranty defects',
                'buying power',
                'subject autocheck terms',
                'vehicle number owners',
                'location years',
                'power based %',
                'condition history data',
                'defects vehicle stolen',
                'buying power est',
                'update search results',
                'autocheck . use',
                'owners fleet &',
                'leased business rather',
                'showing 1',
                'totaled condition automaker',
                "n't issues significant",
                'damage component main',
                'vehicles used rental',
                'capacity condition history'}"""

brand, primary_kw = "autonation", "cars for sale"

messages, response = get_answer(new_prompt,  brand, primary_kw, keyword_list, length=800, temp=0,)


messages, response = continue_conversation(messages, response, brand, primary_kw, keyword_list, length=1500, temp=0 )
print(messages, response)
# messages, response = localize_content(messages, response, brand, primary_kw, keyword_list, location,  length=500, temp=0)

# save final response to file
with open(f'{primary_kw}output.txt', 'w') as f:
    f.write(str(response['content']))
    f.close()
