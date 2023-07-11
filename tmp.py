def cleaning_up_special_characters(name):
    error = None
    max_length = 255
    special_char_removed_name = ''.join(c for c in name if c.isalnum() or c == '_')
    shortened_name = special_char_removed_name.replace(" ", "_")[:max_length]
    if len(name) != len(shortened_name):
        error = "Maximum characters exceeded"
    elif '_' not in shortened_name:
        error = "Special characters found"
    return shortened_name, error


def cleaning_up_special_characters(name):
    error = None
    max_length = 255
    cleaned_name = name.replace(" ", "_")
    special_char_removed_name = ''.join(c for c in cleaned_name if c.isalnum() or c == '_')
    shortened_name = special_char_removed_name[:max_length]
    if len(cleaned_name) != len(shortened_name):
        error = "Maximum characters exceeded"
    elif '_' not in shortened_name:
        error = "Special characters found"
    return shortened_name, error

