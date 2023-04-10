from git.repo.base import Repo
import os
import shutil
from aipower import explain_code
from splitall import extract_code
import json

with open('config.json', 'r') as f:
    config = json.load(f)
API_KEY = config["API_KEY"]
i = 0
v = 0
work = "work" + str(v)
file_list = {}

while True:
  if os.path.exists(os.path.join(work)):
    i += 1
    work = "work" + str(i)
  else:
    break

URL = input("URL: ")
#   https://github.com/malay9418/PYTHON_PROJECTS

#clone

repo_url = URL
print("Cloning repo...")
repo_name = os.path.join(work, os.path.basename(repo_url)).rstrip(".git")
Repo.clone_from(repo_url, repo_name)
print("Cloned succesfully")
docs = os.path.basename(repo_url).rstrip(".git") + "-docs" + str(i)

repo_dir = os.path.abspath(repo_name)
root_path = os.path.join(docs)
dest_path = os.path.join(work)
here = os.path.abspath(os.path.join(os.path.dirname(__file__), work))

#print(repo_dir, docs_dir)

print("creating needed files and dirs...")


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
        #print("file: ", item)
        path_data.update({item: "file"})
    elif os.path.isdir(item_path):
      #print("dir: ", item)
      data = make_tree(item_path)
      path_data.update({item: data})
  return path_data


trees = make_tree(here)

print("Analyzing file system...")


def create_file_tree(tree, root_path, dest_path):
  global file_list
  for node, content in tree.items():
    node_path = os.path.join(root_path, node)
    if isinstance(content, dict):
      os.makedirs(node_path, exist_ok=True)
      create_file_tree(content, node_path, dest_path)
    else:
      init_path = work + node_path.split(docs)[1]
      node_path = os.path.splitext(node_path)[0] + '.md'
      file_list.update({init_path: node_path})
      with open(node_path, 'w') as f:
        f.write("")


create_file_tree(trees, root_path, dest_path)
#print(file_list)
print(f"total {len(file_list)} python scripts found")

def write_into_file():
  print("Generating documentation...")
  for parent in file_list:
    child = file_list[parent]
    with open(child, "a") as f:
      data = extract_code(parent)
      for typos in data:
        if (len(data[typos])!=0):
          f.write("\n***\n# " + typos + "\n***\n")
          elems = data[typos]
          response = explain_code(API_KEY, typos, elems)
          f.write(response)
    print(parent, "succesfully documented")

write_into_file()


print(f"All the dpcumentation are saved into {docs} directory")
def cleare_path(path):
  shutil.rmtree(path)


cleare_path(os.path.join(work))