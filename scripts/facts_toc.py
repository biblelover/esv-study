import os


folder_path = "global-study-bible/facts/books"
readme_path = "global-study-bible/facts"

if not os.path.exists(folder_path):
    os.makedirs(folder_path)

file_path = "%s/README.md" % (readme_path)

files = os.listdir(folder_path)[:-1]
files = sorted(files, key=lambda x: int(x.split(".")[0]))

header = """# Facts
Facts from the Bible

"""

with open(file_path, "w") as f:
    f.write(header)

    for index, FILE in enumerate(files, 1):
        filename = FILE.split(".")[1].replace("-", " ").title().strip()
        f.write("%s. [%s](books/%s)\n" % (index, filename, FILE.replace(" ", "%20")))

print("TOC written")