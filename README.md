[![Build Status](https://travis-ci.org/ssat335/processkeralarescue.svg?branch=master)](https://travis-ci.org/ssat335/processkeralarescue)

# processkeralarescue
Repository aims to develop a dashboard to optimise and sort rescue operations. See initial implementation in
https://process.keralarescue.in/.

## Running natively
### Prerequisites

You will need to have following softwares in your system:

- [Python 3](https://www.python.org/downloads/)
- [Git](https://git-scm.com/downloads)

### Installing

#### Setting up a development environment
1. Clone the repo.
```
git clone https://github.com/ssat335/processkeralarescue.git
cd processkeralarescue
```

2. Install dependencies.

```
pip3 install -r requirements.txt
```

6. Run the server.

```
python3 app.py
```

## How can you help?

### Contribution Guidelines
[Wiki](https://github.com/IEEEKeralaSection/rescuekerala/wiki/Contribution-Guidelines)

## Testing Pull Requests

1. Checkout the Pull Request you would like to test by
      ```
      git fetch origin pull/ID/head:BRANCHNAME`
      git checkout BRANCHNAME
     ```    
2. Example
    ```
    git fetch origin pull/406/head:jaseem  
    git checkout jaseem1
    ```
### Submitting Pull Requests

Always start your work in a new git branch. **Don't start to work on the
master branch**. Before you start your branch make sure you have the most
up-to-date version of the master branch then, make a branch that ideally
has the bug number in the branch name.

1. Before you begin, Fork the repository. This is needed as you might not have permission to push to the main repository

2. If you have already clone this repository, create a remote to track your fork by
     ```
     git remote add origin2 git@github.com:tessie/processkeralarescue.git
     ```
3. If you have not yet cloned, clone your fork
    ```
    git clone git@github.com:tessie/processkeralarescue.git
    ```
4. Checkout a new branch by
     ```
     git checkout -b issues_442
     ```
4. Make your changes.

5. Ensure your feature is working as expected.

6. Push your code.
      ```
      git push origin2 issues_442
      ```
7. Compare and create your pull request.   
