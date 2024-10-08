import json
import re
import os

import pandas as pd
from dotenv import load_dotenv

load_dotenv()

gsheetkey = os.getenv("GSHEET_KEY")
url = f"https://docs.google.com/spreadsheet/ccc?key={gsheetkey}&output=xlsx"
pattern = r"^(?:([^|]+) \| ([^|]+) \| ([^|]+))(?: / ([^|]+) \| ([^|]+) \| ([^|]+))?$"


def groups_to_json():
    xls = pd.ExcelFile(url)
    numeric_sheets = [sheet for sheet in xls.sheet_names if sheet.isdigit()]
    with open("groups.json", "w") as file:
        file.write(json.dumps(numeric_sheets, indent=4, ensure_ascii=False))


def extract_lessons_from_schedule(schedule):
    lessons = []
    for index, lesson in enumerate(schedule):
        match = re.match(pattern, str(lesson))
        if match:
            lesson_temp = [match.group(1), match.group(2), match.group(3)]
            if match.group(4):
                lesson_temp += [match.group(4), match.group(5), match.group(6)]
            else:
                lesson_temp += [None, None, None]
        else:
            lesson_temp = [None, None, None, None, None, None]
        temp_data = {
            "number": index + 1,
            "title": lesson_temp[0],
            "teacher": lesson_temp[1],
            "room": lesson_temp[2],
            "title_denom": lesson_temp[3],
            "teacher_denom": lesson_temp[4],
            "room_denom": lesson_temp[5],
        }
        lessons.append(temp_data)
    return lessons


def extract_group_info(group_info):
    return [
        {"message": row.iloc[0], "message_type": row.iloc[1]}
        for index, row in group_info.iterrows()
        if pd.notna(row.iloc[0])
    ]


def main():
    with open("groups.json", "r", encoding="utf-8") as file:
        groups = json.load(file)

    result = {}
    dfs = pd.read_excel(url, sheet_name=groups)

    for group in groups:
        df = dfs[group]
        schedule = df.iloc[0:7, 1:6]
        group_info = df.iloc[0:7, 6:8]

        schedule_json = {}
        for day, data in schedule.items():
            lessons = extract_lessons_from_schedule(data)
            if lessons:
                schedule_json[day] = lessons

        schedule_json["info"] = extract_group_info(group_info)
        result[group] = schedule_json

    # General sheet processing
    df_general = pd.read_excel(url, sheet_name="General")
    general = {
        "warning": df_general["Warning"].dropna().tolist(),
        "info": df_general["Info"].dropna().tolist(),
        "is_numerator": bool(df_general.loc[0, "Is Numerator"]),
    }

    to_json = {
        "groups": result,
        "general": general,
    }

    with open("schedule.json", "w", encoding="utf-8") as file:
        json.dump(to_json, file, indent=4, ensure_ascii=False)
