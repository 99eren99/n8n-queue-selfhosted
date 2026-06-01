from gguf import GGUFReader

# Path to your .gguf file
reader = GGUFReader("your.gguf")

#print(reader.fields.keys())

# Access metadata
metadata = reader.fields
template = metadata.get("tokenizer.chat_template")

if template:
    print(template.contents())
    # GGUF stores strings as byte arrays
    template_str = bytes(template.data).decode('utf-8')
    print(template_str)
else:
    print("No chat template found in this GGUF.")