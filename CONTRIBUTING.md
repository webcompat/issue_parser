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
   
   You should see something like this in your environment (if `path_to_code` is `~/code`)
   
        (issue_parser) 13:03:48 ~/code/issue_parser
        
   The virtual environment will keep the project isolated which is good for not messing up versions in between different projects. Now that we have a safe place we can install the project dependencies.

5. Install the dependencies for the project

   We use `pip install -r requirements.txt`

        (issue_parser) 13:03:48 ~/code/issue_parser% pip install -r requirements.txt 
        Collecting db==0.1.1 (from -r requirements.txt (line 1))
          Downloading db-0.1.1.tar.gz
        Collecting SQLAlchemy==1.1.0b2 (from -r requirements.txt (line 2))
          Downloading SQLAlchemy-1.1.0b2.tar.gz (5.1MB)
            100% |████████████████████████████████| 5.1MB 213kB/s 
        Collecting antiorm (from db==0.1.1->-r requirements.txt (line 1))
          Downloading antiorm-1.2.1.tar.gz (171kB)
            100% |████████████████████████████████| 174kB 3.5MB/s 
        Building wheels for collected packages: db, SQLAlchemy, antiorm
          Running setup.py bdist_wheel for db ... done
          Stored in directory: /Users/[USERNAME]/Library/Caches/pip/wheels/e4/1a/92/d22e4b97c77ac3c945b9b34395b290f1353f65239edb406156
          Running setup.py bdist_wheel for SQLAlchemy ... done
          Stored in directory: /Users/[USERNAME]/Library/Caches/pip/wheels/1f/b2/29/45506927d237f0eade80692adcd81635437beb719e8fe2e857
          Running setup.py bdist_wheel for antiorm ... done
          Stored in directory: /Users/[USERNAME]/Library/Caches/pip/wheels/a2/33/f1/7f82ec910d513ff6e964aef854d9af2e3211c287fe1f0c7a09
        Successfully built db SQLAlchemy antiorm
        Installing collected packages: antiorm, db, SQLAlchemy
        Successfully installed SQLAlchemy-1.1.0b2 antiorm-1.2.1 db-0.1.1


You are good to start coding on the project.
