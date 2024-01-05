import markdown
import os
from jinja2 import Environment, FileSystemLoader

env = Environment(loader=FileSystemLoader("."))
m = markdown.Markdown(extensions=["meta"])
os.makedirs("build/", exist_ok=True)
POSTS_DIR = "posts"
_, _, files = next(os.walk("posts"))
COUNT = len(files)


def main():
    t = env.get_template("index.html.jinja2")
    for file in os.listdir(POSTS_DIR):
        markdown_file = os.path.join(POSTS_DIR, file)
        with open(markdown_file, "r") as f:
            # https://python-markdown.github.io/extensions/footnotes/#resetting-instance-state
            m.reset()
            post_html = m.convert(f.read())
            post_page = t.render(post=post_html, meta=m.Meta, COUNT=COUNT)
            slug = m.Meta["slug"][0]
            if slug=="0":
                with open("build/index.html", "w") as output_file:
                    output_file.write(post_page)
                print("[+] generated: /index.html")

            with open(f"build/{slug}.html", "w") as output_file:
                output_file.write(post_page)
            print(f"[+] generated: /{slug}.html")


if __name__ == "__main__":
    main()
