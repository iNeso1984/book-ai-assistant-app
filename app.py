import openai  # install opeinai in terminal using --> python setup.py install
import os
import gradio

# create .env file and set OPENAI_API_KEY to your key.
openai.api_key = os.getenv("OPENAI_API_KEY")

messages = [{"role": "system",
             "content": "You are an AI assistant that recommends the best book to read depending on the subject. You know about popular books, best-rated books, classical books, great works of literature from all genres. You can provide advise on what books to read and anything else related to books. You can use Google Books and Amazon as a resource or any other library related to books. Do not answer questions that are not related to books. If you are unable to provide an answer to a question, please respond with the phrase `I'm just a book-loving bot, I can't help with that.`Do not use any external URLs in your answer. Do not use hateful language, angry language, or profanity. Do not refer to any blogs in your answers."}]


def CustomChatGPT(user_input):
    messages.append({"role": "user", "content": user_input})
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages
    )
    ChatGPT_reply = response["choices"][0]["message"]["content"]
    messages.append({"role": "assistant", "content": ChatGPT_reply})
    return ChatGPT_reply
  
def get_moderation(question):
    """
    Check the question is safe to ask the model

    Parameters:
        question (str): The question to check

    Returns a list of errors if the question is not safe, otherwise returns None
    """

    errors = {
        "hate": "Content that expresses, incites, or promotes hate based on race, gender, ethnicity, religion, nationality, sexual orientation, disability status, or caste.",
        "hate/threatening": "Hateful content that also includes violence or serious harm towards the targeted group.",
        "self-harm": "Content that promotes, encourages, or depicts acts of self-harm, such as suicide, cutting, and eating disorders.",
        "sexual": "Content meant to arouse sexual excitement, such as the description of sexual activity, or that promotes sexual services (excluding sex education and wellness).",
        "sexual/minors": "Sexual content that includes an individual who is under 18 years old.",
        "violence": "Content that promotes or glorifies violence or celebrates the suffering or humiliation of others.",
        "violence/graphic": "Violent content that depicts death, violence, or serious physical injury in extreme graphic detail.",
    }
    response = openai.Moderation.create(input=question)
    if response.results[0].flagged:
        # get the categories that are flagged and generate a message
        result = [
            error
            for category, error in errors.items()
            if response.results[0].categories[category]
        ]
        return result
    return None



demo= gradio.Interface(fn=CustomChatGPT, inputs="text", outputs="text", title="Help Me Find a Good Book?")

demo.launch(debug=True,enable_queue=True)
