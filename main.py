import streamlit as st
import re
from dataclasses import dataclass
from typing import List


@dataclass
class Activity:
    start: str
    end: str
    name: str


def parse_activities(text: str) -> List[Activity]:
    # Parse lines like '09:00 - 09:15 Activity'
    pattern = r"(\d{2}:\d{2})\s*-\s*(\d{2}:\d{2})\s+(.*)"
    activities = []
    for line in text.splitlines():
        match = re.match(pattern, line.strip())
        if match:
            start, end, name = match.groups()
            activities.append(Activity(start, end, name))
    return activities


def get_time_points(activities: List[Activity]) -> List[str]:
    # Collect all unique time points
    points = set()
    for act in activities:
        points.add(act.start)
        points.add(act.end)
    return sorted(points)


def build_ascii_table(activities: List[Activity], time_points: List[str]) -> str:
    # Calculate column widths
    activity_col_width = max(8, max((len(a.name) for a in activities), default=8))
    time_col_width = max(7, max(len(tp) for tp in time_points))
    # Header (no column separators)
    header = f"  {'activity'.center(activity_col_width)}  "
    for tp in time_points:
        header += f" {tp.center(time_col_width)}"
    header += "\n"
    # Separator (just a single line)
    sep = f" {'-' * (activity_col_width + 2)} "
    for _ in time_points:
        sep += f" {'-' * time_col_width}"
    sep += "\n"
    table = sep + header + sep
    # Build a grid for each row (y = activity, x = time_point)
    for act in activities:
        # Build a list of cells for the timeline
        cells = [" " * time_col_width for _ in time_points]
        try:
            start_idx = time_points.index(act.start)
            end_idx = time_points.index(act.end)
        except ValueError:
            continue  # skip if time not found
        # Draw the bar
        cells[start_idx] = (
            "|" + ("-" * (time_col_width - 2)) + ("|" if start_idx == end_idx else "-")
        )
        for i in range(start_idx + 1, end_idx):
            cells[i] = "-" * time_col_width
        if end_idx > start_idx:
            cells[end_idx] = ("-" * (time_col_width - 2)) + "|"
        # Convert row to string (no column separators)
        row_str = f"  {act.name.ljust(activity_col_width)}  "
        for cell in cells:
            row_str += f" {cell}"
        row_str += "\n"
        table += row_str
    table += sep
    return table


def main():
    st.title("asciitl - ASCII Timeline Table Generator")
    st.markdown(
        "This tool generates an ASCII table from your daily activity timeline. "
        "Input your activities in the format `HH:MM - HH:MM Activity`."
    )

    with st.expander("### How to Use"):
        st.markdown(
            "1. Input your daily activities in the format `HH:MM - HH:MM Activity`."
        )
        st.markdown(
            "2. Each activity should be on a new line, and the time format should be 24-hour."
        )
        st.markdown(
            "Example:\n"
            "```\n"
            "09:00 - 09:15 Morning Routine\n"
            "09:15 - 10:00 Breakfast\n"
            "10:00 - 12:00 Work Session 1\n"
            "12:00 - 13:00 Lunch Break\n"
            "13:00 - 15:00 Work Session 2\n"
            "15:00 - 16:00 Coffee Break\n"
            "16:00 - 18:00 Work Session 3\n"
            "18:00 - 19:00 Evening Routine\n"
            "```"
        )

    sample_input = (
        "09:00 - 09:15 Morning Routine\n"
        "09:15 - 10:00 Breakfast\n"
        "10:00 - 12:00 Work Session 1\n"
        "12:00 - 13:00 Lunch Break\n"
        "13:00 - 15:00 Work Session 2\n"
        "15:00 - 16:00 Coffee Break\n"
        "16:00 - 18:00 Work Session 3\n"
        "18:00 - 19:00 Evening Routine\n"
    )

    text_input = st.text_area("Timeline Input", value=sample_input, height=200)
    if text_input:
        activities = parse_activities(text_input)
        print(f"Parsed Activities: {activities}")
        if not activities:
            st.warning(
                "No valid activities found. Please use the format '09:00 - 09:15 Activity'."
            )
            return
        time_points = get_time_points(activities)
        ascii_table = build_ascii_table(activities, time_points)
        st.text("ASCII Table:")
        st.code(ascii_table, language="text")


if __name__ == "__main__":
    main()
