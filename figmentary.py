import argparse
import random
import re
import ruamel.yaml
import sys

def check_colorful_availability():
    "Check if optional 'colorful' module is available, and import it if available."
    colorful_available = True
    global colorful
    try: import colorful
    except ImportError: colorful_available = False
    return colorful_available

colorful_available = check_colorful_availability()

yaml = ruamel.yaml.YAML()

def allow_arguments():
    "Allow the user to utilize the program through command-line arguments and values."
    
    def specify_arguments():
        "Specify allowed command-line arguments using *argparse* module."
        global parser
        parser = argparse.ArgumentParser(prefix_chars='-+')
        parser.add_argument("-c", "--colorize", help="display colorized text with a pseudorandomly-selected color (requires *colorful* package)", action="store_true")
        parser.add_argument("-C", "--count-stories", help="display a count of how many stories are available instead of displaying a story", action="store_true")
        parser.add_argument("-d", "--diagnostic", help="display diagnostic information instead of displaying a story", action="store_true")
        parser.add_argument("-r", "--regex", dest="minus_r", help="exclude any stories with a specified regular expression", default=None)
        parser.add_argument("+r", "++regex", dest="plus_r", help="only include stories with a specified regular expression", default=None)
        parser.add_argument("-t", "--tag", dest="minus_t", help="exclude any stories with a specified tag", default=None)
        parser.add_argument("+t", "++tag", dest="plus_t", help="only include stories with a specified tag", default=None)
        args = parser.parse_args()
        return args

    args = specify_arguments()

    def assess_arguments(args):
        "Determine if values provided by the user are valid, and assign values to variables, whether provided by the user or not."
        
        display_story = True
        
        if args.colorize == True:
            colorize_text = True
        else:
            colorize_text = False

        if args.minus_t != None:
            tag_to_exclude = args.minus_t
        else:
            tag_to_exclude = None

        if args.plus_t != None:
            required_tag = args.plus_t
        else:
            required_tag = None

        if args.count_stories == True:
            count_stories = True
        else:
            count_stories = False

        if args.diagnostic == True:
            display_diagnostic_information = True
        else:
            display_diagnostic_information = False

        if args.minus_r != None:
            regex_to_exclude = args.minus_r
        else:
            regex_to_exclude = None

        if args.plus_r != None:
            required_regex = args.plus_r
        else:
            required_regex = None
        
        return {
            'colorize text': colorize_text,
            'count stories': count_stories,
            'display story': display_story,
            'display diagnostic information': display_diagnostic_information,
            'regex to exclude': regex_to_exclude,
            'required regex': required_regex,
            'required tag': required_tag,
            'tag to exclude': tag_to_exclude
        }
    
    values_provided_by_user = assess_arguments(args)
    return values_provided_by_user

values_provided_by_user = allow_arguments()
colorize_text = values_provided_by_user['colorize text']
count_stories = values_provided_by_user['count stories']
display_story = values_provided_by_user['display story']
display_diagnostic_information = values_provided_by_user['display diagnostic information']
regex_to_exclude = values_provided_by_user['regex to exclude']
required_regex = values_provided_by_user['required regex']
required_tag = values_provided_by_user['required tag']
tag_to_exclude = values_provided_by_user['tag to exclude']

with open("figmentary.yaml", "r") as opened_file:
    contents_of_opened_file = yaml.load(opened_file)
    # Filtering six-word stories based on story content if so instructed by user input
    if regex_to_exclude != None:
        for interim_dictionary in contents_of_opened_file['six-word stories'][:]:
            if "story" in interim_dictionary and re.search(regex_to_exclude, interim_dictionary["story"]) != None:
                contents_of_opened_file['six-word stories'].remove(interim_dictionary)
    if required_regex != None:
        for interim_dictionary in contents_of_opened_file['six-word stories'][:]:
            if "story" in interim_dictionary and re.search(required_regex, interim_dictionary["story"]) == None:
                contents_of_opened_file['six-word stories'].remove(interim_dictionary)
    # Filtering six-word stories based on tags if so instructed by user input
    if tag_to_exclude != None:
        # Two separate list comprehensions are required in order to avoid checking for a tag in a non-existent 'tag' key
        changing_six_word_stories = contents_of_opened_file['six-word stories']
        # Removing any list items in the 'six-word stories' list that do not contain an optional dictionary with 'tag' as a key
        changing_six_word_stories[:] = [list_item for list_item in changing_six_word_stories if 'tag' in list_item]
        # Removing any list items in the 'six-word stories' list containing the tag to be excluded
        changing_six_word_stories[:] = [list_item for list_item in changing_six_word_stories if tag_to_exclude not in list_item['tag']]
    if required_tag != None:
        # Two separate list comprehensions are required in order to avoid checking for a tag in a non-existent 'tag' key
        changing_six_word_stories = contents_of_opened_file['six-word stories']
        # Removing any list items in the 'six-word stories' list that do not contain an optional dictionary with 'tag' as a key
        changing_six_word_stories[:] = [list_item for list_item in changing_six_word_stories if 'tag' in list_item]
        # Removing any list items in the 'six-word stories' list that do not contain the required tag
        changing_six_word_stories[:] = [list_item for list_item in changing_six_word_stories if required_tag in list_item['tag']]
    sixws_count = len(contents_of_opened_file['six-word stories'])
    if sixws_count == 0:
        # In this situation, no six-word stories remain
        exit()
    # Displaying diagnostic information if so instructed by user input
    if display_diagnostic_information == True:
        yaml.dump(contents_of_opened_file, sys.stdout)
        # Nothing more will be displayed now that diagnostic information has been displayed
        count_stories = False
        display_story = False
    # Displaying story count if so instructed by user input
    if count_stories == True:
        print("Story count:",sixws_count)
        # A story will not be displayed now that story-count-related information has been displayed
        display_story = False
    # Displaying a story if so instructed by user input
    if display_story == True:
        random_sixws_index = random.randint(0,sixws_count - 1)
        # Colorizing text of a story if so instructed by user input, and if the 'colorful' module is available
        if colorize_text == True and colorful_available == True:
            colorful.use_style('solarized')
            available_colors = ['yellow','orange','red','magenta','violet','blue','cyan','green']
            random_color_selection = random.choice(available_colors)
            print(getattr(colorful, random_color_selection),contents_of_opened_file['six-word stories'][random_sixws_index]['story'])
        # Displaying a story
        else:
            print(contents_of_opened_file['six-word stories'][random_sixws_index]['story'])
