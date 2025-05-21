import spacy
import sys
import re
from timeit import default_timer as timer

# start timing code execution
start = timer()

# Load the most accurate/powerful spaCy model (English transformer pipeline)
nlp = spacy.load('en_core_web_trf')

# Input file 
input_file = sys.argv[1]

# If the output file has not been specified the default name will be the name of the input file with the file ending vrt
if len(sys.argv) < 3:
    output_file = "{}.vrt".format(sys.argv[1])
else: 
    output_file = sys.argv[2]


# Function to process non-XML text using spaCy
def tag_tokens(text):
    doc = nlp(text)
    return ''.join(
        [token.text + "\t" + token.tag_ + "\t" + token.pos_ + "\t" + token.lemma_.lower() + "\n" for token in doc if not token.is_space]
    )

""" 
spacy will print each token, the corresponding Penn Treebank tag (tag_),
the Universal Dependencies tag (pos_) and
the lemma (lemma_) in all lowercase letters for everything that is not whitespace
on a new line 
"""

print("Lemmatizing...")


# Read the input file
with open(input_file, "r", encoding="utf-8") as f:
    content = f.read()


# Pattern to split XML tags and non-tags
# Group 1: XML tags; Group 2: non-tag text
parts = re.findall(r'(<[^>]+>)|([^<]+)', content)

with open(output_file, "w", encoding="utf-8") as out:
    for tag, text in parts:
        if tag:
            # It's an XML tag — write it unchanged
            out.write(tag + "\n")
        elif text:
            # It's text content — lemmatize, clean and write
            tagged = tag_tokens(text)
            out.write(tagged)


print(f"Lemmatized text written to '{output_file}'.")

# end timing code execution
end = timer()

# calculate execution time and convert to minutes
exec_time = (end - start)/60

print("Code executed in " + str(round(exec_time, 2)) + " minutes.")