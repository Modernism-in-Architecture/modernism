import re


_end_of_truncating_line = '</p>\r\n'
_new_line_chars = '\r\n'
_nbsp_space = '&nbsp;'


def truncate_leading_trailing_spaces_from_wysiwyg_text(init_str):
    init_str = _truncate_leading_spaces(init_str)
    init_str = _truncate_trailing_spaces(init_str)
    return init_str


def _truncate_leading_spaces(init_str):
    # Check <p>, remove it and then add it in the end
    if not init_str.startswith('<p>'):
        return init_str
    init_str = re.sub(fr"^{re.escape('<p>')}", '', init_str).strip()
    # Remove nbsp-spaces
    while init_str.startswith(_nbsp_space):
        init_str = re.sub(fr"^{re.escape(_nbsp_space)}", '', init_str).strip()
    # Check that we have reached the end of the line
    if init_str.startswith(_end_of_truncating_line):
        # Remove new line chars and go to check next line
        init_str = re.sub(fr"^{re.escape(_end_of_truncating_line)}", '', init_str)
        # Spaces can be on multiple lines
        init_str = _truncate_leading_spaces(init_str)
        return init_str
    # Add removed <p>
    init_str = '<p>' + init_str
    return init_str.strip()


def _truncate_trailing_spaces(init_str):
    # Check </p>, remove it and then add it in the end
    if not init_str.endswith('</p>'):
        return init_str
    init_str = re.sub(fr"{re.escape('</p>')}$", '', init_str).strip()
    # Remove nbsp-spaces
    while init_str.endswith(_nbsp_space):
        init_str = re.sub(fr"{re.escape(_nbsp_space)}$", '', init_str).strip()
    # Check that we have reached the beginning of the line
    if init_str.endswith('<p>'):
        # Remove tag of new line because we move from end to start of the line
        init_str = re.sub(fr"{re.escape('<p>')}$", '', init_str)
        # Remove new line chars and go to check previous line
        init_str = re.sub(fr"{re.escape(_new_line_chars)}$", '', init_str)
        # Spaces can be on multiple lines
        init_str = _truncate_trailing_spaces(init_str)
        return init_str
    # Add removed </p>
    init_str = init_str + '</p>'
    return init_str



