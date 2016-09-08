import iso8601

def time_diff_in_seconds(a, b):
    time_delta = iso8601.parse_date(b) - iso8601.parse_date(a)
    return time_delta.seconds
