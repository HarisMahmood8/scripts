def cleaning_up_special_characters(name):
    error = None
    # removes special characters and spaces, replaces spaces with underscore
    max_length = 255
    cleaned_name = name.replace(" ", "_")
    special_char_removed_name = ''.join(c for c in cleaned_name if c.isalnum() or c == '_')
    shortened_name = special_char_removed_name[:max_length]
    if cleaned_name != shortened_name:
        if len(shortened_name) < len(special_char_removed_name):
            error = "Maximum characters exceeded"
        elif len(special_char_removed_name) < len(cleaned_name):
            error = "Special characters found"
    return shortened_name, error
