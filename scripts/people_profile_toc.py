import os


folder_path = "global-study-bible/people/profiles"
readme_path = "global-study-bible/people"

if not os.path.exists(folder_path):
    os.makedirs(folder_path)

file_path = "%s/README.md" % (readme_path)

files = os.listdir(folder_path)[:-1]

header = """# Facts
Profiles of objects (People, places etc.) in the Bible

"""

with open(file_path, "w") as f:
    f.write(header)

    for index, FILE in enumerate(files, 1):
        filename = FILE.split(".")[0].replace("-", " ").title().strip()
        f.write("%s. [%s](profiles/%s)\n" % (index, filename, FILE.replace(" ", "%20")))

print("TOC written")