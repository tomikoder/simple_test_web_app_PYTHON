from jinja2 import Environment, FileSystemLoader

environment = Environment(loader=FileSystemLoader("C:\\Users\\Tomek\\PycharmProjects\\some_project\\templates"))
template = environment.get_template("menu.html")

print(template.render())
