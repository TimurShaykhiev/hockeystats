NHL_STATS_DOMAIN = 'https://statsapi.web.nhl.com'


def create_load_file(filename, objects, append=True):
    """
    Create file with data for loading to MySql
    :param filename: File name
    :param objects: List of data models
    :param append: If True - append data to file, overwrite it otherwise
    :return: None
    """
    with open(filename, 'a' if append else 'w') as outfile:
        for o in objects:
            outfile.write(str(o))
