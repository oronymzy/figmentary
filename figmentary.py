import argparse
import random
import re
import ruamel.yaml
import sys

# Checking if optional 'colorful' module is available
colorful_available = True
try: import colorful
except ImportError: colorful_available = False

yaml = ruamel.yaml.YAML()

# Using the argparse module
parser = argparse.ArgumentParser(prefix_chars='-+')
parser.add_argument("-c", "--colorize", help="display colorized text with a pseudorandomly-selected color (requires *colorful* package)", action="store_true")
parser.add_argument("-C", "--count-stories", help="display a count of how many stories are available instead of displaying a story", action="store_true")
parser.add_argument("-d", "--diagnostic", help="display diagnostic information instead of displaying a story", action="store_true")
parser.add_argument("-r", "--regex", dest="minus_r", help="exclude any stories with a specified regular expression", default=None)
parser.add_argument("+r", "++regex", dest="plus_r", help="only include stories with a specified regular expression", default=None)
parser.add_argument("-t", "--tag", dest="minus_t", help="exclude any stories with a specified tag", default=None)
parser.add_argument("+t", "++tag", dest="plus_t", help="only include stories with a specified tag", default=None)
args = parser.parse_args()

# Assignments to hold default values for maximizing output consistency
display_story = True
display_diagnostic_information = True

# Code related to assignments to hold user-provided values begins

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

# Code related to assignments to hold user-provided values ends

with open("figmentary.yaml", "r") as opened_file:
    contents_of_opened_file = yaml.load(opened_file)
    # Filtering six-wrod stories based on story content if so instructed by user input
    if regex_to_exclude != None:
        for current_dictionary in contents_of_opened_file['six-word stories'][:]:
            if "story" in current_dictionary and re.search(regex_to_exclude, current_dictionary["story"]) != None:
                contents_of_opened_file['six-word stories'].remove(current_dictionary)
    if required_regex != None:
        for current_dictionary in contents_of_opened_file['six-word stories'][:]:
            if "story" in current_dictionary and re.search(required_regex, current_dictionary["story"]) == None:
                contents_of_opened_file['six-word stories'].remove(current_dictionary)
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
