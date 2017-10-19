# yummy-recipes

[![Build Status](https://travis-ci.org/indungu/yummy-recipes.svg?branch=master)](https://travis-ci.org/indungu/yummy-recipes)

[![Coverage Status](https://coveralls.io/repos/github/indungu/yummy-recipes/badge.svg?branch=master)](https://coveralls.io/github/indungu/yummy-recipes?branch=master)

Yummy recipes provides a platform for users to keep track of their awesome recipes and share with others if they so wish.

follow this [link](https://indungu.github.io/yummy-recipes)

## Notes

Well as you will realize there is still a lot more that needs to be done, some elements are irresponsive, some links are just dead links.
The wire-frame however covers/showcases the following features

* *Creating an account*
* *Login in to an account*
* A landing page [Dashboard] after a successful login

## How to Use

On following the [link](https://indungu.github.io/yummy-recipes) a `Welcome` page is displayed.

Click the `Sign Up` button and this opens the `signup` page where which you provide account creation details and click `Submit`
to create your account.

The Dashboard is really just a mock-up of how the complete and functional dashboard will look.
On successful it opens to a default view of the list of categories the user has created {the last four}.
There is a `View Recipes` link button under each of the diplayed categories which when clicked reveals
all the recipes in that category.

## Installation

The project is running parallel front end (static UI desing) and backend, as such you just need to follow the link above to view proposed UI and the following steps to install serverside framwork.

### Prerequisites

1. *Python version*

`$ python --version`
`Python 3.6.2`
If you have a lower version of Python please download the above version for your specific version
[here](https://www.python.org/downloads/release/python-362/) or alternatively a higher version
[here](https://www.python.org/downloads/), if one exists at the time of review.
2. *Virtual environment*

`$ pip install virtualenv`
alternatively
`$ pip install pipenv`

### For MacOS or Linux

```bash
  #!/bin/bash
  $ git clone -b dev https://github.com/indungu/yummy-recipes # Clone repo's dev branch
  $. cd yummy-recipes  # Switch to working directory
  $ virtualenv venv        # Install virtual envronment
  $ bin/activate             # Activate virtualenv
  $ pip install -r requirements.txt # Install package dependencies
  $ pip install pytest     # Install testing script
```

### For Windows

In an elevated `cmd` prompt or PowerShell instance, enter the following commands

```bat
#!c:\user\usr\

  > git clone -b dev https://github.com/indungu/yummy-recipes # Clone repo's dev branch
  >. cd yummy-recipes  # Switch to working directory
  > virtualenv venv        # Install virtual environment
  >.venv\Scripts\activate              # Activate virtualenv
  > pip install -r requirements.txt # Install package dependencies
  > pip install pytest                     # Install testing script
```

## To-Do

I.  Add Create/Delete capability for recipes and recipe categories
II. Improve aesthetic value of  the UI espectially for the welcome, signup and login pages
III. Implement backend with Python Flask Microframework
