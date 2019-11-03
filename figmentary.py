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
        parser.add_argument("-T", "--display-tags", help="display available tags", action="store_true")
        args = parser.parse_args()
        return args

    args = specify_arguments()

    def assess_arguments(args):
        "Determine if values provided by the user are valid, and assign values to control-variables, whether provided by the user or not."
        
        story_displaying = True
        
        if args.colorize == True:
            text_colorizing = True
        else:
            text_colorizing = False

        if args.minus_t != None:
            tag_to_exclude = args.minus_t
        else:
            tag_to_exclude = None

        if args.plus_t != None:
            required_tag = args.plus_t
        else:
            required_tag = None
        if args.display_tags == True:
            tags_displaying = True
        else:
            tags_displaying = False
        if args.count_stories == True:
            story_count_displaying = True
        else:
            story_count_displaying = False

        if args.diagnostic == True:
            diagnostic_information_displaying = True
        else:
            diagnostic_information_displaying = False

        if args.minus_r != None:
            regex_to_exclude = args.minus_r
        else:
            regex_to_exclude = None

        if args.plus_r != None:
            required_regex = args.plus_r
        else:
            required_regex = None
        
        return {
            'text colorizing': text_colorizing,
            'story count displaying': story_count_displaying,
            'story displaying': story_displaying,
            'diagnostic information displaying': diagnostic_information_displaying,
            'regex to exclude': regex_to_exclude,
            'required regex': required_regex,
            'required tag': required_tag,
            'tag to exclude': tag_to_exclude,
            'tags displaying': tags_displaying
        }
    
    values_provided_by_user = assess_arguments(args)
    return values_provided_by_user

values_provided_by_user = allow_arguments()

with open("figmentary.yaml", "r") as opened_file:
    contents_of_opened_file = yaml.load(opened_file)
    def filter_sixws(values_provided_by_user):
        "Selectively remove six-word story list items, if so instructed by user input, then return a six-word story count."
        def exclude_sixws_based_on_story_content(regex_to_exclude):
            "Exclude six-word stories with specific, regex-formatted story content."
            for interim_dictionary in contents_of_opened_file['six-word stories'][:]:
                if "story" in interim_dictionary and re.search(regex_to_exclude, interim_dictionary["story"]) != None:
                    contents_of_opened_file['six-word stories'].remove(interim_dictionary)
        def include_sixws_based_on_story_content(required_regex):
            "Include only six-word stories with specific, regex-formatted story content."
            for interim_dictionary in contents_of_opened_file['six-word stories'][:]:
                if "story" in interim_dictionary and re.search(required_regex, interim_dictionary["story"]) == None:
                    contents_of_opened_file['six-word stories'].remove(interim_dictionary)
        def exclude_sixws_based_on_tag(tag_to_exclude):
            "Exclude six-word stories with a specific tag."
            # Two separate list comprehensions are required in order to avoid checking for a tag in a non-existent 'tag' key
            changing_six_word_stories = contents_of_opened_file['six-word stories']
            # Removing any list items in the 'six-word stories' list that do not contain an optional dictionary with 'tag' as a key
            changing_six_word_stories[:] = [list_item for list_item in changing_six_word_stories if 'tag' in list_item]
            # Removing any list items in the 'six-word stories' list containing the tag to be excluded
            changing_six_word_stories[:] = [list_item for list_item in changing_six_word_stories if tag_to_exclude not in list_item['tag']]
        def include_sixws_based_on_tag(required_tag):
            "Include only six-word stories with a specific tag."
            # Two separate list comprehensions are required in order to avoid checking for a tag in a non-existent 'tag' key
            changing_six_word_stories = contents_of_opened_file['six-word stories']
            # Removing any list items in the 'six-word stories' list that do not contain an optional dictionary with 'tag' as a key
            changing_six_word_stories[:] = [list_item for list_item in changing_six_word_stories if 'tag' in list_item]
            # Removing any list items in the 'six-word stories' list that do not contain the required tag
            changing_six_word_stories[:] = [list_item for list_item in changing_six_word_stories if required_tag in list_item['tag']]
        if values_provided_by_user['regex to exclude'] != None:
            exclude_sixws_based_on_story_content(values_provided_by_user['regex to exclude'])
        if values_provided_by_user['required regex'] != None:
            include_sixws_based_on_story_content(values_provided_by_user['required regex'])
        if values_provided_by_user['tag to exclude'] != None:
            exclude_sixws_based_on_tag(values_provided_by_user['tag to exclude'])
        if values_provided_by_user['required tag'] != None:
            include_sixws_based_on_tag(values_provided_by_user['required tag'])
        def get_sixws_count():
            "Get six-word story count, terminating if the count is zero."
            sixws_count = len(contents_of_opened_file['six-word stories'])
            if sixws_count == 0:
                exit()
            return sixws_count
        sixws_count = get_sixws_count()
        return sixws_count

    def control_display(colorful_available, values_provided_by_user):
        "Control what content to display as command-line output, choosing one out of several mutually-exclusive possibilities."
        def display_diagnostic_information():
            "Display diagnostic information."
            yaml.dump(contents_of_opened_file, sys.stdout)
        def display_tags():
            "Display available tags."
            tags_for_displaying = set()
            for interim_dictionary in contents_of_opened_file['six-word stories'][:]:
                if "tag" in interim_dictionary:
                    for interim_list_item in interim_dictionary['tag']:
                        tags_for_displaying.add(interim_list_item)
            print(sorted(tags_for_displaying))
        def display_story_count():
            "Display story count."
            sixws_count = filter_sixws(values_provided_by_user)
            print("Story count:",sixws_count)
        def display_story(text_colorizing):
            "Display a pseudorandomly-selected story, optionally colorizing text based on user input and module availability."
            sixws_count = filter_sixws(values_provided_by_user)
            def colorize_text(random_sixws_index):
                "Colorize text with a pseudorandomly-selected color."
                colorful.use_style('solarized')
                available_colors = ['yellow','orange','red','magenta','violet','blue','cyan','green']
                random_color_selection = random.choice(available_colors)
                print(getattr(colorful, random_color_selection),contents_of_opened_file['six-word stories'][random_sixws_index]['story'])
            random_sixws_index = random.randint(0,sixws_count - 1)
            if text_colorizing == True and colorful_available == True:
                colorize_text(random_sixws_index)
            else:
                print(contents_of_opened_file['six-word stories'][random_sixws_index]['story'])
        if values_provided_by_user['diagnostic information displaying'] == True:
            display_diagnostic_information()
        elif values_provided_by_user['tags displaying'] == True:
            display_tags()
        elif values_provided_by_user['story count displaying'] == True:
            display_story_count()
        elif values_provided_by_user['story displaying'] == True:
            display_story(values_provided_by_user['text colorizing'])
    control_display(colorful_available, values_provided_by_user)
