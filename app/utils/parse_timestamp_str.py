def parse_timestamp_str(datetime_str):
    """
    Convert the string representation of datetime object to datetime object
    Args:
        datetime_str (str): string representation of datetime object
    Returns:
        datetime (datetime): datetime object 
    """
    time_format = "%d %b %Y %I:%M %p"

    datetime = datetime_str.strptime(datetime_str, time_format)

    return datetime
