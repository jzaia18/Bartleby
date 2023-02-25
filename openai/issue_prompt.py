import openai

SECRET_KEY_LOCATION = 'secrets.txt'

with open(SECRET_KEY_LOCATION) as f:
    openai.api_key = f.read().strip()


def get_gpt_response(prompt):
    response = openai.Completion.create(
        model="text-curie-001",
        prompt=prompt,
        temperature=0.9,
        max_tokens=250,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0.6,
    )

    return response

def get_response_text(response):
    return response['choices'][0]['text']

if __name__ == '__main__':
    r = get_gpt_response(input())

    print(get_response_text(r))
