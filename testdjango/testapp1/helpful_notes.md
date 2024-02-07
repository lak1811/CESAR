To the next developer testing this website, this will be useful when you want to send information to the database as a test
When you have given the database alot of unecessary data, just use code 
truncate testapp1_capitulosdelivrospublicados;
truncate testapp1_education;
truncate testapp1_otherproductions;
truncate testapp1_person;
truncate testapp1_producaotecnica;
truncate testapp1_project;
truncate testapp1_publications;
TRUNCATE testapp1_trabalho;
to remove it all


Also, if you want to connect this program to another database, firstly add the correct data
DATABASES = {
        'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'sql10639123',
        'USER': 'sql10639123',
        'PASSWORD': 'VyKJuJnrrl',
        'HOST': 'sql10.freemysqlhosting.net',  # or your MySQL host
        'PORT': '3306',       # MySQL default port
        'OPTIONS': {
          'autocommit': True,
        },
    }
}

this is how the database sections in settings.py is looking right now. To change it to your database, change the name,user,password,host and potentially port. After this make the migrations (py manage.py makemigrations) and migrate (py manage.py migrate)


I will explain here the necessary things you need to know as a developer for this application:
The file extrafuns is directly from the lucylattes application, and is essential that you dont remove it. It contains functions that are essential.
The Main.py file contains the whole method on this project. If you are looking to fix something in the functionality, then its the main.py file that is in question. The code is structured so you firstly generate all the information from the xml files into dataframes, and later transfer this data over to the databases. Its the same concept for all the dataframes, except the person table. There you mention that i have implemented an compare function. This function makes sure that the person doesnt exist from before. If the person exists from before, then you shall not add him again. Its a trick to avoid duplication in the persons table, to further improve validity.

If you wish to run the application, then you need to write 'py manage.py runserver'. This will start the server and give you an adress to type in the browser. From there the procedure is simple. If you are still not certain and have any question, please read the tutorial i have added. Good luck!