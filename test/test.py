# import function from main.py
from main import read_pdf, cut_into_sentences, combine_sentences, send_to_chatgpt

# test read_pdf
text = read_pdf('./files/jpm-4q22-earnings-call-final-transcript.pdf')

# test cut_into_sentences
sentences = cut_into_sentences(text)

print(sentences[1])