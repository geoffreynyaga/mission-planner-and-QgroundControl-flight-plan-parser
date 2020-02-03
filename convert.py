import os
import pandas as pd
from typing import Any
from django.contrib.gis.geos import LineString, MultiLineString


def mission_planner_convert_log(url: str) -> list:
    """ This function takes in a string url of the .waypoints, .txt or .json
        file exported from the mission planner flight plan
        It returns an array of coordinates for each point

    Returns:
        [array] -- [
            [long, lat],
            [long, lat],
            ...
        ]
    """

    data = pd.read_table(str(url), delim_whitespace=True)

    df = pd.DataFrame(data)
    df.to_csv("me.csv",)
    datatest = pd.DataFrame((pd.read_csv("me.csv", index_col=0)))
    d = datatest.drop(
        [
            "WPL",
            "Unnamed: 1",
            "Unnamed: 2",
            "Unnamed: 3",
            "Unnamed: 4",
            "Unnamed: 5",
            "Unnamed: 6",
            "Unnamed: 7",
            "110",
        ],
        axis=1,
    )
    z = d[d != 0.0].dropna(axis=0)
    cols = list(z)
    cols[0], cols[1] = cols[1], cols[0]
    f = z.loc[:, cols]
    e = f.values.tolist()

    # print(e)
    return e


# x = mission_planner_convert_log("./mission.waypoints")
# print(x)

# FOR DJANGO USERS
"""We can further convert the above lat/long array into LineString and MultiLineString
format to be used for saving to database as well as displaying on the front-end
"""


def convert_mission_planner_log_to_geoJson(url: str) -> Any:
    """ kindly check how to install these libraries
    https://docs.djangoproject.com/en/3.0/ref/contrib/gis/install/geolibs/
    """
    # GEOS_LIBRARY_PATH = "/home/<your computer username>/local/lib/libgeos_c.so"
    GEOS_LIBRARY_PATH = "/home/nyaga/local/lib/libgeos_c.so"

    output = mission_planner_convert_log(url)
    print(output, "output")
    line = LineString(output)
    print(line, "line")
    multi_line = MultiLineString(line)
    print(multi_line, "multi_line")

    from django.core.serializers import serialize

    return multi_line


# y = convert_mission_planner_log_to_geoJson("./mission.waypoints")
# print(y, "y")


def qgc_convert_log(url: str) -> list:
    import shutil
    import json

    """ This function takes in a string url of the .plan,
        file exported from the QgroundControl flight plan
        It returns an array of coordinates for each point

    Returns:
        [array] -- [
            [long, lat],
            [long, lat],
            ...
        ]
    """
    pre, ext = os.path.splitext(url)

    dest = shutil.copyfile(url, f"./{pre}.json")

    with open(f"{pre}.json") as f:
        data = json.load(f)

        mission_data = data["mission"]
        hover_speed = mission_data["hoverSpeed"]
        cruise_speed = mission_data["cruiseSpeed"]
        planned_home_position = mission_data["plannedHomePosition"]

        mission_waypoints_data = mission_data["items"]

        output: list = []

        for waypoint in mission_waypoints_data:
            lat_long = [waypoint["params"][5], waypoint["params"][4]]
            output.append(lat_long)

    return output


# z = qgc_convert_log("./qgc.plan")
# print(z,"z")


def convert_qgc_log_to_geoJson(url: str) -> Any:
    """ This function converts a qgroundControl .plan to Django Linestring/MultiLineString formats
     kindly check how to install these libraries
    https://docs.djangoproject.com/en/3.0/ref/contrib/gis/install/geolibs/
    """
    # GEOS_LIBRARY_PATH = "/home/<your computer username>/local/lib/libgeos_c.so"
    GEOS_LIBRARY_PATH = "/home/nyaga/local/lib/libgeos_c.so"

    output = qgc_convert_log(url)
    print(output, "output")
    line = LineString(output)
    print(line, "line")
    multi_line = MultiLineString(line)
    print(multi_line, "multi_line")


    return multi_line


z1 = convert_qgc_log_to_geoJson("./qgc.plan")
print("z1")
