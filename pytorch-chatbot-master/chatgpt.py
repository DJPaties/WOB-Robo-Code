from openai import OpenAI
# import os
client = OpenAI(
    api_key="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"
)
def chat(message):
    completion = client.chat.completions.create(
        # model="gpt-4",
        model="gpt-3.5-turbo",
        messages=[
        {"role": "system", "content": "You try to respond with short answer without sybmols."},
        {"role": "user", "content": message}
    ]
    )
    print(type(completion.choices[0].message.content))
    return {'gpt_response':completion.choices[0].message.content, 'intent':"conversation"}

# print(chat("ما هو المصطلح الذي يعبر عن فلسفة البوذية؟"))