# Shumeees 

Shumeees is a hobby-based web application that allows users to create profiles and connect with others based on shared hobbies. 


## Deployment

The deployed application is accessible at https://group28-web-apps-ec22517.apps.a.comp-teach.qmul.ac.uk/

### Admin user
**Username:** `admin`

**Password:** `B5PJwb8CW6EVx9`

### Test users
**Usernames:** `Ben`, `Daniel`, `Matt`, `William`, `Theo`

**Password (for all test users):** `queenMary100.`

## Local development

To run this project in your development machine, follow these steps:

1. Create and activate a conda environment

2. Download this repo as a zip and add the files to your own private repo.

3. Install Pyhton dependencies (main folder):

    ```console
    $ pip install -r requirements.txt
    ```

4. Create a development database:

    ```console
    $ python manage.py migrate
    ```

5. Install JavaScript dependencies (from 'frontend' folder):

    ```console
    $ npm install
    ```

6. If everything is alright, you should be able to start the Django development server from the main folder:

    ```console
    $ python manage.py runserver
    ```

7. and the Vue server from the 'frontend' sub-folder:

    ```console
    $ npm run dev
    ```

8. Open your browser and go to http://localhost:5173, you will be greeted with a template page.


