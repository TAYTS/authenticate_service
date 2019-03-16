def create_timestamp_str(datetime):
    """
    Create the string representation of datetime object
    Args:
        datetime (datetime): timestamp
    Returns:
        timestamp_str(str): string representation of datetime object
    """
    time_format = "%d %b %Y %I:%M %p"

    timestamp_str = datetime.strftime(time_format)

    return timestamp_str
