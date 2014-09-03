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

There are numerous functions packaged with this project, but only a few our intended for the end user:

`download`
`download_set`
`search`
`interactive_search`

## download

The `download` function takes a notice id and an option, Boolean `cache_override`. It downloads the notice corresponding to the id, using/building the cache if the `CACHE_BOOL` evaluates to `True`, handles the raw json string with `DOWNLOAD_HANDLER`, and then returns the result.

## download_set

The `download_set` function takes a list and option Boolean, `cache_override`. Each item of the list is interpreted as an integer and then the corresponding notice is downloaded via the `download` function. The results of the `download` function are accumulated in a list and returned when `download_set` complete.

## search

The `search` function takes a dictionary and option Boolean, `cache_override`. The function uses the cache if `CACHE_BOOL` evaluates to `True`. The keys of the dictionary should be the names of search parameters from the search_params.py file (this file includes all valid parameters on the Chilling Effects database and can be extended as desired). The values of the dictionary should be in one of the following forms:
`["search_term"]`
`["term1, "term2", "require_all"]`
`["term1, "term2"]`

Terms can include macros as discussed later in the documentation. For parameters that can accept multiple values, the final element of the list should be the string "require_all" if all values should be required.

Each list of terms is passed to the corresponding `Param` object and the formatted by that object. The returned strings are concatenated and then the search request is issued. The result is handled by SEARCH_HANDLER and returned.

## interactive_search

The `interactive_search` function takes an optional Boolean, `fully_interactive` (defaults to `True`), an optional dictionary, `seed_dic` (defaults to `{}`), and an optional Boolean `cache_override` (defaults to `False` as usual).

The function features an interactive prompt. If `fully_interactive` evaluates to `True`, then the prompt will query the user about each `Param` defined in search_params.py. If `fully_interactive` evaluates to `False`, then the prompt will query the user about which `Param`s need to be accessed. The user input for search terms is parsed according to `process_user_input` which assumes terms are separated by the space character, `' '`. The user input can include macros as discussed later in the documentation.

The parsed input is formatted properly and added to the `seed_dic`. The result is passed to the `search` function.
