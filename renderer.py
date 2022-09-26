import jinja2
import csv
from dataclasses import dataclass, field


class TemplateNotFoundError(Exception):
    def __str__(self):
        return "File: jeopardy_template.html was not found."


@dataclass
class Question:
    value: int
    question: str
    answer: str
    img: str
    id: int = field(default=None)

    def __post_init__(self):
        self.id = id(self)


def get_categories(file):
    categories = {}
    with open(file, encoding="utf-8") as f:
        reader = csv.reader(f)
        next(reader)
        for _row in reader:
            if _row[0] not in categories.keys():
                categories.update({_row[0]: [Question(_row[1], _row[2], _row[3], _row[4])]})
            else:
                categories[_row[0]].append(Question(_row[1], _row[2], _row[3], _row[4]))

    qlens = [len(categories[cat]) for cat in categories]
    same_len = all(qlen == qlens[0] for qlen in qlens)
    if not same_len:
        raise ValueError("Every category has to have the same number of questions")
    return categories


def make_rows(categories):
    rows = []
    num_questions = len(categories[next(iter(categories))])
    for index in range(num_questions):
        questions = []
        for i in categories:
            questions.append(categories[i][index])
        rows.append(questions)
    return rows


def render(rows, categories):
    template_loader = jinja2.FileSystemLoader(searchpath="./")
    template_env = jinja2.Environment(loader=template_loader)
    TEMPLATE_FILE = "templates/jeopardy_template.html"
    try:
        template = template_env.get_template(TEMPLATE_FILE)
    except jinja2.exceptions.TemplateNotFound:
        raise TemplateNotFoundError
    rendered = template.render(categories=categories.keys(), rows=rows)
    return rendered


def make_jeopardy(file, pageid):
    categories = get_categories(file)
    rows = make_rows(categories)
    rendered = render(rows, categories)
    with open("templates/jeopardy_" + pageid + ".html", "w") as f:
        f.write(rendered)
    
