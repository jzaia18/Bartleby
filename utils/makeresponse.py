import openai

SECRET_KEY_LOCATION = 'secrets.txt'

with open(SECRET_KEY_LOCATION) as f:
    openai.api_key = f.read().strip()


def get_gpt_response(prompt, persona='Joe Rogan', context=""):
    response = openai.Completion.create(
        model="text-davinci-003",
#         prompt=f"""
# Respond as a strongly opinionated rich gnome named Bartleby: "{prompt}"
# """ + (f"({str(context)})" if context else ""),
#         prompt=f"""
# Respond as a kind eccentric gnome named Bartleby: "{prompt}"
# """ + (f"({str(context)})" if context else ""),
        prompt=f"""
Respond as a kind feisty gnome named Bartleby: "{prompt}"
""" + (f"({str(context)})" if context else ""),
#         prompt=f"""
# Respond as a kind gnome named Bartleby, with some sass: "{prompt}"
# """ + (f"({str(context)})" if context else ""),
        temperature=0.9,
        max_tokens=250,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0.6,
    )

    return response

def get_text_from(response):
    return response['choices'][0]['text']

def get_gpt_response_text(prompt):
    return get_text_from(get_gpt_response(prompt))

#TODO, if we want to moderate responses
def get_moderated_text(prompt, *args, **kwargs):
    response = get_gpt_response(prompt, *args, **kwargs)
    
    text = get_text_from(response)

    moderation_data = openai.Moderation.create(
        input=text
    )

    moderation_data = moderation_data['results'][0]['categories']

    # If any flags, excluding violence, do not allow the text through
    if any([moderation_data[k] for k in moderation_data.keys() if 'violence' not in k]):
        return None

    return text

if __name__ == '__main__':
    r = get_gpt_response(input())

    print(get_text_from(r))
    #print(get_moderated_text(r))
