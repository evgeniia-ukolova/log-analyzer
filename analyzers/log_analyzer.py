


def count_requests(entries):
    count = 0

    for entry in entries:
        count += 1

    return count


def count_status_codes(entries):
    status_counts = {}

    for entry in entries:
        status_code = entry.status_code

        if status_code in status_counts:
            status_counts[status_code] += 1
        else:
            status_counts[status_code] = 1

    return status_counts


def count_errors(entries):

    count = 0
    for entry in entries:

        if entry.status_code >= 400:
            count += 1

    return count


def average_response_time(entries):
    total_time = 0
    count = 0

    for entry in entries:
        total_time += entry.response_time
        count += 1

    if count == 0:
        return 0

    return total_time / count   


def count_endpoints(entries):
    endpoints_counts = {}

    for entry in entries:
        endpoint = entry.endpoint

        if endpoint in endpoints_counts:
            endpoints_counts[endpoint] += 1
        else:
            endpoints_counts[endpoint] = 1

    return endpoints_counts


def top_endpoints(entries):
    endpoint_counts = count_endpoints(entries)

    sorted_endpoints = sorted(
    endpoint_counts.items(),
    key=lambda item: item[1],
    reverse=True,
    )

    return sorted_endpoints


def slowest_requests(entries):
    entries = list(entries)

    result = sorted(
        entries,
        key=lambda entry: entry.response_time,
        reverse=True,
    )

    return result


def filter_by_level(entries, level):
    for entry in entries:
        if entry.level == level:
            yield entry


def filter_by_status(entries, status_code):
    for entry in entries:
        if entry.status_code == status_code:
            yield entry


def filter_by_method(entries, method):
    for entry in entries:
        if entry.method == method:
            yield entry
 

def filter_by_endpoint(entries, endpoint):
    for entry in entries:
        if entry.endpoint == endpoint:
            yield entry


def filter_by_response_time(entries, min_response_time):
    for entry in entries:
        if entry.response_time >= min_response_time:
            yield entry



















