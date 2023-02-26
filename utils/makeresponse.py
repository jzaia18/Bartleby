import openai

SECRET_KEY_LOCATION = 'secrets.txt'

with open(SECRET_KEY_LOCATION) as f:
    openai.api_key = f.read().strip()


def get_gpt_response(prompt, persona='Joe Rogan'):
    response = openai.Completion.create(
        model="text-curie-001",
        prompt=f'Answer as if you were {persona}, but your name is Bartleby and you are a gnome: {prompt}',
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
def get_moderated_text(response):
    text = get_response_text(response)

    print(text)

    response = openai.Moderation.create(
        input=text
    )
    output = response["results"][0]

    print(output)
    return output

if __name__ == '__main__':
    r = get_gpt_response(input())

    print(get_text_from(r))
    #print(get_moderated_text(r))
