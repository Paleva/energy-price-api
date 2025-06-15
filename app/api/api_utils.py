def group_hours(hours):
    ranges = []
    current_range = []

    for i in hours:
        if not current_range or i == current_range[-1] + 1:
            current_range.append(i)
        else:
            ranges.append(current_range)
            current_range = [i]
    if current_range:
        ranges.append(current_range)

    return {f"range_{index + 1}": r for index, r in enumerate(ranges)}
