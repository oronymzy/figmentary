import argparse
import random
import ruamel.yaml

colorful_available = True
try: import colorful
except ImportError: colorful_available = False

yaml = ruamel.yaml.YAML()

# Using the argparse module
parser = argparse.ArgumentParser(prefix_chars='-+')
parser.add_argument("-c", "--colorize", help="display colorized text (requires *colorful* package)", action="store_true")
parser.add_argument("-t", "--tag", dest="minus_t", help="exclude literature by a specified tag", default=None)
parser.add_argument("+t", "++tag", dest="plus_t", help="only include literature containing a specified tag", default=None)
args = parser.parse_args()

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

with open("figmentary.yaml", "r") as opened_file:
    contents_of_opened_file = yaml.load(opened_file)
    if tag_to_exclude != None:
        # Two separate list comprehensions are required in order to avoid checking for a tag in a non-existent 'tag' key
        changing_six_word_stories = contents_of_opened_file['six-word stories']
        # Removing any list items in the 'six-word stories' list that do not contain a dictionary with 'tag' as a key
        changing_six_word_stories[:] = [list_item for list_item in changing_six_word_stories if 'tag' in list_item]
        # Removing any list items in the 'six-word stories' list containing the tag to be excluded
        changing_six_word_stories[:] = [list_item for list_item in changing_six_word_stories if tag_to_exclude not in list_item['tag']]
    if required_tag != None:
        # Two separate list comprehensions are required in order to avoid checking for a tag in a non-existent 'tag' key
        changing_six_word_stories = contents_of_opened_file['six-word stories']
        # Removing any list items in the 'six-word stories' list that do not contain a dictionary with 'tag' as a key
        changing_six_word_stories[:] = [list_item for list_item in changing_six_word_stories if 'tag' in list_item]
        # Removing any list items in the 'six-word stories' list that do not contain the required tag
        changing_six_word_stories[:] = [list_item for list_item in changing_six_word_stories if required_tag in list_item['tag']]
    number_of_six_word_stories = len(contents_of_opened_file['six-word stories'])
    random_6ws_index = random.randint(0,number_of_six_word_stories - 1)
    if colorize_text == True and colorful_available == True:
        colorful.use_style('solarized')
        available_colors = ['yellow','orange','red','magenta','violet','blue','cyan','green']
        random_color_selection = random.choice(available_colors)
        print(getattr(colorful, random_color_selection),contents_of_opened_file['six-word stories'][random_6ws_index]['story'])
    else:
        print(contents_of_opened_file['six-word stories'][random_6ws_index]['story'])
