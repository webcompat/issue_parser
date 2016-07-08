# Quick And Rough Contributions Guidelines

Before starting contributing on this code, 

1. Fork this repository

2. Clone your fork locally (replace USERNAME by yours)

        git clone git@github.com:USERNAME/issue_parser.git

3. Add the original repository as an upstream

        git remote add upstream https://github.com/webcompat/issue_parser.git

    Now when you type `git remote -v`, you should see:

        → git remote -v
        origin  git@github.com:USERNAME/issue_parser.git (fetch)
        origin  git@github.com:USERNAME/issue_parser.git (push)
        upstream    https://github.com/webcompat/issue_parser.git (fetch)
        upstream    https://github.com/webcompat/issue_parser.git (push)

4. Create a [virtual environment](https://virtualenvwrapper.readthedocs.io/en/latest/)

        mkvirtualenv -a /path_to_code/issue_parser/ issue_parser

5. Install the dependencies for the project

        pip install -r /path_to_code/issue_parser/requirements.txt


You are good to start.