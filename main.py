# import all used modules
import os
import sys
import nltk
import PyPDF2
import openai

# download the punkt tokenizer
nltk.download('punkt')


# Read pdf all pages from path via pypdf2 and return the text
def read_pdf(path):
    pdfFileObj = open(path, 'rb')
    pdfReader = PyPDF2.PdfReader(pdfFileObj)
    text = ''
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
        if chunk_size + len(sentence) < 1000:
            chunk.append(sentence)
            chunk_size += len(sentence)
        else:
            yield chunk
            chunk = [sentence]
            chunk_size = len(sentence)
    yield chunk

# send the chunk to the chatgpt via openai api package
def send_to_chatgpt(chunk):
    # get the api key from the environment variable
    openai.api_key = os.environ.get("GPT_KEY")

    response = openai.Completion.create(
        engine="davinci",
        prompt=chunk,
        temperature=0.9,
        max_tokens=150,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0.6,
        stop=["\n", " Human:", " AI:"]
    )
    return response


# main function
def main():
    # read the pdf file
    text = read_pdf(sys.argv[1])

    # cut the text into sentences
    sentences = cut_into_sentences(text)

    # combine the sentences into chunks
    chunks = combine_sentences(sentences)

    # send the chunks to chatgpt
    for chunk in chunks:
        response = send_to_chatgpt(chunk)
        print(response['choices'][0]['text'])


if __name__ == '__main__':
    main()

