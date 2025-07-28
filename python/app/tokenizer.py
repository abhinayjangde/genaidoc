import tiktoken
tokenizer = tiktoken.encoding_for_model("gpt-4")
text = "WTF is an LLM?"
tokenized_words = tokenizer.encode(text)
print(tokenized_words)

# output = [100264, 9125, 100266, 2675, 527, 264, 11190, 18328, 100265, 100264, 882, 100266, 54, 9112, 374, 459, 445, 11237, 30, 100265, 100264, 78191, 100266]
