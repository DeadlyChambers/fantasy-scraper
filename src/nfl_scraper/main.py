# pylint: disable=too-many-function-args
# pylint: disable=multiple-imports
import sys, getopt
from nfl.user_login import open_main_page
from prompt_toolkit import prompt
from prompt_toolkit.shortcuts import set_title
from prompt_toolkit.validation import Validator


def is_valid_email(text):
    """_summary_

    Args:
        text (_type_): _description_

    Returns:
        _type_: _description_
    """
    return "@" in text


validator = Validator.from_callable(
    is_valid_email,
    error_message="Not a valid e-mail address (Does not contain an @).",
    move_cursor_to_end=True,
)

def main(args):
    """_summary_

    Args:
        args (_type_): _description_

    Returns:
        _type_: _description_
    """
    email = password = l_id = l_name = None
    verbose = True
    try:
        opts, args = getopt.getopt(args,"qhe:p:i:n",["email=","password=","id=","name="])
    except getopt.GetoptError:
        print('Issue with input validate your format is like below')
        print('main.py -e <email> -p <password> -i <id> -n <name> [-q]')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print('NFL Scraper will scrap NFL.COM to get your league history. Ensure you use the format below. \n')
            print('main.py -e <email> -p <password> -i <id> -n <name> [-q]')
            sys.exit()
        elif opt == "-q":
            verbose = False
        elif opt in ("-e", "--email"):
            email = arg
        elif opt in ("-p", "--password"):
            password = arg
        elif opt in ("-i", "--id"):
            l_id = arg
        elif opt in ("-n", "--name"):
            l_name = arg
        else:
            print('main.py -e <email> -p <password> -i <id> -n <name> [-q]')
            print(f'{arg} unexpected, remove option and try again')
            sys.exit(1)
    if email is None:
        email = prompt("Enter e-mail address: ", validator=validator, validate_while_typing=False)
    if password is None:
        password = prompt("Password: ", is_password=True)
    if l_id is None:
        l_id = prompt("Input League Id: ")
    if l_name is None:
        l_name = prompt("Input the name of the league: ")
    open_main_page(email, password, l_id, l_name, verbose)
    return 1

if __name__ == "__main__":
    set_title("Enter nfl.com email, password, leaugeid, and any name")
    main(sys.argv[1:])
