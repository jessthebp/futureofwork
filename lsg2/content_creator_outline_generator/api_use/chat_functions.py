import openai
import os

openai.api_key = os.getenv("OPENAI_API_KEY")
class ContentAssistant:
    def __init__(self, api_key):
        self.api_key = api_key
        openai.api_key = os.getenv("OPENAI_API_KEY")

    def get_answer(self, new_prompt, brand="", primary_kw="", keyword_list="", length=1500, temp=0):
        messages = [
            {
                "role": "user",
                "content": f"What are some questions someone searching for the term {primary_kw} might have? What are specific issues someone might have to do with {primary_kw}?"
            },
            {
                "role": "user",
                "content": f"{keyword_list}"
            },
            {
                "role": "user",
                "content": f"primary_kw: {primary_kw}"
            },
            {
                "role": "user",
                "content": f"What is the intent of a user searching for this keyword? What are secondary intents? What are the aspects of a good page that would cover these intents? What content on {brand} would cover these intents?"
            }
        ]

        response = self._create_chat_response(messages, length, temp)
        return messages, response.choices[0].message

    def continue_conversation(self, messages, response, brand="", primary_kw="", keyword_list="", length=1500, temp=0):
        response_content = self._sanitize_content(response["content"])

        response1 = {
            "role": "assistant",
            "content": response_content
        }

        response2 = {
            "role": "user",
            "content": f"Write an outline about this subject in a python dictionary format with the key name being the head and the item as notes about the content. example of the format: {{'{primary_kw}: what you need to know': {{'content': 'introduction to the content and quick access to important info', 'keywords': 'needs to include keywords x, y, z, a, b, c'}}, 'our process': {{'content':'this is about our process', 'keywords':...etc'}}}} Brand is for {brand}. Keep in mind the questions and intent we discussed above: solve the main intent as soon as possible. Include at least 5 parts. Include an FAQ with questions/answers. Include where different specific keywords listed previously (in the keywords list) would be put in as part of the content. Focus first on user intent."
        }

        response2["content"] = response2["content"].replace("{brand}", brand)
        response2["content"] = response2["content"].replace("{primary_kw}", primary_kw)

        messages.append(response1)
        messages.append(response2)

        if type(messages) != list:
            messages = [messages]

        response = self._create_chat_response(messages, length, temp)
        return messages, response.choices[0].message

    def localize_content(self, messages, response, brand="", primary_kw="", keyword_list="", location="", length=500,
                         temp=0):
        response_content = self._sanitize_content(response["content"])
        previous_response = response_content

        previous_response = previous_response.to_dict()
        num_values = len(previous_response)
        last_value = previous_response["content"]

        messages.append(previous_response)

        localtext = {
            "role": "user",
            "content": f"If someone was searching from this specific location {location} what sections would you add to this outline? Add two segments to this outline and return it. Focus first on user intent for the primary keyword and location."
        }
        localtext["content"] = localtext["content"].replace("{location}", location)
        messages.append(localtext)

        response = self._create_chat_response(messages, length, temp)
        return messages, response.choices[0].message

    def _create_chat_response(self, messages, length, temp):
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=messages,
            temperature=temp,
            max_tokens=length,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0
        )
        return response

    def _sanitize_content(self, content):
        return str(content).replace("{", "\\{").replace("}", "\\}").replace("$", "\\$").replace("[", "\\[").replace("]",
                                                                                                                    "\\]").replace(
            "(", "\\(").replace(")", "\\)").replace("?", "\\?").replace("*", "\\*").replace("+", "\\+").replace("|",
                                                                                                                "\\|").replace(
            "^", "\\^").replace(".", "\\.").replace("!", "\\!").replace("-", "\\-").replace(":", "\\:").replace(";",
                                                                                                                "\\;").replace(
            "/", "\\/").replace("#", "\\#").replace("@", "\\@")
