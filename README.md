# yummy-recipes
Yummy recipes provides a platform for users to keep track of their awesome recipes and share with others if they so wish.

follow this [link](https://indungu.github.io/yummy-recipes)

## Notes
Well as you will realize there is still a lot more that needs to be done, some elements are irresponsive, some links are just dead links.
The wire-frame however covers/showcases the following features
``` 
  1. Creating an account 
  2. Login in to an account
  3. A landing page [Dashboard] after a successful login
```

## How to Use
On following the [link](https://indungu.github.io/yummy-recipes) a `Welcome` page is displayed.

Click the `Sign Up` button and this opens the `signup` page where which you provide account creation details and click `Submit`
to create your account.

The Dashboard is really just a mock-up of how the complete and functional dashboard will look. 
On successful it opens to a default view of the list of categories the user has created {the last four}.
There is a `View Recipes` link button under each of the diplayed categories which when clicked reveals
 all the recipes in that category.
 
 ## How to test
 
 The project is still in the UI desing phase, as such you just need to follow the following steps to test
 
 ```
  1. Clone the repository: git clone https://github.com/indungu/yummy-recipes
  2. Change directories: cd yummy-recipes
  3. On a browser of choice (preferably Chrome/Firefox) open the following file designs/UI/index.html
  4. Navigate the site as you would any other site.
  5. (Chrome/Firefox Users) You can test the mobile appearance of the site by accessing developer tools 
     [Ctrl+Shift+I] then toggle the device view to mobile through clicking the Toggle Device button or the 
     following key combination shortcut [Ctrl+Shift+M]
 ```
 Please note that the above set testing instructions are generally from a User/Developer running Chrome/Firefox on Windows. Most of the same is transferable to Linux and Mac OSX as is but there might be slight differences, especially in step five.
 
 ## To-Do
 ```
  I.  Add Create/Delete capability for recipes and recipe categories
  II. Improve aesthetic value of  the UI espectially for the welcome, signup and login pages
  III. Implement backend with Python Flask Microframework
 ```
