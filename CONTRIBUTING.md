# Quick And Rough Contributions Guidelines

## Before starting contributing

1. Fork this repository
2. Clone your fork locally (replace USERNAME by yours)  

```bash
git clone git@github.com:USERNAME/issue_parser.git
```
3. Add the original repository as an upstream  

```bash
git remote add upstream https://github.com/webcompat/issue_parser.git
```
Now when you type `git remote -v`, you should see:  
```bash
→ git remote -v
origin  git@github.com:USERNAME/issue_parser.git (fetch)
origin  git@github.com:USERNAME/issue_parser.git (push)
upstream    https://github.com/webcompat/issue_parser.git (fetch)
upstream    https://github.com/webcompat/issue_parser.git (push)
```
4. Create a [virtual environment](https://virtualenvwrapper.readthedocs.io/en/latest/)

```bash
mkvirtualenv -a /path_to_code/issue_parser/ issue_parser
```

You should see something like this in your environment (if `path_to_code` is `~/code`)

```bash   
(issue_parser) 13:03:48 ~/code/issue_parser
```

The virtual environment will keep the project isolated which is good for not messing up versions in between different projects. Now that we have a safe place we can install the project dependencies.

5. Install the dependencies for the project

We use `pip install -r requirements.txt`

```
(issue_parser) 13:03:48 ~/code/issue_parser% pip install -r requirements.txt 
Collecting SQLAlchemy==1.1.0b2 (from -r requirements.txt (line 2))
  Downloading SQLAlchemy-1.1.0b2.tar.gz (5.1MB)
    100% |████████████████████████████████| 5.1MB 213kB/s 
Building wheels for collected packages: SQLAlchemy, antiorm
  Running setup.py bdist_wheel for SQLAlchemy ... done
  Stored in directory: /Users/[USERNAME]/Library/Caches/pip/wheels/1f/b2/29/45506927d237f0eade80692adcd81635437beb719e8fe2e857
  Running setup.py bdist_wheel for antiorm ... done
  Stored in directory: /Users/[USERNAME]/Library/Caches/pip/wheels/a2/33/f1/7f82ec910d513ff6e964aef854d9af2e3211c287fe1f0c7a09
Successfully built SQLAlchemy antiorm
Installing collected packages: antiorm, SQLAlchemy
Successfully installed SQLAlchemy-1.1.0b2 antiorm-1.2.1
```

You are good to start coding on the project.

## Python Code Requirements

* Save your files as utf-8
* Install a flake8 linter in your code editor
* Code with python 3
* Make it modular and testable
* Adds tests

## Commits and Pull Requests

* Mention the issue number in your commits 
  * YES ✅ `Issue #3 - Adds test case for issue parsing` 
  * NO 🚨 `Adding test case for issue parsing` 
* Tells what your commit is doing, not what you are doing. 
  * YES ✅ `Issue #3 - Adds test case for issue parsing` 
  * NO 🚨 `Issue #3 - Adding test case for issue parsing` 
* When doing a pull request, add the issue number you are fixing in the Pull Request title.
  * YES ✅ `Fixes #3 - Solves issues with encoding` 
  * NO 🚨 `Solves issues with encoding`
* Ask for explicit review from someone. Probaly @karlcow or @miketaylr
