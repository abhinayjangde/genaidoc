import tiktoken

encoder = tiktoken.encoding_for_model("gpt-4")

vocab_size = encoder.n_vocab

print("vocab size :", vocab_size)

text = "I am genai developer"

tokens = encoder.encode(text) # [40, 939, 3645, 1361, 24261]

print("Number of tokens: ", len(tokens))
print("tokens: ", tokens)

print(encoder.decode([40, 939, 3645, 1361, 24261]))