Chilling Effects Tools for Researchers
==============

This Python projects aims to provide tools for researchers who hope to use the [Chilling Effects](http://chillingeffects.org) database. When I developed this project I set out five goals:

- Simple design for researchers without a technical background
- Minimal setup.
- Easy customization to suit individual needs.
- Wide cross platform support (currently known to be supported on unix only).
- No unnecessary requests made to the database.

I chose Python because it is a defacto introductory programming language that should be easy for researchers to learn and use.

Installation and Setup
--------------

Clone the repository and execute `python commands.py`. This will build the necessary directories.

Basics
--------------

This project can be used in two primary ways: through the interpreter and direct execution.

To run through the interpreter:
- Enter the directory containing the file "commands.py".
- Run the python interpreter: `python`.
- Import the commands file: `import commands`.

This will load all the function definitions and enable you to interactively use the project.

To execute directly:
- Run `python commands.py`.

This will execute any commands you have placed beneath the `### Define commands here ###` line of "commands.py". All of the project's functions will be available to use in the commands file.


Configuration and Customization
--------------

To configure the project's global variables, edit their definitions in "config.py".

To change the project's default handlers for downloading notices and searching the database, change the variables `DOWNLOAD_HANDLER` and `SEARCH_HANDLER` in the "requests.py" file.

The Functions
--------------

There are numerous functions packaged with this project, but only a few our intended for the end user.

`download`
`download_set`
`search`
`interactive_search`
