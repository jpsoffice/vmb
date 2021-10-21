vmb
===

Vaishnava Marriage Bureau

.. image:: https://img.shields.io/badge/built%20with-Cookiecutter%20Django-ff69b4.svg
     :target: https://github.com/pydanny/cookiecutter-django/
     :alt: Built with Cookiecutter Django
.. image:: https://img.shields.io/badge/code%20style-black-000000.svg
     :target: https://github.com/ambv/black
     :alt: Black code style


:License: GPLv3

Local development
-----------------

* Install Docker and run Docker on your system. Follow the instructions here to install Docker, https://docs.docker.com/engine/install/
* Install ``docker-compose`` on your machine. https://docs.docker.com/compose/install/
* Set environment variables (e.g., API keys, secrets, etc.) used in ``docker-compose.yml``:

  * Fixer API Key for currency conversion

    * Go to https://fixer.io and get a free API Key, and set the API key against ``DJMONEY_EXCHANGE_FIXER_ACCESS_KEY`` in ``docker-compose.yml``
  * Google places API key
    * `export DJMONEY_EXCHANGE_FIXER_ACCESS_KEY=...`

    * Follow the instructions here: https://developers.google.com/maps/documentation/places/web-service/get-api-key to create a Google Maps API key
    * `export PLACES_MAPS_API_KEY=...`
* Run the services using ``docker-compose up -d``
* Check if service is up and running using ``docker-compose ps``. It should show something like below.

.. code-block::

     Name                   Command               State                    Ports
     --------------------------------------------------------------------------------------------------
     celerybeat       /entrypoint /start-celerybeat    Up
     celeryworker     /entrypoint /start-celeryw ...   Up
     flower           /entrypoint /start-flower        Up      0.0.0.0:5555->5555/tcp,:::5555->5555/tcp
     redis            docker-entrypoint.sh redis ...   Up      6379/tcp
     vmb_django_1     /entrypoint /start               Up      0.0.0.0:8000->8000/tcp,:::8000->8000/tcp
     vmb_postgres_1   docker-entrypoint.sh postgres    Up      5432/tcp


* You can now access the service by opening ``http://127.0.0.1:8000`` on your browser
* Create a superuser for the application using ``docker-compose exec django /entrypoint /app/manage.py createsuperuser``
* You can now login to the admin interface of the app using the superuser credentials from http://127.0.0.1:8000/admin
* Load fixtures to get the app funcional ``docker-compose exec django /entrypoint /app/manage.py loaddata /app/vmb/matrimony/fixtures/*``
* Load currency data: ``docker-compose exec django /entrypoint /app/manage.py update_rates``

Settings
--------

Moved to settings_.

.. _settings: http://cookiecutter-django.readthedocs.io/en/latest/settings.html

Basic Commands

--------------

Setting Up Your Users
^^^^^^^^^^^^^^^^^^^^^

* To create a **normal user account**, just go to Sign Up and fill out the form. Once you submit it, you'll see a "Verify Your E-mail Address" page. Go to your console to see a simulated email verification message. Copy the link into your browser. Now the user's email should be verified and ready to go.

* To create an **superuser account**, use this command::

    $ python manage.py createsuperuser

For convenience, you can keep your normal user logged in on Chrome and your superuser logged in on Firefox (or similar), so that you can see how the site behaves for both kinds of users.

Type checks
^^^^^^^^^^^

Running type checks with mypy:

::

  $ mypy vmb

Test coverage
^^^^^^^^^^^^^

To run the tests, check your test coverage, and generate an HTML coverage report::

    $ coverage run -m pytest
    $ coverage html
    $ open htmlcov/index.html

Running tests with py.test
~~~~~~~~~~~~~~~~~~~~~~~~~~

::

  $ pytest

Live reloading and Sass CSS compilation
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Moved to `Live reloading and SASS compilation`_.

.. _`Live reloading and SASS compilation`: http://cookiecutter-django.readthedocs.io/en/latest/live-reloading-and-sass-compilation.html





Deployment
----------

The following details how to deploy this application.



Docker
^^^^^^

See detailed `cookiecutter-django Docker documentation`_.

.. _`cookiecutter-django Docker documentation`: http://cookiecutter-django.readthedocs.io/en/latest/deployment-with-docker.html



