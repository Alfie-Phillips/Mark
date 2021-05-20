def to_pages_by_lines(content: str, max_size: int):
    pages = ['']
    i = 0
    for line in content.splitlines(keepends=True):
        if len(pages[i] + line) > max_size:
            i += 1
            pages.append('')
        pages[i] += line
    return pages