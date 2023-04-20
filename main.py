# import all used modules
import os
import sys
import nltk
import PyPDF2
import openai
import time
import json
import requests

# download the punkt tokenizer
nltk.download("punkt")


# Read pdf all pages from path via pypdf2 and return the text
def read_pdf(path):
    pdfFileObj = open(path, "rb")
    pdfReader = PyPDF2.PdfReader(pdfFileObj)
    text = ""
    for page in range(len(pdfReader.pages)):
        pageObj = pdfReader.pages[page]
        text += pageObj.extract_text()
    return text


# and cut the file into sentences
def cut_into_sentences(text):
    return nltk.sent_tokenize(text)


# combine the sentences into a paragraph chunk less than 1000 words and return it in list form
def combine_sentences(sentences):
    chunk = []
    chunk_size = 0
    for sentence in sentences:
        # trim all the dot from the sentence
        sentence = sentence.replace(".", "")
        sentence = sentence.replace("\n", "")

        if chunk_size + len(sentence) < 3000:
            chunk.append(sentence)
            chunk_size += len(sentence)
        else:
            yield chunk
            chunk = [sentence]
            chunk_size = len(sentence)
    yield chunk


def reformat_messages(original_list, role="user"):
    messages = {"role": role, "content": original_list}
    return messages

def reformat_messages(original_list, role="user"):
    messages = []

    for text in original_list:
        messages.append({"role": role, "content": text})
    return messages


# send the chunk to the chatgpt via openai api package
def send_to_chatgpt(messages):
    # get the api key from the environment variable
    openai.api_key = os.environ.get("GPT_KEY")

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages,
        temperature=0.9,
        max_tokens=150,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0.6,
    )

    return response['choices'][0]['message']


def generate_response(prompt):
    # set up the request headers and data
    API_KEY = os.environ.get("GPT_KEY")

    headers = {
        'Content-Type': 'application/json',
        'Authorization': f"{API_KEY}"
    }
    data = {
        'prompt': prompt,
        'temperature': 0.7,
        'max_tokens': 2000,
    }

    # send the request to the GPT API
    response = requests.post('https://api.openai.com/v1/chat/completions', headers=headers, data=json.dumps(data))

    # check for errors in the API response
    if 'choices' not in response.json():
        return "Sorry, I couldn't generate a response for that prompt."

    # parse the response from the API and return the generated text
    response_text = response.json()['choices'][0]['text']
    return response_text


# insert prompt before real content
def add_prompt_before_chunks(chunks):
    prompt = ['You are a helpful assistant to help answer questions. Read content first, before I send "end reading", continue read text and only reply "noted"']
    messages = reformat_messages(prompt, role="system")

    chunks.insert(0, messages)
    return chunks


# insert prompt after real content
def add_prompt_after_chunks(chunks):
    prompt = ["end reading"]
    messages = reformat_messages(prompt)

    chunks.append(messages)
    return chunks


# main function
def main():
    # read the pdf file
    print(sys.argv[1])
    text = read_pdf(sys.argv[1])

    # cut the text into sentences
    sentences = cut_into_sentences(text)

    # combine the sentences into chunks
    chunks = combine_sentences(sentences)

    chunk_list = [x for x in chunks]
    chunk_list = [reformat_messages(x) for x in chunk_list]
    chunk_list = chunk_list[:6]
    chunk_list = add_prompt_before_chunks(chunk_list)
    chunk_list = add_prompt_after_chunks(chunk_list)

    # send the chunks to chatgpt
    for i, chunk in enumerate(chunk_list):
        response = send_to_chatgpt(chunk)

        print(i)
        print(response)

        if i%3 == 0:
            time.sleep(60)


if __name__ == "__main__":
    main()


