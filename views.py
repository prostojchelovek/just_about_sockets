def read_html(path):
    with open(path) as template:
        html_doc = template.read()
        return html_doc
