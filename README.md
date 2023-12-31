# Quora Clone

- Video: https://www.youtube.com/watch?v=MD5wOmRpdOU

### A website inspired by Quora with the following functionality requirements:

1. The user should be able to create a login
2. Post questions
3. View questions posted by others
4. Able to answer questions posted by others
5. Should be able to like answers posted by others
6. Able to log out
7. Can use Django Forms and the assignment does not look for elegance on the HTML front but functionality.

### Additional Functionality:

#### Questions
- Not Allowed to add, edit, delete questions until logged-in.
- Delete Button to delete questions
- Delete Button is only visible to the author of the Question
- Edit Button to Edit Questions
- Delete Question functionality only if logged-in user and question author are the same user

#### Answer

- Total likes count updated LIVE
- Edit Button to Edit Answers
- Not Allowed to add, edit answers until logged-in.

#### Like

- Likes are mapped from User to Answer allowing to keep track of who liked what
- Total likes are automatically calculated
- Not Allowed to Like until logged-in

### Basic Setup:

--> Move into the directory where we have the project files :

```bash
cd Quora-clone

```

--> Create a virtual environment :

```bash
# Let's install virtualenv first
pip install virtualenv

# Then we create our virtual environment
virtualenv envname

```

--> Activate the virtual environment :

```bash
envname\scripts\activate

```

--> Install the requirements :

```bash
pip install -r requirements.txt

```

#

### Running the App

--> To run the App, we use :

```bash
python manage.py runserver

```

> The development server will be started at http://127.0.0.1:8000/
