# Party Reply System

## Overview
A party reply system, where a host can send a link to all their invitees. The invitees can then register their name, and their response to the invite. As invitees return to the page, it will remember their previous response.

This program used a simple text file on the server to keep track of all the names and responses. 

Names must consist of at least one letter, so “X Æ A-12” would be a valid name, but “1234”. “~!!”, and “💩” would not be.

This program utilized the `pattern` attribute in the HTML `form` element to ensure a valid name is returned.

The “invitation” response page have a form with a text field for name, and a pair of radio buttons for “attending”. On submission, the user should be shown a “replied” page, showing their name and response. On return to the page, the use should see the “replied” page.

The “replied” page includes an “Anonymize” button. On clicking, the user will be forgotten from the site by clearing (setting to empty) the cookie values and having the visitor automatically returned to the invitation page.

The user can also update to their response when they revisit the CGI script, or if “Anonymize” operation is performed, with their previously submitted name.


## Usage
The same file is deployed [here](http://www-test.cs.umanitoba.ca/~wus2/cgi-bin/a.cgi).


## implementation

### Form
Implemented using a text box with `pattern` contraint attributes, and a pair of radio button indicating attending or not.

The form is returned by POST method.

### “Anonymize”
“Anonymize” request is returned by GET method without value.

### States
The states of this CGI script is determined by GET, POST requests and cookies.

GET request is exclusively used for “Anonymize” function.

POST request is used to transmit the response form.

Cookies are used to determine previous response.

There will be 5 states that this script need to handle:

* “Anonymize”: GET request `Anonymize=` is received, all other request will be ignored.

| States            | POST | Cookie |
|:-----------------:|:----:|:------:|
|     New User      |  ❌  |   ❌   |
|  Just submitted   |  ✔   |   ❌   |
|  Returning User   |  ❌  |   ✔    |
| Updating response |  ✔   |   ✔    |


### Response Storage 
The responses are stored in the same folder of this CGI script, named `dic_db.txt`. 

The responses are internally a dictionary, with name as key and response as value.

The response dictionary is printed out to the storage file and parsed by using `ast.literal_eval()`.
