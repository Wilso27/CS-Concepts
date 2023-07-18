# regular_expressions.py


import re

import numpy as np


def prob1():
    """Compile and return a regular expression pattern object with the
    pattern string "python".

    Returns:
        (_sre.SRE_Pattern): a compiled regular expression pattern object.
    """
    return re.compile("python")


def prob2():
    """Compile and return a regular expression pattern object that matches
    the string "^{@}(?)[%]{.}(*)[_]{&}$".

    Returns:
        (_sre.SRE_Pattern): a compiled regular expression pattern object.
    """
    return re.compile(r"\^\{@\}\(\?\)\[%\]\{\.\}\(\*\)\[_\]\{&\}\$")


def prob3():
    """Compile and return a regular expression pattern object that matches
    the following strings (and no other strings).

        Book store          Mattress store          Grocery store
        Book supplier       Mattress supplier       Grocery supplier

    Returns:
        (_sre.SRE_Pattern): a compiled regular expression pattern object.
    """
    return re.compile(r"^(Book|Mattress|Grocery) (store|supplier)$")


def prob4():
    """Compile and return a regular expression pattern object that matches
    any valid Python identifier.

    Returns:
        (_sre.SRE_Pattern): a compiled regular expression pattern object.
    """
    return re.compile(r"^[a-zA-Z_](\w*)( *)(= *(\d*)|= *(\d*\.\d*)|= *\'(\w*)\'|= *[a-zA-Z_](\w*))?$")


def prob5(code):
    """Use regular expressions to place colons in the appropriate spots of the
    input string, representing Python code. You may assume that every possible
    colon is missing in the input string.

    Parameters:
        code (str): a string of Python code without any colons.

    Returns:
        (str): code, but with the colons inserted in the right places.
    """
    # begin by recognizing every key word
    pattern = re.compile(r"^([ \t]*(?:if|elif|for|while|try|with|def|class|else|finally|except|except)[^\n]*)", flags=re.MULTILINE)

    #return the substitution with the original pattern and a colon
    return pattern.sub( r"\1:", code)


def prob6(filename="fake_contacts.txt"):
    """Use regular expressions to parse the data in the given file and format
    it uniformly, writing birthdays as mm/dd/yyyy and phone numbers as
    (xxx)xxx-xxxx. Construct a dictionary where the key is the name of an
    individual and the value is another dictionary containing their
    information. Each of these inner dictionaries should have the keys
    "birthday", "email", and "phone". In the case of missing data, map the key
    to None.

    Returns:
        (dict): a dictionary mapping names to a dictionary of personal info.
    """
    # open file
    with open(filename, 'r') as file:
        data = np.genfromtxt(file, delimiter = ',', dtype = str)
    file.close()

    # create dictionary
    contacts = dict()

    # compile patterns
    name_p = re.compile(r"^[a-zA-Z]+ ([A-Z]\. )?[a-zA-Z]+")
    birthday_p = re.compile(r"(\d{1,2})\/(\d{1,2})\/(\d{4}|\d{2})")
    email_p = re.compile(r"[^@\s]*@[^\s]*")
    phone_p = re.compile(r"(\d{3}).{0,2}(\d{3})-(\d{4})")

    for i in range(len(data)): # loop through each person
        # get one line of data
        person = data[i]

        # search for the patterns
        name = name_p.search(person).group(0)
        birthday = birthday_p.search(person)
        email = email_p.search(person)
        phone = phone_p.search(person)

        # check if each attribute is not None
        if birthday is not None:
            # Separate each group
            month = birthday.group(1)
            day = birthday.group(2)
            year = birthday.group(3)

            # pad lengths if needed
            if len(day) == 1:
                day = '0' + day
            if len(month) == 1:
                month = '0' + month
            if len(year) == 2:
                year = '20' + year
            print(year)

            # append them to create the date
            birthday = month + '/' + day + '/' + year

        if email is not None:
            email = email.group(0)

        if phone is not None:
            # append the groups in proper format
            phone = '(' + phone.group(1) + ')' + phone.group(2) + '-' + phone.group(3)

        # create the dictionary with all elements
        contacts[name] = {"birthday":birthday, "email":email, "phone":phone}

    # return the dictionary
    return contacts
