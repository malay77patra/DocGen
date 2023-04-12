from git.repo.base import Repo
import os
import shutil
from aipower import explain_code
from splitall import extract_code
import json

with open('config.json', 'r') as f:
  config = json.load(f)

API_KEY = config["API_KEY"]
username = config["username"]
password = config["pat"]
#
i = 0
file_list = {}
api_settings = {
  "engine": "text-davinci-003",
  "max_tokens": 2048,
  "n": 1,
  "stop": None,
  "temperature": 0.3,
}

URL = input("Enter the repo url: ")
base_name = os.path.basename(URL).rstrip(".git")
work = base_name + str(i)
while True:
  if os.path.exists(os.path.join(work)):
    i += 1
    work = base_name + str(i)
  else:
    break
docs = os.path.join(work, "docs")

#clone

repo_url = URL
print("Cloning repo...")
repo_name = work
try:
  Repo.clone_from(repo_url, repo_name)
except:
  try:
    ending = URL.replace("https://", "")
    starting = f"https://{username}:{password}@"
    repo_url = starting + ending
    Repo.clone_from(repo_url, repo_name)
  except Exception as e:
    print(e)


repo_dir = os.path.abspath(repo_name)
root_path = os.path.join(docs)
here = os.path.abspath(os.path.join(os.path.dirname(__file__), work))

print("Creating needed files and dirs...")
os.mkdir(docs)


def cleare_path(patho):
  shutil.rmtree(os.path.join(patho))


def make_tree(root_dir):
  path_data = {}
  items = sorted(os.listdir(root_dir))

  for item in items:
    #
    if item.startswith('.'):
      continue
    #
    item_path = os.path.join(root_dir, item)
    #
    if os.path.isfile(item_path):
      if item.endswith(".py"):
        path_data.update({item: "file"})
    elif os.path.isdir(item_path):
      data = make_tree(item_path)
      path_data.update({item: data})
  return path_data


trees = make_tree(here)

print("Analyzing file system...")


def create_file_tree(tree, root_path):
  md_path = root_path.replace("/docs", "")
  parent_files = os.listdir(md_path)
  py_files = [file for file in parent_files if file.endswith('.py')]
  if len(py_files) != 0:
    with open(os.path.join(md_path, "README.md"), "a") as g:
      g.write("***\n# Read The Documentation For Better Understanding\n")
      for file in py_files:
        md_path_new = os.path.join(root_path, file).replace(".py", ".md")
        rel_md_path = os.path.relpath(md_path_new, md_path)
        md = f"\n📃 [{file}]({file}) - [Documentation]({rel_md_path})\n"
        g.write(md)

  global file_list
  for node, content in tree.items():
    if node == 'docs' or node == 'venv':
      continue
    node_path = os.path.join(root_path, node)
    if isinstance(content, dict):
      os.makedirs(node_path, exist_ok=True)
      create_file_tree(content, node_path)
    else:
      init_path = work + node_path.split(docs)[1]
      node_path = os.path.splitext(node_path)[0] + '.md'
      file_list.update({init_path: node_path})
      os.mknod(node_path)


create_file_tree(trees, root_path)

print(f"Total number of python scripts found: {len(file_list)}")


def write_into_file():
  print(
    "Analyzing codes and Generating documentation...\nPlease wait it may take a few minutes to complete!"
  )
  for parent in file_list:
    child = file_list[parent]
    with open(child, "a") as f:
      print(f"Analyzing file: {parent}")
      data = extract_code(parent)
      for typos in data:
        if (len(data[typos]) != 0):
          f.write("\n***\n# " + typos + "\n***\n")
          elems = data[typos]
          response = explain_code(API_KEY, api_settings, typos, elems)
          f.write(response)
    print(parent, "--succesfully documented ✔️")


write_into_file()

print(f"\nAll the documentation are saved into {docs} directory ✔️")

#please don't uncomment below line , It will remove all the generated docs, this is just for testing purpose root_path.replace("/docs", "")
"""
def cleare_path(path):
  shutil.rmtree(path)
#cleare_path(os.path.join(work))
"""
