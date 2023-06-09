import os
import sys

# import module from parent folder
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# import function from main.py
from main import read_pdf, cut_into_sentences, combine_sentences, send_to_chatgpt, add_prompt_before_chunks, add_prompt_after_chunks

# test read_pdf
text = read_pdf('./files/jpm-4q22-earnings-call-final-transcript.pdf')

# test cut_into_sentences
sentences = cut_into_sentences(text)
print(sentences[1])

# test combine_sentences, return a generator
chunks = combine_sentences(sentences)

# iterate through the generator chunks
# for chunk in chunks:
#     print(chunk)

chunk_list = [x for x in chunks]

chunk_list = add_prompt_before_chunks(chunk_list)
chunk_list = add_prompt_after_chunks(chunk_list)


print(len(chunk_list))
for chunk in chunk_list:
    print(chunk)
