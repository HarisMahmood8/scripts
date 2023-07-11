def cleaning_up_special_characters(name):
    error = None
    max_length = 255
    cleaned_name = name.replace(" ", "_")
    special_char_removed_name = ''.join(c for c in cleaned_name if c.isalnum() or c == '_')
    shortened_name = special_char_removed_name[:max_length]
    if special_char_removed_name != cleaned_name:
        error = "Special characters found"
    elif len(cleaned_name) != len(shortened_name):
        error = "Maximum characters exceeded"
    return shortened_name, error

name = "Hello-123 @Test"
shortened_name, error = cleaning_up_special_characters(name)

print("Shortened Name:", shortened_name)
print("Error:", error)
