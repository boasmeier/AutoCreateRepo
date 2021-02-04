from github import Github
import pygit2
from configparser import ConfigParser
import os.path
import argparse

def getConfig(filename, section, key):
    if not os.path.isfile(filename):
        raise FileNotFoundError("File with name {} not found.".format(filename))
    parser = ConfigParser()
    parser.read(filename)
    return parser.get(section, key)

if __name__ == "__main__":
    # construct the argument parser and parse the arguments
    ap = argparse.ArgumentParser()
    ap.add_argument("-i", "--name", required=True,
	    help="name of the repository to create")
    ap.add_argument("-p", "--path", required=False,
	    help="absolute path to create local repo")
    args = vars(ap.parse_args())

    # create session
    g = Github(getConfig('github.ini', 'Auth', 'accesstoken'))
    user = g.get_user()

    # create repo
    repo = user.create_repo(args['name'])
    repo.create_file("README.md", "init commit", "# " + args['name'])

    # clone repo and set upstream
    if args['path'] is None:
        repoClone = pygit2.clone_repository(repo.git_url, "./" + args['name'])
    else:
        repoClone = pygit2.clone_repository(repo.git_url, args['path'] + "/" + args['name'])
  
    repoClone.remotes.set_url("origin", repo.ssh_url)
    repoClone.remotes.set_push_url("origin", repo.ssh_url)


