import git
from datetime import datetime

current_date = datetime.now().date()

repo = git.Repo(r'D:\Projects\Eternityscape')

git = repo.git
git.add('.')

if repo.is_dirty():
    git.commit('-m', 'auto commit for ' + str(current_date))
    print("commit successfully")
else:
    print("workspace is clean")
