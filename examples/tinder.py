# pip install locate-pixelcolor-c cv2imshow get-consecutive-filename adbkit kthread-sleep deepcopyall a-pandas-ex_apply-ignore-exceptions openpyxl

import os
import random
from collections import defaultdict
import cv2
from cv2imshow.cv2imshow import cv2_imshow_single
from get_consecutive_filename import get_free_filename
from adbkit import ADBTools
from kthread_sleep import sleep
from deepcopyall import deepcopy


from a_pandas_ex_apply_ignore_exceptions import pd_add_apply_ignore_exceptions
from locate_pixelcolor_c import search_colors

from mydevices import deviceserial

pd_add_apply_ignore_exceptions()
import numpy as np
import pandas as pd


def get_uiautomator_frame(screenshotfolder="c:\\ttscreenshots"):
    if screenshotfolder:
        adb.aa_update_screenshot()
    df = adb.aa_get_all_displayed_items_from_uiautomator(
        screenshotfolder=screenshotfolder,  # screenshots will be saved here
        max_variation_percent_x=10,
        # used for one of the click functions, to not click exactly in the center - more information below
        max_variation_percent_y=10,  # used for one of the click functions, to not click exactly in the center
        loung_touch_delay=(
            1000,
            1500,
        ),  # with this settings longtouch will take somewhere between 1 and 1,5 seconds
        swipe_variation_startx=10,  # swipe coordinate variations in percent
        swipe_variation_endx=10,
        swipe_variation_starty=10,
        swipe_variation_endy=10,
        sdcard="/storage/emulated/0/",
        # sdcard will be used if you use the sendevent methods, don't pass a symlink - more information below
        tmp_folder_on_sd_card="AUTOMAT",  # this folder will be created in the sdcard folder for using sendevent actions
        bluestacks_divider=32767,
        # coordinates must be recalculated for BlueStacks https://stackoverflow.com/a/73733261/15096247 when using sendevent
    )
    return df


def get_pics2(df):
    allscreenshots = []
    adb.aa_update_screenshot()
    allscreenshots.append(adb.screenshot.copy())
    oldpixels = 0
    returnclicks = 0
    for key in range(9):
        df.iloc[0].ff_bb_tap_center_offset(width // 4, 0)
        sleep(0.1)
        adb.aa_update_screenshot()
        pixval = np.sum(adb.screenshot)
        if pixval == oldpixels:
            break
        oldpixels = pixval
        returnclicks += 1
        allscreenshots.append(adb.screenshot.copy())

    for key in range(returnclicks):
        df.iloc[0].ff_bb_tap_center_offset((width // 4) * -1, 0)
        sleep(0.05)

    return np.hstack(allscreenshots)


def save_all_screenshots(df):
    df.dropna(subset="bb_screenshot").ff_bb_save_screenshot.apply(lambda x: x())


def get_all_infos(df):
    try:
        df.loc[df.bb_pure_id == "id/recsDetailArrowUpInfo"].sort_values(
            by="bb_area", ascending=False
        ).ff_bb_tap_exact_center.iloc[0]()
    except Exception as fe:
        print(fe)
    sleep(0.1)
    alldfs = []
    firstdflen = 0
    df3 = pd.DataFrame()
    lastdf = pd.DataFrame()
    for _ in range(10):
        adb.aa_swipe(width // 2, int(height * 0.8), width // 2, int(height * 0.2), 1)
        sleep(0.1)
        alldfs.append(
            deepcopy(get_uiautomator_frame(screenshotfolder=screenshotfolder))
        )
        lastdf = alldfs[-1].copy()
        df3 = pd.concat(alldfs, ignore_index=True)
        df3 = df3.drop_duplicates("bb_keys_hierarchy")
        if len(df3) == firstdflen:
            break
        firstdflen = len(df3)
    df4 = df3.loc[~((df3.bb_text == "") | (df3.bb_text.isna()))].copy()
    df4["keylen"] = df4.bb_keys_hierarchy.str.len()

    df5 = df4.copy()
    df5 = df5.loc[~df5.bb_pure_id.str.contains("section_name", na=False)]
    df5 = df5.loc[~df5.bb_resource_id.isin(forbiddenids)]
    newdict = defaultdict(list)
    for name, group in df5.groupby("keylen"):
        group2 = group.copy()
        group2.bb_pure_id = group2.bb_pure_id.fillna("")
        for key, item in group2.iterrows():
            newcol = (
                item.bb_pure_id.split("/", maxsplit=1)[-1]
                if item.bb_pure_id
                else f"cat_{name}"
            )
            newdict[newcol].append(item.bb_text.replace("\n", "      "))

    for key in newdict:
        newdict[key] = "|||".join(newdict[key])

    return newdict, lastdf


def likes_active():
    while True:
        df = get_uiautomator_frame(screenshotfolder=screenshotfolder)
        picgreen = (
            df.loc[(df.bb_pure_id == "id/gamepad_like") & (df.bb_clickable == True)]
            .sort_values(by="bb_area")
            .iloc[0]
            .bb_screenshot
        )
        co = search_colors(picgreen, heartcolor)
        if len(co) < likelimit:
            adb.aa_force_stop("com.tinder")
            sleep(random.randint(30, 60))
            adb.aa_swipe(300, 400, 300, 300, 1)
            adb.aa_open_app("com.tinder")
            sleep(random.randint(35, 60))
        else:
            break


def show_blurry_picture():
    adb.aa_update_screenshot()
    dst = adb.screenshot.copy()
    for ra in range(30):
        try:
            dst = cv2.GaussianBlur(dst, (width // 55, height // 55), cv2.BORDER_DEFAULT)
        except Exception:
            adb.aa_update_screenshot()
            dst = adb.screenshot.copy()

    cv2_imshow_single(
        title="pic1",
        image=dst,
        killkeys="ctrl+alt+h",  # switch on/off
    )


heartcolor = np.array([[176, 232, 29]], dtype=np.uint8)
likelimit = 100

forbiddenids = [
    "com.tinder:id/recommend_title",
    "com.tinder:id/recommend_subtitle",
    "com.tinder:id/block_user_text",
    "com.tinder:id/block_user_description",
    "com.tinder:id/report_title",
    "com.tinder:id/report_user_subtitle",
    "com.tinder:id/title_text",
]

screenshotfolder = "c:\\ttscreenshots"
if not os.path.exists(screenshotfolder):
    os.makedirs(screenshotfolder)
savefolder = "c:\\titest"
if not os.path.exists(savefolder):
    os.makedirs(savefolder)
ADBTools.aa_kill_all_running_adb_instances() #####
adb_path = r"C:\ProgramData\chocolatey\bin\adb.exe"
adb = ADBTools(adb_path=adb_path, deviceserial=deviceserial)
adb.aa_start_server()  # creates a new process which is not a child process ####
sleep(3)
adb.aa_connect_to_device() ####
width, height = adb.aa_get_screen_resolution()

matchpic = get_free_filename(folder=savefolder, fileextension=".png", leadingzeros=5)
adb.aa_open_app("com.tinder")

if __name__ == "__main__":
    sleep(5)
    while True:
        try:
            likes_active()
            df = get_uiautomator_frame(screenshotfolder=screenshotfolder)
            if not (
                h := df.loc[df.bb_pure_id == "id/its_match_x_dismiss_button"]
            ).empty:
                adb.aa_update_screenshot()
                cv2.imwrite(matchpic, adb.screenshot)
                h.ff_bb_tap_exact_center.iloc[0]()
                sleep(1)
                continue

            alluserpics = get_pics2(df)
            alluserinfos, lastdf = get_all_infos(df)

            fijpg = get_free_filename(
                folder=savefolder, fileextension=".jpg", leadingzeros=5
            )
            fixlsx = get_free_filename(
                folder=savefolder, fileextension=".xlsx", leadingzeros=5
            )
            matchpic = fijpg[:-3] + "png"

            alluserinfos["picture"] = fijpg
            dffinal = pd.DataFrame(pd.Series(alluserinfos)).T
            cv2.imwrite(fijpg, alluserpics)
            dffinal.to_excel(fixlsx)
            lastdf.loc[
                (lastdf.bb_pure_id == "id/gamepad_like") & (lastdf.bb_clickable == True)
            ].sort_values(by="bb_area").iloc[0].ff_bb_tap_exact_center()
        except Exception as fe:
            print(fe)
            adb.aa_force_stop("com.tinder")
            sleep(5)
            adb.aa_open_app("com.tinder")
            sleep(5)

            continue
        except KeyboardInterrupt:
            break
