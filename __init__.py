import glob
import os
import subprocess
from collections import deque, defaultdict
from functools import reduce
from time import sleep
from typing import Union

import a_pandas_ex_adb_execute_activities
import rapidfuzz
from PIL import Image
from a_cv2_shape_finder import (
    get_shapes_using_THRESH_OTSU,
    get_shapes_using_ADAPTIVE_THRESH_MEAN_C,
    get_shapes_using_ADAPTIVE_THRESH_GAUSSIAN_C,
)
from a_pandas_ex_adb_execute_activities import pd_add_adb_execute_activities

from a_pandas_ex_image_tools import pd_add_image_tools
from adb_push_create import push_file, make_folders
from adbescapes import ADBInputEscaped

from adbdevicechanger import AdbChanger
from bstconnect import connect_to_all_localhost_devices
from check_if_nan import is_nan
from cv2imshow.cv2imshow import cv2_imshow_multi
from taskkill import taskkill_regex_rearch
from tesseractmultiprocessing import tesser2df

pd_add_adb_execute_activities()
import kthread
import numpy as np
import cv2
import psutil
import pyperclip
import regex
from a_cv_imwrite_imread_plus import open_image_in_cv
from a_cv2_imshow_thread import add_imshow_thread_to_cv2
from a_pandas_ex_adb_settings_to_df import parse_config_files
from a_pandas_ex_adb_to_df import get_folder_df
from a_pandas_ex_logcat2df import adb_logcat_to_df
from a_pandas_ex_tesseract_multirow_regex_fuzz import (
    pd_add_tesseract,
    pd_add_regex_fuzz_multiline,
)
from adb_grep_search import adb_grep
from adb_unicode_keyboard import AdbUnicodeKeyboard
from androdf import AndroDF
from flatten_everything import flatten_everything
from a_pandas_ex_csv_plus import pd_add_convert_to_df
from getevent_sendevent import GetEventSendEvent
from sendevent_getevent_keyboard import SendEventKeystrokes
from sendevent_touch import SendEventTouch

pd_add_convert_to_df()
from touchtouch import touch
from subprocess_print_and_capture import (
    execute_subprocess_multiple_commands_with_timeout_bin,
    execute_subprocess,
)
import pandas as pd
from a_cv_imwrite_imread_plus import add_imwrite_plus_imread_plus_to_cv2

add_imwrite_plus_imread_plus_to_cv2()
add_imshow_thread_to_cv2()
from a_pandas_ex_apply_ignore_exceptions import pd_add_apply_ignore_exceptions

pd_add_apply_ignore_exceptions()
import sys
from adbblitz import AdbShotUSB, AdbShotTCP, mainprocess

use_root = sys.modules[__name__]

use_root.enabled = False
pd_add_image_tools()

startupinfo = subprocess.STARTUPINFO()
creationflags = 0 | subprocess.CREATE_NO_WINDOW
startupinfo.wShowWindow = subprocess.SW_HIDE
invisibledict = {
    "startupinfo": startupinfo,
    "creationflags": creationflags,
    "start_new_session": True,
}
dequelist = lambda: deque([], 1)
_screenshots = defaultdict(dequelist)


def _draw_shapes_result(image, df, min_area=200):
    for name, group in df.groupby("aa_h3"):
        if name == 0:
            continue
        fabb = (
            np.random.randint(50, 250),
            np.random.randint(50, 250),
            np.random.randint(50, 250),
        )
        for key, item in group.loc[
            (group.aa_area > min_area)
            & (
                group.aa_shape.isin(
                    ["rectangle", "triangle", "circle", "pentagon", "hexagon"]
                )
            )
        ].iterrows():
            image = cv2.drawContours(
                image,
                item.aa_convexHull,
                -1,
                color=fabb,
                thickness=5,
                lineType=cv2.LINE_AA,
            )
            image = cv2.rectangle(
                image,
                (item.aa_bound_start_x, item.aa_bound_start_y),
                (item.aa_bound_end_x, item.aa_bound_end_y),
                (0, 0, 0),
                3,
            )
            image = cv2.rectangle(
                image,
                (item.aa_bound_start_x, item.aa_bound_start_y),
                (item.aa_bound_end_x, item.aa_bound_end_y),
                fabb,
                2,
            )
            image = cv2.putText(
                image,
                f"{str(item.aa_shape)} - {key}",
                (item.aa_bound_start_x, item.aa_bound_start_y),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.4,
                (0, 0, 0),
                2,
                cv2.LINE_AA,
            )
            image = cv2.putText(
                image,
                f"{str(item.aa_shape)} - {key}",
                (item.aa_bound_start_x, item.aa_bound_start_y),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.4,
                fabb,
                1,
                cv2.LINE_AA,
            )
    return image


def execute_multicommands_adb_shell(
    adb_path,
    device_serial,
    subcommands: list,
    exit_keys: str = "ctrl+x",
    print_output=True,
    timeout=None,
):
    if not isinstance(subcommands, list):
        subcommands = [subcommands]
    if use_root.enabled:
        subcommands.insert(0, "su")
    return execute_subprocess_multiple_commands_with_timeout_bin(
        cmd=f"{adb_path} -s {device_serial} shell",
        subcommands=subcommands,
        exit_keys=exit_keys,
        end_of_printline="",
        print_output=print_output,
        timeout=timeout,
    )


def execute_command_adb(adb_path, device_serial, command: str):
    proc = subprocess.run(
        f"{adb_path} -s {device_serial} {command}", capture_output=True
    )

    return (
        proc.stdout.decode("utf-8", "ignore"),
        proc.stderr.decode("utf-8", "ignore"),
        proc.returncode,
    )


def execute_adb_without_shell(
    adb_path,
    command,
    device_serial=None,
    exit_keys="ctrl+x",
    print_output=True,
    timeout=None,
):
    addserial = ""
    add_root = ""
    if device_serial is not None:
        addserial = f"-s {device_serial} "

    return execute_subprocess_multiple_commands_with_timeout_bin(
        cmd=f"""{adb_path} {addserial}{add_root}\"{command}\"""",
        subcommands=[],
        exit_keys=exit_keys,
        end_of_printline="",
        print_output=print_output,
        timeout=timeout,
    )


def connect_to_all_localhost_accounts_in_range(
    adb_path, start=4999, end=6000, timeout=10
):
    kth = [
        kthread.KThread(
            target=execute_subprocess_multiple_commands_with_timeout_bin,
            name=aca,
            args=(
                f"{adb_path} connect localhost:{aca}",
                [],
                "ctrl+x",
                "",
                False,
                timeout,
            ),
        )
        for aca in range(start, end)
    ]
    _ = [i.start() for i in kth]
    sleep(timeout + 2)
    for ac in kth:
        try:
            if ac.is_alive():
                ac.kill()
        except Exception as fe:
            print(fe)
            pass


def get_all_devices(
    adb_path,
    exit_keys="ctrl+x",
    print_output=True,
    timeout=None,
):
    deva = execute_subprocess_multiple_commands_with_timeout_bin(
        cmd=f"{adb_path} devices",
        subcommands=[],
        exit_keys=exit_keys,
        end_of_printline="",
        print_output=print_output,
        timeout=timeout,
    )
    try:
        return pd.DataFrame(
            [x.decode("utf-8", "ignore").strip().split() for x in deva[1:-1]]
        ).rename(columns={0: "deviceserial", 1: "status"})
    except Exception as fe:
        print(fe)
        return deva


def stop_server(
    adb_path,
    exit_keys="ctrl+x",
    print_output=True,
    timeout=None,
):
    return execute_adb_without_shell(
        adb_path,
        command="stop-server",
        exit_keys=exit_keys,
        print_output=print_output,
        timeout=timeout,
    )


def kill_server(
    adb_path,
    exit_keys="ctrl+x",
    print_output=True,
    timeout=None,
):
    return execute_adb_without_shell(
        adb_path,
        command="kill-server",
        exit_keys=exit_keys,
        print_output=print_output,
        timeout=timeout,
    )


def kill_all_running_adbs():
    return taskkill_regex_rearch(
        dryrun=False,
        kill_children=True,
        force_kill=True,
        flags_title=regex.I,
        windowtext=".*",
        flags_windowtext=regex.I,
        class_name=".*",
        flags_class_name=regex.I,
        path=r"\badb.exe$",
        flags_path=regex.I,
    )


def start_server(
    adb_path,
    exit_keys="ctrl+x",
    print_output=True,
    timeout=None,
):
    mainprocess([adb_path, "start-server"])
    # return execute_adb_without_shell(
    #     adb_path,
    #     command="start-server",
    #     exit_keys=exit_keys,
    #     print_output=print_output,
    #     timeout=timeout,
    # )


def reboot_and_listen_to_usb(
    adb_path,
    exit_keys="ctrl+x",
    print_output=True,
    timeout=None,
):
    return execute_adb_without_shell(
        adb_path,
        command="usb",
        exit_keys=exit_keys,
        print_output=print_output,
        timeout=timeout,
    )


def connect_to_adb(adb_path, deviceserial):
    _ = subprocess.run(f"{adb_path} start-server", capture_output=True, shell=False)
    _ = subprocess.run(
        f"{adb_path} connect {deviceserial}", capture_output=True, shell=False
    )


def get_screen_height_width(adb_path, deviceserial):
    try:
        p = subprocess.run(
            rf"{adb_path} -s {deviceserial} shell dumpsys window",
            shell=True,
            capture_output=True,
            **invisibledict,
        )
        screenwidth, screenheight = [
            int(x)
            for x in regex.findall(rb"cur=(\d{,4}x\d{,4}\b)", p.stdout)[0]
            .lower()
            .split(b"x")
        ]
        print(screenheight, screenwidth)

    except Exception:
        screenwidth, screenheight = (
            subprocess.run(
                rf'{adb_path} -s {deviceserial} shell dumpsys window | grep cur= |tr -s " " | cut -d " " -f 4|cut -d "=" -f 2',
                shell=True,
                capture_output=True,
                **invisibledict,
            )
            .stdout.decode("utf-8", "ignore")
            .strip()
            .split("x")
        )
        screenwidth, screenheight = int(screenwidth), int(screenheight)
    return screenwidth, screenheight


def convert_to_ADAPTIVE_THRESH_MEAN_C(im):
    try:
        ima2 = cv2.adaptiveThreshold(
            open_image_in_cv(im, channels_in_output=2),
            255,
            cv2.ADAPTIVE_THRESH_MEAN_C,
            cv2.THRESH_BINARY,
            11,
            2,
        )
        return ima2
    except Exception as fe:
        print(fe)
        return im


def convert_to_ADAPTIVE_THRESH_GAUSSIAN_C(im):
    try:
        ima2 = cv2.adaptiveThreshold(
            open_image_in_cv(im, channels_in_output=2),
            255,
            cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
            cv2.THRESH_BINARY,
            11,
            2,
        )
        return ima2
    except Exception as fe:
        print(fe)
        return im


def convert_to_THRESH_OTSU(im):
    blur = cv2.GaussianBlur(open_image_in_cv(im, channels_in_output=2), (5, 5), 0)
    _, threshg = cv2.threshold(
        blur,
        127,
        255,
        cv2.THRESH_BINARY + cv2.THRESH_OTSU,
    )
    return threshg


def uninstall_apk(
    adb_path,
    deviceserial,
    apk,
    exit_keys="ctrl+x",
    print_output=True,
    timeout=None,
):
    return execute_multicommands_adb_shell(
        adb_path,
        deviceserial,
        subcommands=[f"pm uninstall {apk}"],
        exit_keys=exit_keys,
        print_output=print_output,
        timeout=timeout,
    )


def install_apk_from_hdd(adb_path, deviceserial, savepathapk):
    savepathapk = os.path.normpath(savepathapk)
    subprocess.run(f"{adb_path} -s {deviceserial} install {savepathapk}")


def copy_apk_to_hd(
    adb_path,
    deviceserial,
    packageregex,
    allpackages,
    folder,
    exit_keys="ctrl+x",
    print_output=False,
    timeout=None,
):
    alpa = allpackages.copy()
    alpa = alpa.loc[
        alpa["aa_name"].str.contains(packageregex, regex=True, na=False)
    ].copy()
    alpa["aa_folder"] = alpa.aa_path.str.replace("/[^/]+.apk$", "", regex=True)
    return _apks_to_hdd(
        adb_path,
        deviceserial,
        alpa,
        folder,
        exit_keys=exit_keys,
        print_output=print_output,
        timeout=timeout,
    )


def copy_apks_to_hd(
    adb_path,
    deviceserial,
    allpackages,
    folder,
    exit_keys="ctrl+x",
    print_output=False,
    timeout=None,
):
    alpa = allpackages.copy()
    alpa["aa_folder"] = alpa.aa_path.str.replace("/[^/]+.apk$", "", regex=True)
    return _apks_to_hdd(
        adb_path,
        deviceserial,
        allpackages,
        folder,
        exit_keys=exit_keys,
        print_output=print_output,
        timeout=timeout,
    )


def _apks_to_hdd(
    adb_path,
    deviceserial,
    alpa,
    folder,
    exit_keys="ctrl+x",
    print_output=False,
    timeout=None,
):
    for key, item in alpa.iterrows():
        apppa = item.aa_path
        savefolder = item.aa_name
        sf = os.path.normpath(os.path.join(folder, savefolder))
        sffile = os.path.normpath(os.path.join(sf, apppa.strip("/").split("/")[-1]))

        if not os.path.exists(sf):
            os.makedirs(sf)
        filax = b"".join(
            [
                x.replace(b"\r\n", b"\n")
                for x in execute_multicommands_adb_shell(
                    adb_path,
                    deviceserial,
                    subcommands=[f"cat {apppa}"],
                    exit_keys=exit_keys,
                    print_output=print_output,
                    timeout=timeout,
                )
            ]
        )
        try:
            with open(sffile, mode="wb") as f:
                f.write(filax)
        except Exception:
            continue


def _get_n_adb_screenshots(
    adb_path,
    deviceserial,
    sleeptime=None,
    n=1,
    gray=False,
    ADAPTIVE_THRESH_MEAN_C=False,
    ADAPTIVE_THRESH_GAUSSIAN_C=False,
    THRESH_OTSU=False,
):
    read, write = os.pipe()
    nbin = str(n).encode()
    if sleeptime is None:
        subcommand = (
            b"n=0; while (( n++ < "
            + nbin
            + b" )); do "
            + b"screencap -p\n"
            + b"echo oioioioioioioioi"
            + b"; done"
        )
    else:
        subcommand = (
            b"n=0; while (( n++ < "
            + nbin
            + b" )); do "
            + b"screencap -p\n"
            + b"echo oioioioioioioioi\nsleep "
            + str(sleeptime).encode()
            + b"; done"
        )

    DEVNULL = open(os.devnull, "wb")
    os.write(write, subcommand)

    os.close(write)
    popen = subprocess.Popen(
        f"{adb_path} -s {deviceserial} shell",
        stdin=read,
        stdout=subprocess.PIPE,
        universal_newlines=False,
        stderr=DEVNULL,
        shell=False,
    )
    popenpid = popen.pid
    wholbilist = []
    killit = False
    try:
        for stdout_line in iter(popen.stdout.readline, b""):
            try:
                try:
                    wholbilist.append(stdout_line.replace(b"\r\n", b"\n"))
                    if (wholbilist[-1][-17:]) == b"oioioioioioioioi\n":
                        wholbilist[-1] = wholbilist[-1][:-17]
                        varaba = b"".join(wholbilist)
                        if not gray:
                            bildyield = open_image_in_cv(
                                cv2.imdecode(
                                    np.frombuffer(varaba, np.uint8), cv2.IMREAD_COLOR
                                ),
                                channels_in_output=3,
                            )
                        else:
                            bildyield = open_image_in_cv(
                                cv2.imdecode(
                                    np.frombuffer(varaba, np.uint8), cv2.IMREAD_COLOR
                                ),
                                channels_in_output=2,
                            )
                        if ADAPTIVE_THRESH_MEAN_C:
                            bildyield = convert_to_ADAPTIVE_THRESH_MEAN_C(bildyield)

                        if ADAPTIVE_THRESH_GAUSSIAN_C:
                            bildyield = convert_to_ADAPTIVE_THRESH_GAUSSIAN_C(bildyield)

                        if THRESH_OTSU:
                            bildyield = convert_to_THRESH_OTSU(bildyield)

                        yield bildyield
                        wholbilist = []

                except Exception as fe:
                    print(fe)
                    pass

            except Exception as Fehler:
                print(Fehler)
                continue
            except KeyboardInterrupt:
                killit = True
                break
    except Exception:
        pass
    except KeyboardInterrupt:
        killit = True
    if killit:
        try:
            p = psutil.Process(popenpid)
            p.kill()
        except:
            pass


def adb_path_exists(adb_path, deviceserial, path):
    ex = (
        subprocess.run(
            f"""{adb_path} -s {deviceserial} shell ls {path} > /dev/null 2>&1 && echo "True" || echo "False""",
            shell=False,
            capture_output=True,
        )
        .stdout.decode("utf-8", "ignore")
        .strip()
    )
    if ex == "False":
        return False
    return True


def isfolder(
    adb_path,
    deviceserial,
    path,
    exit_keys: str = "ctrl+x",
    print_output=True,
    timeout=None,
):
    if not adb_path_exists(adb_path, deviceserial, path):
        return False
    isfolder = False
    commands = f"ls -i -H -las -s -d {path}"
    result = execute_multicommands_adb_shell(
        adb_path,
        deviceserial,
        commands,
        exit_keys=exit_keys,
        print_output=print_output,
        timeout=timeout,
    )

    if [x.decode("utf-8", "ignore").split() for x in result][0][2][0] == "d":
        isfolder = True
    return isfolder


def copy_to_sd_card(adb_path, deviceserial, path, sdcard="/sdcard/"):
    execu = rf"push {path} {sdcard}"
    return execute_command_adb(adb_path, deviceserial, execu)


def pull(adb_path, deviceserial, path_pc, path_device="/sdcard/"):
    touch(path_pc)
    execu = rf"pull {path_device} {path_pc}"
    return execute_command_adb(adb_path, deviceserial, execu)


def adb_shell_change_to_folder_and_execute(
    adb_path,
    deviceserial,
    commands,
    folder="/sdcard/",
    exit_keys="ctrl+x",
    print_output=True,
):
    if not isinstance(commands, list):
        commands = [commands]

    subcommands = [f"cd {folder}", "\r"] + commands

    return execute_multicommands_adb_shell(
        adb_path,
        deviceserial,
        subcommands=subcommands,
        exit_keys=exit_keys,
        print_output=print_output,
    )


def adb_open_shell(adb_path, deviceserial):
    subprocess.run(f"start cmd /k {adb_path} -s {deviceserial} shell", shell=True)


def adb_swipe(
    adb_path,
    deviceserial,
    x0,
    y0,
    x1,
    y1,
    delay,
    exit_keys="ctrl+x",
    print_output=True,
    timeout=None,
):
    return execute_multicommands_adb_shell(
        adb_path,
        deviceserial,
        subcommands=[f"input swipe {x0} {y0} {x1} {y1} {delay}"],
        exit_keys=exit_keys,
        print_output=print_output,
        timeout=timeout,
    )


def start_package(
    adb_path,
    deviceserial,
    package,
    exit_keys="ctrl+x",
    print_output=True,
    timeout=None,
):
    return execute_multicommands_adb_shell(
        adb_path,
        deviceserial,
        subcommands=[f"monkey -p {package} 1"],
        exit_keys=exit_keys,
        print_output=print_output,
        timeout=timeout,
    )


def expand_notifications(
    adb_path,
    deviceserial,
    exit_keys="ctrl+x",
    print_output=True,
    timeout=None,
):
    return execute_multicommands_adb_shell(
        adb_path,
        deviceserial,
        subcommands=["cmd statusbar expand-notifications"],
        exit_keys=exit_keys,
        print_output=print_output,
        timeout=timeout,
    )


def expand_settings(
    adb_path,
    deviceserial,
    exit_keys="ctrl+x",
    print_output=True,
    timeout=None,
):
    return execute_multicommands_adb_shell(
        adb_path,
        deviceserial,
        subcommands=["cmd statusbar expand-settings"],
        exit_keys=exit_keys,
        print_output=print_output,
        timeout=timeout,
    )


def list_features(
    adb_path,
    deviceserial,
    exit_keys="ctrl+x",
    print_output=True,
    timeout=None,
):
    fea = execute_multicommands_adb_shell(
        adb_path,
        deviceserial,
        subcommands=["""cmd package list features"""],
        exit_keys=exit_keys,
        print_output=print_output,
        timeout=timeout,
    )
    return pd.DataFrame(
        [x.decode("utf-8", "ignore").strip().split(":", maxsplit=1) for x in fea]
    ).rename(columns={0: "feature", 1: "package"})


def resolve_activity(
    adb_path,
    deviceserial,
    package,
    exit_keys="ctrl+x",
    print_output=True,
    timeout=None,
):
    aca = execute_multicommands_adb_shell(
        adb_path,
        deviceserial,
        subcommands=[f"""cmd package resolve-activity --brief {package}"""],
        exit_keys=exit_keys,
        print_output=print_output,
        timeout=timeout,
    )

    xx = pd.DataFrame(
        flatten_everything(
            [
                x.decode("utf-8", "ignore").strip().split()
                if ini == 0
                else (b"package=" + x).decode("utf-8", "ignore").strip().split()
                for ini, x in enumerate(list(flatten_everything(aca)))
            ]
        )
    )
    return (
        xx[0]
        .str.extractall(r"([^=]+)?=?(.*)")
        .reset_index(drop=True)
        .dropna(how="all")
        .set_index(0)
        .T.reset_index(drop=True)
    )


def enable_autoupdate_for_user(
    adb_path,
    deviceserial,
    exit_keys="ctrl+x",
    print_output=True,
    timeout=None,
):
    return execute_multicommands_adb_shell(
        adb_path,
        deviceserial,
        subcommands=["""pm enable-user com.android.vending"""],
        exit_keys=exit_keys,
        print_output=print_output,
        timeout=timeout,
    )


def enable_autoupdate_for_package(
    adb_path,
    deviceserial,
    package,
    user=0,
    exit_keys="ctrl+x",
    print_output=True,
    timeout=None,
):
    return execute_multicommands_adb_shell(
        adb_path,
        deviceserial,
        subcommands=[f"""pm enable-user –user {user} {package}"""],
        exit_keys=exit_keys,
        print_output=print_output,
        timeout=timeout,
    )


def disable_autoupdate_for_user(
    adb_path,
    deviceserial,
    exit_keys="ctrl+x",
    print_output=True,
    timeout=None,
):
    return execute_multicommands_adb_shell(
        adb_path,
        deviceserial,
        subcommands=["""pm disable-user com.android.vending"""],
        exit_keys=exit_keys,
        print_output=print_output,
        timeout=timeout,
    )


def disable_autoupdate_for_package(
    adb_path,
    deviceserial,
    package,
    user=0,
    exit_keys="ctrl+x",
    print_output=True,
    timeout=None,
):
    return execute_multicommands_adb_shell(
        adb_path,
        deviceserial,
        subcommands=[f"""pm disable-user –user {user} {package}"""],
        exit_keys=exit_keys,
        print_output=print_output,
        timeout=timeout,
    )


def applications_in_use(
    adb_path,
    deviceserial,
    exit_keys="ctrl+x",
    print_output=True,
    timeout=None,
):
    xx = execute_multicommands_adb_shell(
        adb_path,
        deviceserial,
        subcommands=[
            """pm list packages|sed -e "s/package://" 

        |while read x; do 
            cmd package resolve-activity --brief $x \
            |tail -n 1 \
            |grep -v "No activity found" 
        done 
        """
        ],
        exit_keys=exit_keys,
        print_output=print_output,
        timeout=timeout,
    )
    return pd.DataFrame([x.decode("utf-8", "ignore").strip() for x in xx]).rename(
        columns={0: "package"}
    )


def list_disabled_packages(
    adb_path,
    deviceserial,
    exit_keys="ctrl+x",
    print_output=True,
    timeout=None,
):
    xx = execute_multicommands_adb_shell(
        adb_path,
        deviceserial,
        subcommands=[
            """pm list packages -d
        """
        ],
        exit_keys=exit_keys,
        print_output=print_output,
        timeout=timeout,
    )
    return pd.DataFrame([x.decode("utf-8", "ignore").strip() for x in xx]).rename(
        columns={0: "package"}
    )


def list_third_party_packages(
    adb_path,
    deviceserial,
    exit_keys="ctrl+x",
    print_output=True,
    timeout=None,
):
    xx = execute_multicommands_adb_shell(
        adb_path,
        deviceserial,
        subcommands=[
            """pm list packages -3
        """
        ],
        exit_keys=exit_keys,
        print_output=print_output,
        timeout=timeout,
    )
    return (
        pd.DataFrame([x.decode("utf-8", "ignore").strip() for x in xx])
        .rename(columns={0: "package"})["package"]
        .str.extractall(r"^([^:]+):(.*)")
        .reset_index(drop=True)
        .rename(columns={0: "type", 1: "package"})
    )


def uninstall_package(
    adb_path,
    deviceserial,
    package,
    exit_keys="ctrl+x",
    print_output=True,
    timeout=None,
):
    return execute_multicommands_adb_shell(
        adb_path,
        deviceserial,
        subcommands=[f"""pm uninstall --user 0 {package}"""],
        exit_keys=exit_keys,
        print_output=print_output,
        timeout=timeout,
    )


def list_permission_groups(
    adb_path,
    deviceserial,
    exit_keys="ctrl+x",
    print_output=True,
    timeout=None,
):
    xx = execute_multicommands_adb_shell(
        adb_path,
        deviceserial,
        subcommands=["""pm list permission-groups"""],
        exit_keys=exit_keys,
        print_output=print_output,
        timeout=timeout,
    )
    return (
        pd.DataFrame([x.decode("utf-8", "ignore").strip() for x in xx])
        .rename(columns={0: "package"})["package"]
        .str.extractall(r"^([^:]+):(.*)")
        .reset_index(drop=True)
        .rename(columns={0: "type", 1: "package"})
    )


def swipe_close(
    adb_path,
    deviceserial,
    swipecoords=(522, 1647, 522, 90),
    exit_keys="ctrl+x",
    print_output=True,
    timeout=None,
):
    execute_multicommands_adb_shell(
        adb_path,
        deviceserial,
        subcommands=[
            f"input swipe {swipecoords[0]} {swipecoords[1]} {swipecoords[2]} {swipecoords[3]}"
        ],
        exit_keys=exit_keys,
        print_output=print_output,
        timeout=timeout,
    )


def is_screen_unlocked(adb_path, deviceserial):
    adbinfos2 = subprocess.run(
        rf'{adb_path} -s "{deviceserial}" shell dumpsys window',
        capture_output=True,
    ).stdout.decode("utf-8")
    return "mDreamingLockscreen=true" in adbinfos2


def close_all_apps(
    adb_path,
    deviceserial,
    loops=20,
    swipecoords=(522, 1647, 522, 90),
    exit_keys="ctrl+x",
    print_output=True,
    timeout=None,
):
    execute_multicommands_adb_shell(
        adb_path,
        deviceserial,
        subcommands=["input keyevent KEYCODE_APP_SWITCH"],
        exit_keys=exit_keys,
        print_output=print_output,
        timeout=timeout,
    )
    for x in range(loops):
        swipe_close(
            adb_path,
            deviceserial,
            swipecoords=swipecoords,
            exit_keys=exit_keys,
            print_output=print_output,
            timeout=timeout,
        )
        sleep(0.1)


def swipe_up_to_unlock_screen(
    adb_path,
    deviceserial,
    password,
    exit_keys="ctrl+x",
    print_output=True,
    timeout=None,
):
    return execute_multicommands_adb_shell(
        adb_path,
        deviceserial,
        subcommands=[
            f"""input keyevent 26 &&""",
            "input touchscreen swipe 930 1000 930 200 1000",
            f"input text {password}",
            "input keyevent 66",
            """input touchscreen swipe 930 1000 930 200 1000""",
        ],
        exit_keys=exit_keys,
        print_output=print_output,
        timeout=timeout,
    )


def lock_screen(
    adb_path, deviceserial, exit_keys="ctrl+x", print_output=True, timeout=None
):
    return execute_multicommands_adb_shell(
        adb_path,
        deviceserial,
        subcommands=[f"""input keyevent 26"""],
        exit_keys=exit_keys,
        print_output=print_output,
        timeout=timeout,
    )


def adb_press_home(
    adb_path, deviceserial, exit_keys="ctrl+x", print_output=True, timeout=None
):
    return execute_multicommands_adb_shell(
        adb_path,
        deviceserial,
        subcommands=[f"input keyevent KEYCODE_HOME"],
        exit_keys=exit_keys,
        print_output=print_output,
        timeout=timeout,
    )


def adb_press_app_switch(
    adb_path, deviceserial, exit_keys="ctrl+x", print_output=True, timeout=None
):
    return execute_multicommands_adb_shell(
        adb_path,
        deviceserial,
        subcommands=[f"input keyevent KEYCODE_APP_SWITCH"],
        print_output=print_output,
        timeout=timeout,
        exit_keys=exit_keys,
    )


def is_keyboard_shown(adb_path, deviceserial):
    return "mInputShown=true" in subprocess.run(
        f"{adb_path} -s {deviceserial} shell dumpsys input_method",
        capture_output=True,
    ).stdout.decode("utf-8", "ignore")


def hide_keyboard(adb_path, deviceserial):
    while tastaturda := is_keyboard_shown(adb_path, deviceserial):
        print(f"Keyboard shown = {tastaturda}")
        os.system(f"""{adb_path} -s "{deviceserial}" shell input keyevent 111""")
        sleep(1)


def adb_move_to_end_of_line(
    adb_path, deviceserial, exit_keys="ctrl+x", print_output=True, timeout=None
):
    return execute_multicommands_adb_shell(
        adb_path,
        deviceserial,
        subcommands=[f"input keyevent KEYCODE_MOVE_END"],
        exit_keys=exit_keys,
        print_output=print_output,
        timeout=timeout,
    )


def rescann_media(
    adb_path,
    deviceserial,
    folder="/mnt/sdcard/",
    exit_keys="ctrl+x",
    print_output=True,
    timeout=None,
):
    return execute_multicommands_adb_shell(
        adb_path,
        deviceserial,
        subcommands=[
            f"""find {folder} | while read f; do am broadcast -a android.intent.action.MEDIA_SCANNER_SCAN_FILE -d \"file://${{f}}\"; done"""
        ],
        exit_keys=exit_keys,
        print_output=print_output,
        timeout=timeout,
    )


def _get_display_orientation(
    adb_path, deviceserial, exit_keys="ctrl+x", print_output=True, timeout=None
):
    return execute_multicommands_adb_shell(
        adb_path,
        deviceserial,
        subcommands=[
            """dumpsys input | grep 'SurfaceOrientation' | awk '{ print $2 }\'"""
        ],
        exit_keys=exit_keys,
        print_output=print_output,
        timeout=timeout,
    )


def get_display_orientation(
    adb_path, deviceserial, exit_keys="ctrl+x", print_output=True, timeout=None
):
    return int(
        _get_display_orientation(
            adb_path,
            deviceserial,
            exit_keys=exit_keys,
            print_output=print_output,
            timeout=timeout,
        )[0]
        .strip()
        .decode("utf-8", "ignore")
    )


def show_users(
    adb_path, deviceserial, exit_keys="ctrl+x", print_output=True, timeout=None
):
    xx = execute_multicommands_adb_shell(
        adb_path,
        deviceserial,
        subcommands=["pm list users"],
        exit_keys=exit_keys,
        print_output=print_output,
        timeout=timeout,
    )
    return pd.DataFrame(
        [x.decode("utf-8", "ignore").strip() for x in xx if b"{" in x]
    ).rename(columns={0: "userinfo"})


def change_screen_orientation(
    adb_path,
    deviceserial,
    exit_keys="ctrl+x",
    print_output=True,
    timeout=None,
    new_orientation="horizontal_upside_down",
):
    format222 = new_orientation

    if format222 == "horizontal_upside_down" or format222 == 2:
        format_einfuegen = 2

    elif format222 == "vertical" or format222 == 1:
        format_einfuegen = 1

    elif format222 == "horizontal" or format222 == 0:
        format_einfuegen = 0

    elif format222 == "vertical_upside_down" or format222 == 3:
        format_einfuegen = 3
    else:
        format_einfuegen = 0

    orientierung = get_display_orientation(
        adb_path, deviceserial, exit_keys="ctrl+x", print_output=True, timeout=None
    )
    newscreen = int(
        execute_multicommands_adb_shell(
            adb_path,
            deviceserial,
            subcommands=[
                f"""content insert --uri content://settings/system --bind name:s:accelerometer_rotation --bind value:i:0""",
                f"""settings put system accelerometer_rotation 0""",
                f"""content insert --uri content://settings/system --bind name:s:user_rotation --bind value:i:{format_einfuegen}""",
                """dumpsys input | grep 'SurfaceOrientation' | awk '{ print $2 }\'""",
            ],
            exit_keys=exit_keys,
            print_output=print_output,
            timeout=timeout,
        )[0].strip()
    )
    return {"old": orientierung, "new": newscreen}


def adb_turn_screen_compatibility_on(
    adb_path, deviceserial, exit_keys="ctrl+x", print_output=True, timeout=None
):
    return execute_multicommands_adb_shell(
        adb_path,
        deviceserial,
        subcommands=["am screen-compat on"],
        exit_keys=exit_keys,
        print_output=print_output,
        timeout=timeout,
    )


def adb_turn_screen_compatibility_off(
    adb_path, deviceserial, exit_keys="ctrl+x", print_output=True, timeout=None
):
    return execute_multicommands_adb_shell(
        adb_path,
        deviceserial,
        subcommands=["am screen-compat off"],
        exit_keys=exit_keys,
        print_output=print_output,
        timeout=timeout,
    )


def execute_single_line_adb(
    adb_path, deviceserial, command, exit_keys="ctrl+x", timeout=None
):
    return execute_subprocess(
        cmd=f"{adb_path} -s {deviceserial} {command}",
        exit_keys=exit_keys,
        timeout=timeout,
    )


def enable_notifications(adb_path, deviceserial, exit_keys="ctrl+x", timeout=None):
    return execute_single_line_adb(
        adb_path=adb_path,
        deviceserial=deviceserial,
        command="shell settings put global heads_up_notifications_enabled 1",
        exit_keys=exit_keys,
        timeout=timeout,
    )


def disable_notifications(adb_path, deviceserial, exit_keys="ctrl+x", timeout=None):
    return execute_single_line_adb(
        adb_path=adb_path,
        deviceserial=deviceserial,
        command="shell settings put global heads_up_notifications_enabled 0",
        exit_keys=exit_keys,
        timeout=timeout,
    )


def disconnect(adb_path, deviceserial, exit_keys="ctrl+x", timeout=None):
    return execute_single_line_adb(
        adb_path=adb_path,
        deviceserial=deviceserial,
        command="disconnect",
        exit_keys=exit_keys,
        timeout=timeout,
    )


def remove_file(adb_path, deviceserial, file, exit_keys="ctrl+x", timeout=None):
    return execute_single_line_adb(
        adb_path=adb_path,
        deviceserial=deviceserial,
        command=f"shell rm -f {file}",
        exit_keys=exit_keys,
        timeout=timeout,
    )


def take_a_picture(
    adb_path,
    deviceserial,
    sleeptime=2,
    exit_keys="ctrl+x",
    print_output=True,
    timeout=None,
):
    return execute_multicommands_adb_shell(
        adb_path,
        deviceserial,
        subcommands=[
            """am start -a android.media.action.STILL_IMAGE_CAMERA""",
            f"sleep {sleeptime}",
            "input keyevent 27",
        ],
        exit_keys=exit_keys,
        print_output=print_output,
        timeout=timeout,
    )


def get_all_broadcasts(
    adb_path, deviceserial, exit_keys="ctrl+x", print_output=True, timeout=None
):
    xx = execute_multicommands_adb_shell(
        adb_path,
        deviceserial,
        subcommands=["""dumpsys activity broadcasts"""],
        exit_keys=exit_keys,
        print_output=print_output,
        timeout=timeout,
    )
    df = pd.DataFrame(xx)
    df[0] = df[0].str.decode("utf-8", "ignore").str.rstrip()
    return df


def get_all_broadcasts_history(
    adb_path, deviceserial, exit_keys="ctrl+x", print_output=True, timeout=None
):
    xx = execute_multicommands_adb_shell(
        adb_path,
        deviceserial,
        subcommands=["""dumpsys activity broadcasts history"""],
        exit_keys=exit_keys,
        print_output=print_output,
        timeout=timeout,
    )
    df = pd.DataFrame(xx)
    df[0] = df[0].str.decode("utf-8", "ignore").str.rstrip()
    return df


def start_gallery(
    adb_path, deviceserial, exit_keys="ctrl+x", print_output=True, timeout=None
):
    return execute_multicommands_adb_shell(
        adb_path,
        deviceserial,
        subcommands=["""am start -t image/* -a android.intent.action.VIEW"""],
        exit_keys=exit_keys,
        print_output=print_output,
        timeout=timeout,
    )


def open_website(
    adb_path, deviceserial, url, exit_keys="ctrl+x", print_output=True, timeout=None
):
    url = _format_url(url)
    return execute_multicommands_adb_shell(
        adb_path,
        deviceserial,
        subcommands=[
            f'''am start -a android.intent.action.VIEW -c android.intent.category.BROWSABLE -d "{url}"'''
        ],
        exit_keys=exit_keys,
        print_output=print_output,
        timeout=timeout,
    )


def _format_url(url):
    ishttps = (
        regex.search(r"^\s*https", url.lower(), flags=regex.IGNORECASE) is not None
    )
    withouthttps = (
        regex.sub(r"^\s*https?://", "", url, flags=regex.IGNORECASE)
    ).strip()
    if not ishttps:
        wholelink = "http://" + withouthttps
    else:
        wholelink = "https://" + withouthttps
    print(wholelink)
    return wholelink


def list_memory(
    adb_path, deviceserial, exit_keys="ctrl+x", print_output=True, timeout=None
):
    xx = execute_multicommands_adb_shell(
        adb_path,
        deviceserial,
        ["""dumpsys meminfo"""],
        exit_keys=exit_keys,
        print_output=print_output,
        timeout=timeout,
    )
    df = pd.DataFrame(xx)
    df[0] = df[0].apply(lambda x: x.decode("utf-8", "ignore")).str.rstrip()

    df[0] = df.loc[
        df[0].str.contains(r"^Total.*\bby\b.*:")
        | df[0].str.contains(r"^\s+[\d,]+[A-Z]+:")
    ]
    df = df.dropna().reset_index(drop=True)
    df[1] = df[0].str.extract(r"(^Total.*\bby\b.*):").ffill()
    spli = df[0].str.split(":", expand=True, n=1)
    df = pd.concat([df, spli].copy(), axis=1, ignore_index=True)
    df = df.loc[~df[3].str.contains(r"^\s*$")]

    df[4] = df[3].str.extract(r"\(pid\s+(\d+)").astype("Int64")
    df[5] = df[3].str.extract(r"^((?!.*?\bpid\b).*)").ffill()

    df = df.loc[~(df[4].isna() & (df[1] != "Total PSS by category"))]
    df[2] = df[2].str.strip()
    defs = {
        "k": 1024,
        "kb": 1024,
        "m": 1024**2,
        "mb": 1024**2,
        "g": 1024**3,
        "gb": 1024**3,
        "t": 1024**4,
        "tb": 1024**4,
    }
    df[2] = (
        df[2]
        .str.replace(",", "", regex=False)
        .str.lower()
        .apply(
            lambda sizes: tuple(
                flatten_everything(regex.findall(r"(\d+)([A-Za-z]+$)", sizes))
            )
        )
    )
    df[2] = df[2].apply(lambda x: float(x[0]) * defs[x[1]]).astype("Int64")
    df = (
        df.drop(columns=0)
        .reset_index(drop=True)
        .rename(
            columns={
                1: "aa_grouped",
                2: "aa_size",
                3: "aa_name",
                4: "aa_pid",
                5: "aa_grouped2",
            }
        )
        .fillna(pd.NA)
    )
    return df


def getprop(
    adb_path, deviceserial, exit_keys="ctrl+x", print_output=True, timeout=None
):
    xx = execute_multicommands_adb_shell(
        adb_path,
        deviceserial,
        subcommands=["""getprop"""],
        exit_keys=exit_keys,
        print_output=print_output,
        timeout=timeout,
    )
    daxz = pd.DataFrame(
        [regex.split(r"[\]:]\s*\[", x.decode("utf-8", "ignore").strip()) for x in xx]
    )
    daxz[0] = daxz[0].str.strip().str.strip(" []")
    daxz[1] = daxz[1].str.strip().str.strip(" []")
    daxz.columns = ["aa_key", "aa_value"]
    return daxz


def activate_root(
    adb_path, deviceserial, exit_keys="ctrl+x", print_output=True, timeout=None
):
    if isroot(
        adb_path,
        deviceserial,
        exit_keys=exit_keys,
        print_output=print_output,
        timeout=timeout,
    ):
        use_root.enabled = True
    else:
        use_root.enabled = False


def isroot(adb_path, deviceserial, exit_keys="ctrl+x", print_output=True, timeout=None):
    roa = execute_multicommands_adb_shell(
        adb_path,
        deviceserial,
        subcommands=[
            f"""which su -- &> /dev/null
    if [[ $? = "0" ]]; then
        echo "True"
    else
        echo "False"
    fi"""
        ],
        exit_keys=exit_keys,
        print_output=print_output,
        timeout=timeout,
    )
    isrooted = False
    if roa[0].decode("utf-8", "ignore").strip() == "True":
        isrooted = True
    return isrooted


def list_pids(
    adb_path,
    deviceserial,
    complete=True,
    exit_keys="ctrl+x",
    print_output=True,
    timeout=None,
):
    xx = execute_multicommands_adb_shell(
        adb_path,
        deviceserial,
        subcommands=["""ps"""],
        exit_keys=exit_keys,
        print_output=print_output,
        timeout=timeout,
    )
    df = pd.DataFrame(
        [x.decode("utf-8", "ignore").strip().split(maxsplit=8) for x in xx[1:]]
    )
    for col in df.columns:
        try:
            df[col] = df[col].ds_string_to_best_dtype()
        except Exception:
            pass
    df.columns = ["USER", "PID", "PPID", "VSIZE", "RSS", "WCHAN", "PC", "NAME", "PATH"]
    if complete and isroot(adb_path, deviceserial):
        allthera = df["PID"].apply(
            lambda x: (
                [
                    x.decode("utf-8", "ignore").strip()
                    for x in execute_multicommands_adb_shell(
                        adb_path,
                        deviceserial,
                        subcommands=[f"""su -- lsof -p {x}"""],
                        exit_keys=exit_keys,
                        print_output=print_output,
                        timeout=timeout,
                    )
                ]
            )
        )
        df2 = pd.Q_convert_to_df(
            string_table=["\n".join(x) for x in allthera.to_list()],
            regex_sep=r"\s+",
            tolerance=1,
        )
        df2.columns = df2.iloc[0].to_list().copy()
        df = df2.loc[~(df2["COMMAND"] == "COMMAND")].reset_index(drop=True).copy()
    return df


def list_all_devices(
    adb_path, deviceserial, exit_keys="ctrl+x", print_output=True, timeout=None
):
    return pd.DataFrame(
        [
            x.decode("utf-8", "ignore").strip()
            for x in execute_multicommands_adb_shell(
                adb_path,
                deviceserial,
                subcommands=[f"""ls sys/module/"""],
                exit_keys=exit_keys,
                print_output=print_output,
                timeout=timeout,
            )
        ]
    )


def open_camera_photo_mode(
    adb_path, deviceserial, exit_keys="ctrl+x", print_output=True, timeout=None
):
    return execute_multicommands_adb_shell(
        adb_path,
        deviceserial,
        subcommands=[f"""am start -a android.media.action.IMAGE_CAPTURE"""],
        exit_keys=exit_keys,
        print_output=print_output,
        timeout=timeout,
    )


def get_procstats(
    adb_path, deviceserial, exit_keys="ctrl+x", print_output=True, timeout=None
):
    xx = execute_multicommands_adb_shell(
        adb_path,
        deviceserial,
        subcommands=[f"""su -- dumpsys procstats"""],
        exit_keys=exit_keys,
        print_output=print_output,
        timeout=timeout,
    )
    allda = []
    for dfra in [
        pd.Q_convert_to_df(
            string_table="\n".join(
                [
                    regex.sub(
                        r"^\s+\*\s+", "Pack: ".ljust(109), k.decode("utf-8", "ignore")
                    )
                    for k in i.splitlines()
                    if regex.findall(r"^\s+", k.decode("utf-8", "ignore"))
                ]
            )
        )
        for i in regex.split(rb"[\r\n]+\s*[\r\n]+\s*[\r\n]+", b"".join(xx))
    ]:
        dfra.columns = range(dfra.shape[1])
        delcol = None
        for col in dfra.columns:
            if not dfra.loc[dfra[col] == "Pack:"].empty:
                delcol = col
                dfra.loc[
                    dfra[dfra.columns[-1]].str.contains(r"^\s*$"), dfra.columns[-1]
                ] = pd.NA
                dfra[dfra.columns[-1]] = (
                    dfra[dfra.columns[-1]].ffill().str.rstrip(":").copy()
                )
                dfra = dfra.loc[~(dfra[0] == "Pack:")].copy()

            dfra[col] = dfra[col].str.rstrip(": ")
        if delcol is not None:
            dfra = dfra.drop(columns=delcol).copy()
        allda.append(dfra.copy())
    return allda


def get_all_activities_from_all_packages(
    adb_path, deviceserial, exit_keys="ctrl+x", print_output=True, timeout=None
):
    allaca = []
    allpa = execute_multicommands_adb_shell(
        adb_path,
        deviceserial,
        subcommands=[f"""pm -l"""],
        exit_keys=exit_keys,
        print_output=print_output,
        timeout=timeout,
    )
    for package in allpa:
        package = package.decode("utf-8", "ignore").strip().split(":", maxsplit=1)[-1]
        xx = execute_multicommands_adb_shell(
            adb_path,
            deviceserial,
            subcommands=[
                f"""dumpsys package \
                |grep -Eo "^[[:space:]]+[0-9a-f]+[[:space:]]+{package}/[^[:space:]]+" \
                |grep -oE "[^[:space:]]+$"
            {package}
            """
            ],
            exit_keys=exit_keys,
            print_output=print_output,
            timeout=timeout,
        )
        if xx:
            dacas = pd.DataFrame(xx)
            dacas[0] = dacas[0].apply(lambda x: x.decode("utf-8", "ignore").strip())
            dacas.columns = ["aa_activity"]
            dacas["aa_package"] = package
            allaca.append(dacas.copy())
    daxc = pd.concat(allaca).drop_duplicates().reset_index(drop=True)
    return daxc.copy()


def get_all_receivers_from_all_packages(
    adb_path, deviceserial, exit_keys="ctrl+x", print_output=True, timeout=None
):
    allaca = []
    allpa = execute_multicommands_adb_shell(
        adb_path,
        deviceserial,
        subcommands=[f"""pm -l"""],
        exit_keys=exit_keys,
        print_output=print_output,
        timeout=timeout,
    )
    for package in allpa:
        package = package.decode("utf-8", "ignore").strip().split(":", maxsplit=1)[-1]
        xx = execute_multicommands_adb_shell(
            adb_path,
            deviceserial,
            subcommands=[
                f"""dumpsys package \
    |grep -Eo "^[[:space:]]+[0-9a-f]+[[:space:]]+{package}/[^[:space:]]+"
    |grep -oE "[^[:space:]]+Receiver"
"""
            ],
            exit_keys=exit_keys,
            print_output=print_output,
            timeout=timeout,
        )
        if xx:
            dacas = pd.DataFrame(xx)
            dacas[0] = dacas[0].apply(lambda x: x.decode("utf-8", "ignore").strip())
            dacas.columns = ["aa_activity"]
            dacas["aa_package"] = package
            allaca.append(dacas.copy())
    daxc = pd.concat(allaca).drop_duplicates().reset_index(drop=True)
    splitti = daxc.aa_activity.str.split(n=1, expand=True).rename(
        columns={0: "aa_hex", 1: "aa_receiver"}
    )
    daxc = pd.concat([splitti, daxc.aa_package].copy(), axis=1)
    return daxc.copy()


def get_all_services_from_all_packages(
    adb_path, deviceserial, exit_keys="ctrl+x", print_output=True, timeout=None
):
    allaca = []
    allpa = execute_multicommands_adb_shell(
        adb_path,
        deviceserial,
        subcommands=[f"""pm -l"""],
        exit_keys=exit_keys,
        print_output=print_output,
        timeout=timeout,
    )
    for package in allpa:
        package = package.decode("utf-8", "ignore").strip().split(":", maxsplit=1)[-1]
        xx = execute_multicommands_adb_shell(
            adb_path,
            deviceserial,
            subcommands=[
                f"""dumpsys package \
            |grep -Eo "^[[:space:]]+[0-9a-f]+[[:space:]]+{package}/[^[:space:]]+" \
            |grep -oE "[^[:space:]]+.*Service"
        """
            ],
            exit_keys=exit_keys,
            print_output=print_output,
            timeout=timeout,
        )
        if xx:
            dacas = pd.DataFrame(xx)
            dacas[0] = dacas[0].apply(lambda x: x.decode("utf-8", "ignore").strip())
            dacas.columns = ["aa_activity"]
            dacas["aa_package"] = package
            allaca.append(dacas.copy())
    daxc = pd.concat(allaca).drop_duplicates().reset_index(drop=True)
    splitti = daxc.aa_activity.str.split(n=1, expand=True).rename(
        columns={0: "aa_hex", 1: "aa_service"}
    )
    daxc = pd.concat([splitti, daxc.aa_package].copy(), axis=1)
    return daxc.copy()


def get_all_activities_from_device(
    adb_path,
    deviceserial,
    exit_keys="ctrl+x",
    print_output=True,
    timeout=None,
):
    allaca = []

    xx = execute_multicommands_adb_shell(
        adb_path,
        deviceserial,
        subcommands=[
            """dumpsys package \
    |grep -Eo "^[[:space:]]+[0-9a-f]+[[:space:]]+.*/[^[:space:]]+" 
    |grep -oE "[^[:space:]]+$"
"""
        ],
        exit_keys=exit_keys,
        print_output=print_output,
        timeout=timeout,
    )
    if xx:
        dacas = pd.DataFrame(xx)
        dacas[0] = dacas[0].apply(lambda x: x.decode("utf-8", "ignore").strip())
        dacas.columns = ["aa_activity"]
        allaca.append(dacas.copy())
    daxc = pd.concat(allaca).drop_duplicates().reset_index(drop=True)
    daxc = daxc.aa_activity.str.split(n=1, expand=True).rename(
        columns={0: "aa_hex", 1: "aa_activity"}
    )
    return daxc.copy()


def get_broadcast_stats(
    adb_path,
    deviceserial,
    exit_keys="ctrl+x",
    print_output=True,
    timeout=None,
):
    xx = execute_multicommands_adb_shell(
        adb_path,
        deviceserial,
        subcommands=[
            """dumpsys activity broadcast-stats
            """
        ],
        exit_keys=exit_keys,
        print_output=print_output,
        timeout=timeout,
    )
    df = pd.DataFrame(
        [
            x.decode("utf-8", "ignore").rstrip()
            if x.decode("utf-8", "ignore").rstrip()[:6] == "      "
            else "Package:" + x.decode("utf-8", "ignore").rstrip().strip(":")
            for x in xx
            if regex.search(r"^\s{4,}", x.decode("utf-8", "ignore").rstrip())
            is not None
        ]
    )[0].str.split(":", n=1, expand=True)
    for col in df.columns:
        df[col] = df[col].str.strip()
    df[2] = pd.NA
    df.loc[(df[0] == "Package"), 2] = df.loc[(df[0] == "Package"), 1]
    df[2] = df[2].ffill()
    df = df.loc[~(df[0] == "Package")].reset_index(drop=True)
    return df


def get_pending_intent(
    adb_path, deviceserial, exit_keys="ctrl+x", print_output=True, timeout=None
):
    xx = execute_multicommands_adb_shell(
        adb_path,
        deviceserial,
        subcommands=[
            """dumpsys activity i
            """
        ],
        exit_keys=exit_keys,
        print_output=print_output,
        timeout=timeout,
    )
    df = pd.DataFrame(
        [
            [z.decode("utf-8", "ignore") for z in y.splitlines()]
            for y in regex.split(rb"[\r\n]\s+\*\s+", b"".join(xx))
        ]
    )
    df1 = df[0].str.split(r"[\s\{\}]+", n=4, expand=True)[[1, 2, 3]]
    df = pd.concat(
        [df1, df[1].str.strip(), df[2].str.strip()], axis=1, ignore_index=True
    )
    return df


def all_dumpsys_to_df(
    adb_path, deviceserial, exit_keys="ctrl+x", print_output=True, timeout=None
):
    def get_not_wanted(x, b):
        return x.loc[
            (x[b].isna())
            | (x[b].str.contains(r":\s*$", regex=True, flags=regex.I, na=False))
        ]

    def arrangestring(x):
        try:
            return (regex.search(r"^\s+", x).end(), x) if x[0] == " " else (0, x)
        except Exception:
            return (0, x)

    def get_space(o):
        if regex.search(rb"^[\n\r\s]*$", o) is not None:
            o = b"                                   "
        try:
            return str(regex.search(rb"^\s+", o).end() * "|\\//").encode()
        except Exception:
            return b"|\\//--------"

    def check_curly_braces(x):
        try:
            if x.count("{") != x.count("}"):
                return x.replace("{", " ").replace("}", " ")
            return x
        except Exception:
            return pd.NA

    xx = execute_multicommands_adb_shell(
        adb_path,
        deviceserial,
        subcommands=["""dumpsys -l"""],
        exit_keys=exit_keys,
        print_output=print_output,
        timeout=timeout,
    )
    bi = [x_.decode("utf-8", "ignore").strip() for x_ in xx][1:]

    alldu = [
        b"".join(
            [
                x.encode() + b"|\\//" + str(len(o)).encode() + get_space(o) + o
                for o in execute_multicommands_adb_shell(
                    adb_path,
                    deviceserial,
                    subcommands=[f"""dumpsys {x} -c"""],
                    exit_keys=exit_keys,
                    print_output=print_output,
                    timeout=timeout,
                )
            ]
        )
        for x in bi
    ]

    alldumps = []
    for __ in enumerate(alldu):
        daxa = [
            [fg.decode("utf-8", "ignore") for fg in y.split(b"|\\//")]
            for y in alldu[__[0]].splitlines()
        ]
        df = pd.DataFrame(daxa)

        l = df.dropna().index.to_list()
        l_mod = [0] + l + [max(l) + 1]
        list_of_dfs = [df.iloc[l_mod[n] : l_mod[n + 1]] for n in range(len(l_mod) - 1)]
        list_of_dfs = [
            x.rename(columns={v: k for k, v in enumerate(x.columns)}).copy()
            for x in list_of_dfs
            if not x.drop(columns=[0, 1]).empty
        ]
        alldumpssub = []
        for l in list_of_dfs:
            er = list(
                sorted(
                    [arrangestring(x) for x in (l[2].value_counts().index.to_list())]
                )
            )[1:]
            if er:
                er = [x[1] for x in er]
                l2 = l.loc[~(l[2].isin(er))].copy()
                alldumpssub.append(l2.copy())
        alldumps.append(alldumpssub.copy())

    filt2 = []
    for dum in alldumps:
        filt2sub = []
        for dafs in dum:
            dafs2 = dafs.copy()
            for col in dafs:
                dafs2[col] = dafs2[col].apply(str)
                dafs2[col] = dafs2[col].replace(
                    r"^\s*$", "-------------------", regex=True
                )
                dafs2[col] = dafs2[col].replace({r"-------------------": pd.NA})
                dafs2[col] = dafs2[col].ffill()
                dafs2[col] = dafs2[col].replace({r"None": pd.NA})
                dafs2[col] = dafs2[col].apply(check_curly_braces)
            if len(dafs2) < 2:
                continue
            try:
                dafs2 = dafs2.dropna(how="all", axis=1)

                dafs2 = dafs2.dropna(subset=dafs2.columns[3:], how="all")
                if dafs2.empty:
                    continue
                filt2sub.append(dafs2.copy())
            except Exception as fe:
                continue
        filt2.append(filt2sub.copy())

    fil3 = []
    for dum in filt2:
        filt3sub = []
        for dafs in dum:
            dafs2 = reduce(get_not_wanted, dafs.columns[3:], dafs).index.to_list()
            gu = dafs.loc[dafs.index.symmetric_difference(dafs2)].copy().drop(columns=1)

            for col in gu.columns:
                gu[col] = gu[col].str.strip()

            gu = gu.replace({"": pd.NA})
            gu.columns = range(gu.shape[1])
            gu = gu.dropna(subset=gu.columns[2:], how="all")
            if not gu.empty:
                filt3sub.append(gu.copy())

        fil3.append(filt3sub.copy())
    fil3 = [x for x in fil3 if len(x) > 0]

    grox = []
    for sub1 in fil3:
        for sub2 in sub1:
            groupbycol = 1
            groupbydf = (
                (
                    sub2.groupby(groupbycol)
                    .agg({k: lambda x: [y for y in x] for k in sub2.columns})
                    .copy()
                )
                .drop(columns=1)
                .copy()
            )
            try:
                groupbydf[0] = groupbydf[0].iloc[0][0]
            except Exception:
                continue
            groupbydf.columns = range(groupbydf.shape[1])

            grox.append(groupbydf.copy())

    no2 = pd.concat(grox)
    dfno2 = (
        no2.drop(columns=0)
        .reset_index(drop=True)
        .set_index(
            pd.MultiIndex.from_frame(no2[0].to_frame().reset_index().filter([0, 1]))
        )
    )
    for col in dfno2.columns:
        dfno2[col] = (
            dfno2[col]
            .apply(
                lambda x: [y for y in x if not pd.isna(y)]
                if isinstance(x, list)
                else pd.NA
            )
            .replace()
            .apply(lambda j: pd.NA if isinstance(j, list) and str(j) == "[]" else j)
        )
    dfno2 = dfno2.explode(1).copy()
    return dfno2


def get_content(
    adb_path,
    deviceserial,
    type_="text/plain",
    exit_keys="ctrl+x",
    print_output=True,
    timeout=None,
):
    return execute_multicommands_adb_shell(
        adb_path,
        deviceserial,
        subcommands=[
            f"""am start  \
        -a android.intent.action.GET_CONTENT \
        -t {type_}"""
        ],
        exit_keys=exit_keys,
        print_output=print_output,
        timeout=timeout,
    )


def press_delete_key_repeated_times(
    adb_path,
    deviceserial,
    repeat=5,
    exit_keys="ctrl+x",
    print_output=True,
    timeout=None,
):
    listpress = ["""input keyevent --longpress $(printf 'KEYCODE_DEL %.0s' {1..50})"""]
    listpress = repeat * listpress
    subc = ["""input keyevent KEYCODE_MOVE_END"""] + listpress
    return execute_multicommands_adb_shell(
        adb_path,
        deviceserial,
        subcommands=subc,
        exit_keys=exit_keys,
        print_output=print_output,
        timeout=timeout,
    )


def go_to_main_screen(
    adb_path,
    deviceserial,
    exit_keys="ctrl+x",
    print_output=True,
    timeout=None,
):
    return execute_multicommands_adb_shell(
        adb_path,
        deviceserial,
        subcommands=[
            """am start  \
            -W -c android.intent.category.HOME  \
            -a android.intent.action.MAIN
        """
        ],
        exit_keys=exit_keys,
        print_output=print_output,
        timeout=timeout,
    )


def add_new_contact(
    adb_path,
    deviceserial,
    name,
    phone,
    email,
    address,
    save=True,
    exit_keys="ctrl+x",
    print_output=True,
    timeout=None,
):
    reas = execute_multicommands_adb_shell(
        adb_path,
        deviceserial,
        subcommands=[
            f"""am start -a android.intent.action.INSERT \
        -t vnd.android.cursor.dir/contact \
        -e name '{name}' \
        -e phone '+{phone}'  \
        -e email '{email}' \
        -e postal '{address}\'"""
        ],
        exit_keys=exit_keys,
        print_output=print_output,
        timeout=timeout,
    )
    if save:
        return execute_multicommands_adb_shell(
            adb_path,
            deviceserial,
            subcommands=[f"""input keyevent 4"""],
            exit_keys=exit_keys,
            print_output=print_output,
            timeout=timeout,
        )
    return reas


def enable_roblox_textures(
    adb_path,
    deviceserial,
    exit_keys="ctrl+x",
    print_output=True,
    timeout=None,
):
    return execute_multicommands_adb_shell(
        adb_path,
        deviceserial,
        subcommands=[
            """su -c mv /data/data/com.roblox.client/app_assets/content/textures/particles1 /data/data/com.roblox.client/app_assets/content/textures/particles""",
            """su -c mv /data/data/com.roblox.client/app_assets/content/sky1 /data/data/com.roblox.client/app_assets/content/sky""",
            """su -c mv /data/data/com.roblox.client/app_assets/android/terrain1 /data/data/com.roblox.client/app_assets/android/terrain""",
            """su -c mv /data/data/com.roblox.client/app_assets/android/textures1 /data/data/com.roblox.client/app_assets/android/textures""",
        ],
        exit_keys=exit_keys,
        print_output=print_output,
        timeout=timeout,
    )


def disable_roblox_textures(
    adb_path,
    deviceserial,
    exit_keys="ctrl+x",
    print_output=True,
    timeout=None,
):
    return execute_multicommands_adb_shell(
        adb_path,
        deviceserial,
        subcommands=[
            """su -c mv /data/data/com.roblox.client/app_assets/content/textures/particles /data/data/com.roblox.client/app_assets/content/textures/particles1""",
            """su -c mv /data/data/com.roblox.client/app_assets/content/sky /data/data/com.roblox.client/app_assets/content/sky1""",
            """su -c mv /data/data/com.roblox.client/app_assets/android/terrain /data/data/com.roblox.client/app_assets/android/terrain1""",
            """su -c mv /data/data/com.roblox.client/app_assets/android/textures /data/data/com.roblox.client/app_assets/android/textures1""",
        ],
        exit_keys=exit_keys,
        print_output=print_output,
        timeout=timeout,
    )


def set_inactive(
    adb_path,
    deviceserial,
    package,
    exit_keys="ctrl+x",
    print_output=True,
    timeout=None,
):
    return execute_multicommands_adb_shell(
        adb_path,
        deviceserial,
        subcommands=[f"am set-inactive {package}"],
        exit_keys=exit_keys,
        print_output=print_output,
        timeout=timeout,
    )


def set_active(
    adb_path,
    deviceserial,
    package,
    exit_keys="ctrl+x",
    print_output=True,
    timeout=None,
):
    return execute_multicommands_adb_shell(
        adb_path,
        deviceserial,
        subcommands=[f"am set-inactive {package} false"],
        exit_keys=exit_keys,
        print_output=print_output,
        timeout=timeout,
    )


def allow_read_clipboard(
    adb_path,
    deviceserial,
    package,
    exit_keys="ctrl+x",
    print_output=True,
    timeout=None,
):
    return execute_multicommands_adb_shell(
        adb_path,
        deviceserial,
        subcommands=[f"cmd appops set {package} READ_CLIPBOARD allow"],
        exit_keys=exit_keys,
        print_output=print_output,
        timeout=timeout,
    )


def ignore_read_clipboard(
    adb_path,
    deviceserial,
    package,
    exit_keys="ctrl+x",
    print_output=True,
    timeout=None,
):
    return execute_multicommands_adb_shell(
        adb_path,
        deviceserial,
        subcommands=[f"cmd appops set {package} READ_CLIPBOARD ignore"],
        exit_keys=exit_keys,
        print_output=print_output,
        timeout=timeout,
    )


def paste_clipboard(
    adb_path,
    deviceserial,
    exit_keys="ctrl+x",
    print_output=True,
    timeout=None,
):
    return execute_multicommands_adb_shell(
        adb_path,
        deviceserial,
        subcommands=[f"input keyevent PASTE"],
        exit_keys=exit_keys,
        print_output=print_output,
        timeout=timeout,
    )


def list_all_packages(
    adb_path,
    deviceserial,
    exit_keys="ctrl+x",
    print_output=True,
    timeout=None,
):
    xx = execute_multicommands_adb_shell(
        adb_path,
        deviceserial,
        subcommands=["""pm list packages -f"""],
        exit_keys=exit_keys,
        print_output=print_output,
        timeout=timeout,
    )
    return pd.DataFrame(
        [regex.split(r"[:=]+", x.decode("utf-8", "ignore").strip())[1:] for x in xx]
    ).rename(columns={0: "aa_path", 1: "aa_name"})


def connect_to_all_bluestacks_hyperv_devices(
    adb_path,
    timeout=10,
    bluestacks_config=r"C:\ProgramData\BlueStacks_nxt\bluestacks.conf",
):
    df = connect_to_all_localhost_devices(
        adb_path=adb_path,
        timeout=timeout,
        bluestacks_config=bluestacks_config,
    )
    df = df.loc[df.status == "device"].reset_index(drop=True).copy()
    df["aa_adbtools"] = df.localhost.apply(
        lambda x: ADBTools(adb_path=adb_path, deviceserial=f"localhost:{x}")
    )
    df.aa_adbtools.apply(lambda x: x.aa_connect_to_device())
    return df


def show_screenshots(title, sleeptime, killkeys="ctrl+alt+h"):
    while True:
        sleep(sleeptime)
        if len(_screenshots[killkeys]) > 0:
            cv2_imshow_multi(
                title=title,
                image=_screenshots[killkeys][0],
                killkeys=killkeys,  # switch on/off
            )


class ADBTools:
    def __init__(self, adb_path, deviceserial, sdcard="/sdcard/"):
        self.adb_path = adb_path
        self.deviceserial = deviceserial
        self.sdcard = sdcard
        self.tesseractpath = None
        self.bb_adbkeyboard = None
        self.bb_sendevent_keyboard = None
        self.bb_getevent_sendevent = None
        self.bb_sendevent_touch = None
        self.bb_adbdevicechanger = None
        self.screenshot = None
        self.screenshot_gray = None
        self.tesseract = None
        self.df = None
        self.bb_input_text = None
        self.scrcpy_screenshot_usb = None
        self.scrcpy_screenshot_tcp = None
        self._show_screenshot_thread = None
        self._add_new_screenshot_thread = None
        self._screenshotkillkeys = None

    def __str__(self):
        return self.deviceserial

    def __repr__(self):
        return self.deviceserial

    def _start_show_screenshot(self, title, killkeys="ctrl+alt+h", sleeptime=1):
        self._add_new_screenshot_thread = kthread.KThread(
            target=self._add_new_screenshots,
            name=str(killkeys),
            args=(sleeptime, killkeys),
        )
        self._add_new_screenshot_thread.start()
        self._show_screenshot_thread = kthread.KThread(
            target=show_screenshots,
            name=str(killkeys),
            args=(title, sleeptime, killkeys),
        )
        self._show_screenshot_thread.start()

    def _add_new_screenshots(self, sleeptime, killkeys):
        self._screenshotkillkeys = killkeys
        while True:
            _screenshots[killkeys].append(self.screenshot.copy())
            sleep(sleeptime)

    def aa_kill_show_screenshot(self):
        print(
            f"Press {self._screenshotkillkeys} to close the screenshot window if you haven't closed it yet"
        )
        try:
            if self._add_new_screenshot_thread:
                while self._add_new_screenshot_thread.is_alive():
                    self._add_new_screenshot_thread.kill()
        except Exception:
            pass
        try:
            if self._show_screenshot_thread:
                while self._show_screenshot_thread.is_alive():
                    self._show_screenshot_thread.kill()
        except Exception:
            pass
        try:
            del _screenshots[self._screenshotkillkeys]
        except Exception:
            pass

    def aa_kill_scrcpy_connection(self):
        if self.scrcpy_screenshot_usb:
            try:
                self.scrcpy_screenshot_usb.quit()
            except Exception:
                pass
        if self.scrcpy_screenshot_tcp:
            try:
                self.scrcpy_screenshot_tcp.quit()
            except Exception:
                pass

    def aa_show_screenshot(self, sleeptime=1, killkeys="ctrl+alt+h"):
        if is_nan(self.screenshot):
            self.aa_update_screenshot()
        if killkeys in _screenshots:
            raise ValueError(f"Killkeys {killkeys} are already being used!")
        else:
            print(f"Use {killkeys} to turn imshow on/off")
            self._start_show_screenshot(str(self.deviceserial), killkeys, sleeptime)

    def aa_activate_scrcpy_screenshots_usb(
        self, adb_host_address="127.0.0.1", adb_host_port=5037, lock_video_orientation=0
    ):
        screenwidth, screenheight = get_screen_height_width(
            self.adb_path, self.deviceserial
        )
        self.scrcpy_screenshot_usb = AdbShotUSB(
            device_serial=self.deviceserial,
            adb_path=self.adb_path,
            adb_host_address=adb_host_address,
            adb_host_port=adb_host_port,
            sleep_after_exception=0.05,
            frame_buffer=4,
            lock_video_orientation=lock_video_orientation,
            max_frame_rate=0,
            byte_package_size=131072,
            scrcpy_server_version="2.0",
            log_level="info",
            max_video_width=screenheight,
            start_server=False,
            connect_to_device=False,
        )

    def aa_activate_scrcpy_screenshots_tcp(
        self, adb_host_address="127.0.0.1", adb_host_port=5037, lock_video_orientation=0
    ):
        screenwidth, screenheight = get_screen_height_width(
            self.adb_path, self.deviceserial
        )

        self.scrcpy_screenshot_tcp = AdbShotTCP(
            device_serial=self.deviceserial,
            adb_path=self.adb_path,
            ip=adb_host_address,
            port=adb_host_port,
            sleep_after_exception=0.05,
            frame_buffer=4,
            lock_video_orientation=lock_video_orientation,
            max_frame_rate=0,
            byte_package_size=131072,
            scrcpy_server_version="2.0",
            log_level="info",
            max_video_width=screenheight,
            start_server=False,
            connect_to_device=False,
        )

    @staticmethod
    def connect_to_all_bluestacks_hyperv_devices(
        adb_path,
        timeout=10,
        bluestacks_config=r"C:\ProgramData\BlueStacks_nxt\bluestacks.conf",
    ):
        return connect_to_all_bluestacks_hyperv_devices(
            adb_path, timeout=timeout, bluestacks_config=bluestacks_config
        )

    def aa_activate_adbdevicechanger(
        self,
    ):
        self.bb_adbdevicechanger = AdbChanger(
            adb_path=self.adb_path,
            deviceserial=self.deviceserial,
        )

        return self

    def aa_uninstall_apk(
        self,
        apk,
        exit_keys="ctrl+x",
        print_output=True,
        timeout=None,
    ):
        return uninstall_apk(
            self.adb_path,
            self.deviceserial,
            apk,
            exit_keys=exit_keys,
            print_output=print_output,
            timeout=timeout,
        )

    def aa_install_apk_from_hdd(self, path):
        savepathapk = os.path.normpath(path)
        subprocess.run(f"{self.adb_path} -s {self.deviceserial} install {savepathapk}")

    def aa_copy_apk_to_hdd(
        self,
        packageregex,
        folder,
        exit_keys="ctrl+x",
        print_output=False,
        timeout=None,
    ):
        allpackages = self.aa_list_all_packages(exit_keys, print_output, timeout)
        copy_apk_to_hd(
            self.adb_path,
            self.deviceserial,
            packageregex,
            allpackages,
            folder,
            exit_keys=exit_keys,
            print_output=print_output,
            timeout=timeout,
        )

    def aa_copy_all_apks_to_hdd(
        self,
        folder,
        exit_keys="ctrl+x",
        print_output=False,
        timeout=None,
    ):
        allpackages = self.aa_list_all_packages(exit_keys, print_output, timeout)

        copy_apks_to_hd(
            self.adb_path,
            self.deviceserial,
            allpackages,
            folder,
            exit_keys=exit_keys,
            print_output=print_output,
            timeout=timeout,
        )

    def aa_input_text_formated(
        self, text, respect_german_letters=False, exit_keys="ctrl+x"
    ):
        self.bb_input_text.escape_text_and_send(
            text, respect_german_letters=respect_german_letters, exit_keys=exit_keys
        )
        return self

    def aa_input_text_formated_with_delay(
        self, text, delay=(0.01, 0.2), respect_german_letters=False, exit_keys="ctrl+x"
    ):
        self.bb_input_text.escape_text_and_send_with_delay(
            text,
            delay=delay,
            respect_german_letters=respect_german_letters,
            exit_keys=exit_keys,
        )
        return self

    def aa_activate_input_text_formated(self, debug=True):
        self.bb_input_text = ADBInputEscaped(
            adb_path=self.adb_path, deviceserial=self.deviceserial
        )
        # adbk.connect_to_device()
        if debug:
            self.bb_input_text.activate_debug()
        return self

    def aa_update_imagedf(self):
        self.df = pd.Q_image2df(self.screenshot)

    def aa_input_tap(self, x, y):
        x, y = int(x), int(y)
        self.aa_execute_multiple_adb_shell_commands([f"input tap {x} {y}"])
        return self

    def aa_multi_input_tap_with_delay(self, coords_and_timeout):
        allco = []
        for co, ti in coords_and_timeout:
            coadd = f"input tap {int(co[0])} {int(co[1])}"
            tisl = f"sleep {round(ti, 3)}"
            allco.append(coadd)
            allco.append(tisl)
        self.aa_execute_multiple_adb_shell_commands(allco)
        return self

    def aa_update_screenshot(self, color_and_gray=True):
        if self.scrcpy_screenshot_tcp:
            self.screenshot = self.scrcpy_screenshot_tcp.get_one_screenshot()
        elif self.scrcpy_screenshot_usb:
            self.screenshot = self.scrcpy_screenshot_usb.get_one_screenshot()
        else:
            self.screenshot = next(
                self.aa_get_screenshots(
                    sleeptime=0,
                    number=1,
                    gray=False,
                )
            )
        if color_and_gray:
            self.screenshot_gray = open_image_in_cv(
                self.screenshot, channels_in_output=2
            )
        return self

    def aa_activate_sendevent_touch(
        self,
        sdcard="/storage/emulated/0/",
        tmp_folder_on_sd_card="AUTOMAT",
        bluestacks_divider=32767,
        use_bluestacks_coordinates=True,
    ):
        self.bb_sendevent_touch = SendEventTouch(
            adb_path=self.adb_path,
            deviceserial=self.deviceserial,
            sdcard=sdcard,
            # it is probably better to pass the path, not the symlink
            tmp_folder_on_sd_card=tmp_folder_on_sd_card,  # if the folder doesn't exist, it will be created
            bluestacks_divider=bluestacks_divider,
            use_bluestacks_coordinates=use_bluestacks_coordinates,
            # Recalculates the BlueStacks coordinates https://stackoverflow.com/a/73733261/15096247
        )

        self.bb_sendevent_touch.connect_to_adb()
        return self

    def aa_activate_getevent_sendevent(
        self,
        sdcard="/storage/emulated/0/",
        tmp_folder_on_sd_card="AUTOMAT",
        bluestacks_divider=32767,
        exit_keys="ctrl+x",
    ):
        self.bb_getevent_sendevent = GetEventSendEvent(
            adb_path=self.adb_path,
            deviceserial=self.deviceserial,
            sdcard=sdcard,
            temfolder_on_sd_card=tmp_folder_on_sd_card,  # if the folder doesn't exist, it will be created
            bluestacks_divider=bluestacks_divider,
            exit_keys=exit_keys,  # stop the recording session
        )

        self.bb_getevent_sendevent.connect_to_adb()
        return self

    def aa_activate_sendevent_keyboard(
        self,
        sdcard="/storage/emulated/0/",
        tmp_folder_on_sd_card="AUTOMAT",
        exit_keys="ctrl+x",
    ):
        self.bb_sendevent_keyboard = SendEventKeystrokes(
            adb_path=self.adb_path,
            deviceserial=self.deviceserial,
            sdcard=sdcard,
            tmp_folder_on_sd_card=tmp_folder_on_sd_card,
            # The folder will be created if it doesn't exist. All temp files will be stored there
            exit_keys=exit_keys,  # If you want to interrupt adb
        )

        self.bb_sendevent_keyboard.connect_to_adb()
        return self

    def aa_activate_adb_keyboard(self, exit_keys="ctrl+x"):
        self.bb_adbkeyboard = AdbUnicodeKeyboard(
            adb_path=self.adb_path, deviceserial=self.deviceserial, exit_keys=exit_keys
        )

        self.bb_adbkeyboard.connect_to_adb()
        return self

    def aa_capture_logcat(
        self,
        exit_keys="ctrl+x",
        timeout=None,
    ):
        return adb_logcat_to_df(
            self.adb_path, self.deviceserial, exit_keys=exit_keys, timeout=timeout
        )

    def aa_get_all_displayed_items_from_act_and_ui(
        self,
        screenshotfolder: Union[str, None] = None,
        max_variation_percent_x: int = 10,
        max_variation_percent_y: int = 10,
        loung_touch_delay: tuple[int, int] = (1000, 1500),
        swipe_variation_startx: int = 10,
        swipe_variation_endx: int = 10,
        swipe_variation_starty: int = 10,
        swipe_variation_endy: int = 10,
        sdcard: str = "/storage/emulated/0/",
        tmp_folder_on_sd_card: str = "AUTOMAT",
        bluestacks_divider: int = 32767,
        with_screenshot=True,
    ):
        andf = AndroDF(
            adb_path=self.adb_path,
            deviceserial=self.deviceserial,
            screenshotfolder=screenshotfolder,  # screenshots will be saved here
            max_variation_percent_x=max_variation_percent_x,
            max_variation_percent_y=max_variation_percent_y,  # used for one of the click functions, to not click exactly in the center
            loung_touch_delay=loung_touch_delay,
            swipe_variation_startx=swipe_variation_startx,  # swipe coordinate variations in percent
            swipe_variation_endx=swipe_variation_endx,
            swipe_variation_starty=swipe_variation_starty,
            swipe_variation_endy=swipe_variation_endy,
            sdcard=sdcard,
            tmp_folder_on_sd_card=tmp_folder_on_sd_card,
            bluestacks_divider=bluestacks_divider,
        )
        andf.get_df_from_view(with_screenshot=with_screenshot)
        df_activities, df_uiautomator, df_merged = andf.get_all_results()
        return df_activities, df_uiautomator, df_merged

    def aa_get_all_displayed_items_from_uiautomator(
        self,
        screenshotfolder: Union[str, None] = None,
        max_variation_percent_x: int = 10,
        max_variation_percent_y: int = 10,
        loung_touch_delay: tuple[int, int] = (1000, 1500),
        swipe_variation_startx: int = 10,
        swipe_variation_endx: int = 10,
        swipe_variation_starty: int = 10,
        swipe_variation_endy: int = 10,
        sdcard: str = "/storage/emulated/0/",
        tmp_folder_on_sd_card: str = "AUTOMAT",
        bluestacks_divider: int = 32767,
        with_screenshot=True,
    ):
        andf = AndroDF(
            adb_path=self.adb_path,
            deviceserial=self.deviceserial,
            screenshotfolder=screenshotfolder,  # screenshots will be saved here
            max_variation_percent_x=max_variation_percent_x,
            max_variation_percent_y=max_variation_percent_y,  # used for one of the click functions, to not click exactly in the center
            loung_touch_delay=loung_touch_delay,
            swipe_variation_startx=swipe_variation_startx,  # swipe coordinate variations in percent
            swipe_variation_endx=swipe_variation_endx,
            swipe_variation_starty=swipe_variation_starty,
            swipe_variation_endy=swipe_variation_endy,
            sdcard=sdcard,
            tmp_folder_on_sd_card=tmp_folder_on_sd_card,
            bluestacks_divider=bluestacks_divider,
        )
        andf.screenshot = self.screenshot
        andf.get_df_from_view(with_screenshot=with_screenshot)
        _, df_uiautomator, _ = andf.get_all_results()
        return df_uiautomator

    def aa_get_all_displayed_items_from_uiautomator_parents_children(
        self, df=None, *args, **kwargs
    ):
        try:
            fetchdf = df.empty
        except Exception:
            fetchdf = True

        if fetchdf:
            df = self.aa_get_all_displayed_items_from_uiautomator(*args, **kwargs)

        return self._find_children_parents(df, prefix="bb")

    def aa_get_all_displayed_items_from_activities(
        self,
        screenshotfolder: Union[str, None] = None,
        max_variation_percent_x: int = 10,
        max_variation_percent_y: int = 10,
        loung_touch_delay: tuple[int, int] = (1000, 1500),
        swipe_variation_startx: int = 10,
        swipe_variation_endx: int = 10,
        swipe_variation_starty: int = 10,
        swipe_variation_endy: int = 10,
        sdcard: str = "/storage/emulated/0/",
        tmp_folder_on_sd_card: str = "AUTOMAT",
        bluestacks_divider: int = 32767,
        with_screenshot=True,
    ):
        andf = AndroDF(
            adb_path=self.adb_path,
            deviceserial=self.deviceserial,
            screenshotfolder=screenshotfolder,  # screenshots will be saved here
            max_variation_percent_x=max_variation_percent_x,
            max_variation_percent_y=max_variation_percent_y,  # used for one of the click functions, to not click exactly in the center
            loung_touch_delay=loung_touch_delay,
            swipe_variation_startx=swipe_variation_startx,  # swipe coordinate variations in percent
            swipe_variation_endx=swipe_variation_endx,
            swipe_variation_starty=swipe_variation_starty,
            swipe_variation_endy=swipe_variation_endy,
            sdcard=sdcard,
            tmp_folder_on_sd_card=tmp_folder_on_sd_card,
            bluestacks_divider=bluestacks_divider,
        )
        andf.screenshot = self.screenshot
        andf.get_df_from_activity(with_screenshot=with_screenshot)
        df_activities, _, _ = andf.get_all_results()
        return df_activities

    def aa_get_all_displayed_items_from_activities_parents_children(
        self, df=None, *args, **kwargs
    ):
        try:
            fetchdf = df.empty
        except Exception:
            fetchdf = True

        if fetchdf:
            df = self.aa_get_all_displayed_items_from_activities(*args, **kwargs)

        return self._find_children_parents(df, prefix="aa")

    def _find_children_parents(self, df, prefix):
        dfnotna = df.loc[
            (~df[f"{prefix}_shapely"].isna())
            & (df[f"{prefix}_area"] > 0)
            & (df[f"{prefix}_area"] < (df[f"{prefix}_area"].max()))
        ]
        splitdf = [dfnotna.iloc[i : i + 1].copy() for i in range(len(dfnotna))]
        df3 = dfnotna.ds_apply_ignore(
            pd.NA,
            lambda x: g
            if not (
                g := pd.concat(
                    [
                        item.assign(**{f"{prefix}_index_parent": x.name})
                        for item in splitdf
                        if x[f"{prefix}_shapely"].contains(
                            item[f"{prefix}_shapely"].iloc[0]
                        )
                        and x.name != item.index[0]
                        and (item[f"{prefix}_area"].iloc[0] < x[f"{prefix}_area"])
                    ]
                )
            ).empty
            else pd.NA,
            axis=1,
        )
        dfparentchild = (
            pd.concat(df3.dropna().to_list())
            .assign(**{f"{prefix}_index_child": lambda x: x.index.__array__().copy()})
            .reset_index(drop=True)
        )
        return dfparentchild

    def aa_list_folder_content(self, folder_to_search):
        return get_folder_df(self.deviceserial, self.adb_path, folder=folder_to_search)

    def aa_list_all_files_on_device(self):
        return get_folder_df(self.deviceserial, self.adb_path, folder="")

    def aa_list_all_packages(
        self,
        exit_keys="ctrl+x",
        print_output=True,
        timeout=None,
    ):
        return list_all_packages(
            self.adb_path,
            self.deviceserial,
            exit_keys=exit_keys,
            print_output=print_output,
            timeout=timeout,
        )

    def aa_grep_search(
        self,
        regular_expression: str,
        folder_to_search: str,
        filetype: str,
        exit_keys: str = "ctrl+x",
        timeout: Union[float, int, None] = None,
        remove_control_characters: bool = True,
    ):
        has_root_access = use_root.enabled

        return adb_grep(
            self.adb_path,
            self.deviceserial,
            has_root_access=has_root_access,
            folder_to_search=folder_to_search,
            remove_control_characters=remove_control_characters,
            filetype=filetype,
            timeout=timeout,
            regular_expression=regular_expression,
            exit_keys=exit_keys,
        )

    def aa_parse_settings_from_all_packages(self, tempfolder, datafolder="data/"):
        return parse_config_files(
            self.adb_path,
            self.deviceserial,
            save_in_folder=tempfolder,
            folder=datafolder,
            with_sed_columns=False,
        )

    def aa_get_activity_execution_df_from_one_package(self, packagename):
        return a_pandas_ex_adb_execute_activities.get_activities_df_from_package(
            self.adb_path, self.deviceserial, packagename=packagename
        )

    def aa_get_activity_execution_df_from_all_packages(self):
        return a_pandas_ex_adb_execute_activities.get_all_activities(
            self.adb_path,
            self.deviceserial,
        )

    def aa_copy_to_clipboard(self, text):
        pyperclip.copy(text)
        return self

    def aa_paste_clipboard(
        self,
        package,
        exit_keys="ctrl+x",
        print_output=True,
        timeout=None,
    ):
        return allow_read_clipboard(
            self.adb_path,
            self.deviceserial,
            package,
            exit_keys=exit_keys,
            print_output=print_output,
            timeout=timeout,
        )

    def aa_allow_read_clipboard(
        self,
        package,
        exit_keys="ctrl+x",
        print_output=True,
        timeout=None,
    ):
        return allow_read_clipboard(
            self.adb_path,
            self.deviceserial,
            package,
            exit_keys=exit_keys,
            print_output=print_output,
            timeout=timeout,
        )

    def aa_ignore_read_clipboard(
        self,
        package,
        exit_keys="ctrl+x",
        print_output=True,
        timeout=None,
    ):
        return ignore_read_clipboard(
            self.adb_path,
            self.deviceserial,
            package,
            exit_keys=exit_keys,
            print_output=print_output,
            timeout=timeout,
        )

    def aa_add_new_contact(
        self,
        name,
        phone,
        email,
        address,
        save=True,
        exit_keys="ctrl+x",
        print_output=True,
        timeout=None,
    ):
        return add_new_contact(
            self.adb_path,
            self.deviceserial,
            name,
            phone,
            email,
            address,
            save=save,
            exit_keys=exit_keys,
            print_output=print_output,
            timeout=timeout,
        )

    def aa_set_active(
        self,
        package,
        exit_keys="ctrl+x",
        print_output=True,
        timeout=None,
    ):
        return set_active(
            self.adb_path,
            self.deviceserial,
            package,
            exit_keys=exit_keys,
            print_output=print_output,
            timeout=timeout,
        )

    def aa_set_inactive(
        self,
        package,
        exit_keys="ctrl+x",
        print_output=True,
        timeout=None,
    ):
        return set_inactive(
            self.adb_path,
            self.deviceserial,
            package,
            exit_keys=exit_keys,
            print_output=print_output,
            timeout=timeout,
        )

    def aa_enable_roblox_textures(
        self,
        exit_keys="ctrl+x",
        print_output=True,
        timeout=None,
    ):
        return enable_roblox_textures(
            self.adb_path,
            self.deviceserial,
            exit_keys=exit_keys,
            print_output=print_output,
            timeout=timeout,
        )

    def aa_disable_roblox_textures(
        self,
        exit_keys="ctrl+x",
        print_output=True,
        timeout=None,
    ):
        return disable_roblox_textures(
            self.adb_path,
            self.deviceserial,
            exit_keys=exit_keys,
            print_output=print_output,
            timeout=timeout,
        )

    def aa_go_to_home_screen(
        self,
        exit_keys="ctrl+x",
        print_output=True,
        timeout=None,
    ):
        return go_to_main_screen(
            self.adb_path,
            self.deviceserial,
            exit_keys=exit_keys,
            print_output=print_output,
            timeout=timeout,
        )

    def aa_press_delete_key_repeated_times(
        self,
        repeat=5,
        exit_keys="ctrl+x",
        print_output=True,
        timeout=None,
    ):
        return press_delete_key_repeated_times(
            self.adb_path,
            self.deviceserial,
            repeat=repeat,
            exit_keys=exit_keys,
            print_output=print_output,
            timeout=timeout,
        )

    def aa_get_content(
        self,
        type_="text/plain",
        exit_keys="ctrl+x",
        print_output=True,
        timeout=None,
    ):
        return get_content(
            self.adb_path,
            self.deviceserial,
            type_=type_,
            exit_keys=exit_keys,
            print_output=print_output,
            timeout=timeout,
        )

    def aa_whole_dumpsys_to_df(
        self, exit_keys="ctrl+x", print_output=True, timeout=None
    ):
        return all_dumpsys_to_df(
            self.adb_path,
            self.deviceserial,
            exit_keys=exit_keys,
            print_output=print_output,
            timeout=timeout,
        )

    def aa_enable_root(
        self,
    ):
        use_root.enabled = True
        return self

    def aa_disable_root(self):
        use_root.enabled = False
        return self

    def aa_list_pending_intents(
        self,
        exit_keys="ctrl+x",
        print_output=True,
        timeout=None,
    ):
        return get_pending_intent(
            self.adb_path,
            self.deviceserial,
            exit_keys=exit_keys,
            print_output=print_output,
            timeout=timeout,
        )

    def aa_list_broadcast_stats(
        self,
        exit_keys="ctrl+x",
        print_output=True,
        timeout=None,
    ):
        return get_broadcast_stats(
            self.adb_path,
            self.deviceserial,
            exit_keys=exit_keys,
            print_output=print_output,
            timeout=timeout,
        )

    def aa_list_all_activities_from_device(
        self,
        exit_keys="ctrl+x",
        print_output=True,
        timeout=None,
    ):
        return get_all_activities_from_device(
            self.adb_path,
            self.deviceserial,
            exit_keys=exit_keys,
            print_output=print_output,
            timeout=timeout,
        )

    def aa_list_all_services(
        self,
        exit_keys="ctrl+x",
        print_output=True,
        timeout=None,
    ):
        return get_all_services_from_all_packages(
            self.adb_path,
            self.deviceserial,
            exit_keys=exit_keys,
            print_output=print_output,
            timeout=timeout,
        )

    def aa_list_all_receivers(
        self,
        exit_keys="ctrl+x",
        print_output=True,
        timeout=None,
    ):
        return get_all_receivers_from_all_packages(
            self.adb_path,
            self.deviceserial,
            exit_keys=exit_keys,
            print_output=print_output,
            timeout=timeout,
        )

    def aa_list_all_activities(
        self,
        exit_keys="ctrl+x",
        print_output=True,
        timeout=None,
    ):
        return get_all_activities_from_all_packages(
            self.adb_path,
            self.deviceserial,
            exit_keys=exit_keys,
            print_output=print_output,
            timeout=timeout,
        )

    def aa_open_camera_photo_mode(
        self,
        exit_keys="ctrl+x",
        print_output=True,
        timeout=None,
    ):
        return open_camera_photo_mode(
            self.adb_path,
            self.deviceserial,
            exit_keys=exit_keys,
            print_output=print_output,
            timeout=timeout,
        )

    def aa_get_procstats(
        self,
        exit_keys="ctrl+x",
        print_output=True,
        timeout=None,
    ):
        return get_procstats(
            self.adb_path,
            self.deviceserial,
            exit_keys=exit_keys,
            print_output=print_output,
            timeout=timeout,
        )

    def aa_list_all_devices(
        self,
        exit_keys="ctrl+x",
        print_output=True,
        timeout=None,
    ):
        return list_all_devices(
            self.adb_path,
            self.deviceserial,
            exit_keys=exit_keys,
            print_output=print_output,
            timeout=timeout,
        )

    def aa_create_nested_folder_path(self, path):
        return make_folders(
            adb_path=self.adb_path, deviceserial=self.deviceserial, path2create=path
        )

    def aa_push_file_to_path(self, file, dest):
        return push_file(
            adb_path=self.adb_path,
            deviceserial=self.deviceserial,
            file=file,
            dest=dest,
        )

    def aa_list_pids_basic(
        self,
        exit_keys="ctrl+x",
        print_output=True,
        timeout=None,
    ):
        return list_pids(
            self.adb_path,
            self.deviceserial,
            complete=False,
            exit_keys=exit_keys,
            print_output=print_output,
            timeout=timeout,
        )

    def aa_list_pids_complete(
        self,
        exit_keys="ctrl+x",
        print_output=True,
        timeout=None,
    ):
        return list_pids(
            self.adb_path,
            self.deviceserial,
            complete=True,
            exit_keys=exit_keys,
            print_output=print_output,
            timeout=timeout,
        )

    def aa_list_memory(
        self,
        exit_keys="ctrl+x",
        print_output=True,
        timeout=None,
    ):
        return list_memory(
            self.adb_path,
            self.deviceserial,
            exit_keys=exit_keys,
            print_output=print_output,
            timeout=timeout,
        )

    def aa_getprop(self, exit_keys="ctrl+x", print_output=True, timeout=None):
        return getprop(
            self.adb_path,
            self.deviceserial,
            exit_keys=exit_keys,
            print_output=print_output,
            timeout=timeout,
        )

    def aa_open_website(self, url, exit_keys="ctrl+x", print_output=True, timeout=None):
        return open_website(
            self.adb_path,
            self.deviceserial,
            url=url,
            exit_keys=exit_keys,
            print_output=print_output,
            timeout=timeout,
        )

    def aa_start_gallery(self, exit_keys="ctrl+x", print_output=True, timeout=None):
        return start_gallery(
            self.adb_path,
            self.deviceserial,
            exit_keys=exit_keys,
            print_output=print_output,
            timeout=timeout,
        )

    def aa_list_all_broadcasts(
        self, exit_keys="ctrl+x", print_output=True, timeout=None
    ):
        return get_all_broadcasts(
            self.adb_path,
            self.deviceserial,
            exit_keys=exit_keys,
            print_output=print_output,
            timeout=timeout,
        )

    def aa_list_all_broadcasts_history(
        self, exit_keys="ctrl+x", print_output=True, timeout=None
    ):
        return get_all_broadcasts_history(
            self.adb_path,
            self.deviceserial,
            exit_keys=exit_keys,
            print_output=print_output,
            timeout=timeout,
        )

    def aa_take_a_picture(
        self, sleeptime=4, exit_keys="ctrl+x", print_output=True, timeout=None
    ):
        return take_a_picture(
            self.adb_path,
            self.deviceserial,
            sleeptime=sleeptime,
            exit_keys=exit_keys,
            print_output=print_output,
            timeout=timeout,
        )

    def aa_disconnect(self, exit_keys="ctrl+x", timeout=None):
        return disconnect(
            self.adb_path,
            self.deviceserial,
            exit_keys=exit_keys,
            timeout=timeout,
        )

    def aa_remove_file(self, file, exit_keys="ctrl+x", timeout=None):
        return remove_file(
            self.adb_path,
            self.deviceserial,
            file,
            exit_keys=exit_keys,
            timeout=timeout,
        )

    def aa_adb_turn_screen_compatibility_on(
        self, exit_keys="ctrl+x", print_output=True, timeout=None
    ):
        return adb_turn_screen_compatibility_on(
            self.adb_path,
            self.deviceserial,
            exit_keys=exit_keys,
            print_output=print_output,
            timeout=timeout,
        )

    def aa_disable_notifications(self, exit_keys="ctrl+x", timeout=None):
        return disable_notifications(
            self.adb_path,
            self.deviceserial,
            exit_keys=exit_keys,
            timeout=timeout,
        )

    def aa_enable_notifications(self, exit_keys="ctrl+x", timeout=None):
        return enable_notifications(
            self.adb_path,
            self.deviceserial,
            exit_keys=exit_keys,
            timeout=timeout,
        )

    def aa_adb_turn_screen_compatibility_off(
        self, exit_keys="ctrl+x", print_output=True, timeout=None
    ):
        return adb_turn_screen_compatibility_off(
            self.adb_path,
            self.deviceserial,
            exit_keys=exit_keys,
            print_output=print_output,
            timeout=timeout,
        )

    def aa_change_screen_orientation(
        self,
        new_orientation="horizontal",
        exit_keys="ctrl+x",
        print_output=True,
        timeout=None,
    ):
        return change_screen_orientation(
            self.adb_path,
            self.deviceserial,
            exit_keys=exit_keys,
            print_output=print_output,
            timeout=timeout,
            new_orientation=new_orientation,
        )

    def aa_list_users(self, exit_keys="ctrl+x", print_output=True, timeout=None):
        return show_users(
            self.adb_path,
            self.deviceserial,
            exit_keys=exit_keys,
            print_output=print_output,
            timeout=timeout,
        )

    def aa_get_display_orientation(
        self, exit_keys="ctrl+x", print_output=True, timeout=None
    ):
        return get_display_orientation(
            self.adb_path,
            self.deviceserial,
            exit_keys=exit_keys,
            print_output=print_output,
            timeout=timeout,
        )

    def aa_rescan_media(self, exit_keys="ctrl+x", print_output=True, timeout=None):
        return rescann_media(
            self.adb_path,
            self.deviceserial,
            exit_keys=exit_keys,
            print_output=print_output,
            timeout=timeout,
        )

    def aa_move_to_end_of_line(
        self, exit_keys="ctrl+x", print_output=True, timeout=None
    ):
        return adb_move_to_end_of_line(
            self.adb_path,
            self.deviceserial,
            exit_keys=exit_keys,
            print_output=print_output,
            timeout=timeout,
        )

    def aa_hide_keyboard(self):
        return hide_keyboard(
            self.adb_path,
            self.deviceserial,
        )

    def aa_is_keyboard_shown(self):
        return is_keyboard_shown(
            self.adb_path,
            self.deviceserial,
        )

    def aa_list_devices(
        self,
        exit_keys="ctrl+x",
        print_output=True,
        timeout=None,
    ):
        return get_all_devices(
            self.adb_path,
            exit_keys=exit_keys,
            print_output=print_output,
            timeout=timeout,
        )

    def aa_is_screen_unlocked(self):
        return is_screen_unlocked(
            self.adb_path,
            self.deviceserial,
        )

    def aa_lock_screen(
        self,
        exit_keys="ctrl+x",
        print_output=True,
        timeout=None,
    ):
        return lock_screen(
            self.adb_path,
            self.deviceserial,
            exit_keys=exit_keys,
            print_output=print_output,
            timeout=timeout,
        )

    def aa_press_home(
        self,
        exit_keys="ctrl+x",
        print_output=True,
        timeout=None,
    ):
        return adb_press_home(
            self.adb_path,
            self.deviceserial,
            exit_keys=exit_keys,
            print_output=print_output,
            timeout=timeout,
        )

    def aa_press_app_switch(
        self,
        exit_keys="ctrl+x",
        print_output=True,
        timeout=None,
    ):
        return adb_press_app_switch(
            self.adb_path,
            self.deviceserial,
            exit_keys=exit_keys,
            print_output=print_output,
            timeout=timeout,
        )

    def aa_swipe_up_to_unlock_screen(
        self,
        password,
        exit_keys="ctrl+x",
        print_output=True,
        timeout=None,
    ):
        return swipe_up_to_unlock_screen(
            self.adb_path,
            self.deviceserial,
            password,
            exit_keys=exit_keys,
            print_output=print_output,
            timeout=timeout,
        )

    def aa_close_all_apps_with_swipe(
        self,
        loops=20,
        swipecoords=(522, 1647, 522, 90),
        exit_keys="ctrl+x",
        print_output=True,
        timeout=None,
    ):
        close_all_apps(
            self.adb_path,
            self.deviceserial,
            loops=loops,
            swipecoords=swipecoords,
            exit_keys=exit_keys,
            print_output=print_output,
            timeout=timeout,
        )

    def aa_list_permission_groups(
        self,
        exit_keys="ctrl+x",
        print_output=True,
        timeout=None,
    ):
        return list_permission_groups(
            self.adb_path,
            self.deviceserial,
            exit_keys=exit_keys,
            print_output=print_output,
            timeout=timeout,
        )

    def aa_uninstall_package(
        self,
        package,
        exit_keys="ctrl+x",
        print_output=True,
        timeout=None,
    ):
        uninstall_package(
            self.adb_path,
            self.deviceserial,
            package,
            exit_keys=exit_keys,
            print_output=print_output,
            timeout=timeout,
        )

    def aa_list_disabled_packages(
        self, exit_keys="ctrl+x", print_output=True, timeout=None
    ):
        return list_disabled_packages(
            self.adb_path,
            self.deviceserial,
            exit_keys=exit_keys,
            print_output=print_output,
            timeout=timeout,
        )

    def aa_list_3rd_party_packages(
        self, exit_keys="ctrl+x", print_output=True, timeout=None
    ):
        return list_third_party_packages(
            self.adb_path,
            self.deviceserial,
            exit_keys=exit_keys,
            print_output=print_output,
            timeout=timeout,
        )

    def aa_list_apps_in_use(self, exit_keys="ctrl+x", print_output=True, timeout=None):
        return applications_in_use(
            self.adb_path,
            self.deviceserial,
            exit_keys=exit_keys,
            print_output=print_output,
            timeout=timeout,
        )

    def aa_disable_autoupdate_for_package(
        self,
        package,
        user=0,
        exit_keys="ctrl+x",
        print_output=True,
        timeout=None,
    ):
        return disable_autoupdate_for_package(
            self.adb_path,
            self.deviceserial,
            package,
            user=user,
            exit_keys=exit_keys,
            print_output=print_output,
            timeout=timeout,
        )

    def aa_enable_autoupdate_for_package(
        self,
        package,
        user=0,
        exit_keys="ctrl+x",
        print_output=True,
        timeout=None,
    ):
        return enable_autoupdate_for_package(
            self.adb_path,
            self.deviceserial,
            package,
            user=user,
            exit_keys=exit_keys,
            print_output=print_output,
            timeout=timeout,
        )

    def aa_enable_autoupdate_for_user(
        self,
        exit_keys="ctrl+x",
        print_output=True,
        timeout=None,
    ):
        return enable_autoupdate_for_user(
            self.adb_path,
            self.deviceserial,
            exit_keys=exit_keys,
            print_output=print_output,
            timeout=timeout,
        )

    def aa_disable_autoupdate_for_user(
        self,
        exit_keys="ctrl+x",
        print_output=True,
        timeout=None,
    ):
        return disable_autoupdate_for_user(
            self.adb_path,
            self.deviceserial,
            exit_keys=exit_keys,
            print_output=print_output,
            timeout=timeout,
        )

    def aa_resolve_activity(
        self,
        package,
        exit_keys="ctrl+x",
        print_output=True,
        timeout=None,
    ):
        return resolve_activity(
            self.adb_path,
            self.deviceserial,
            package=package,
            exit_keys=exit_keys,
            print_output=print_output,
            timeout=timeout,
        )

    def aa_list_features(
        self,
        exit_keys="ctrl+x",
        print_output=True,
        timeout=None,
    ):
        return list_features(
            self.adb_path,
            self.deviceserial,
            exit_keys=exit_keys,
            print_output=print_output,
            timeout=timeout,
        )

    def aa_expand_settings(
        self,
        exit_keys="ctrl+x",
        print_output=True,
        timeout=None,
    ):
        return expand_settings(
            self.adb_path,
            self.deviceserial,
            exit_keys=exit_keys,
            print_output=print_output,
            timeout=timeout,
        )

    def aa_expand_notifications(
        self,
        exit_keys="ctrl+x",
        print_output=True,
        timeout=None,
    ):
        return expand_notifications(
            self.adb_path,
            self.deviceserial,
            exit_keys=exit_keys,
            print_output=print_output,
            timeout=timeout,
        )

    def aa_open_app(
        self,
        package_name,
        exit_keys="ctrl+x",
        print_output=True,
        timeout=None,
    ):
        return start_package(
            self.adb_path,
            self.deviceserial,
            package_name,
            exit_keys=exit_keys,
            print_output=print_output,
            timeout=timeout,
        )

    def aa_swipe(
        self,
        x0,
        y0,
        x1,
        y1,
        delay,
        exit_keys="ctrl+x",
        print_output=True,
        timeout=None,
    ):
        return adb_swipe(
            self.adb_path,
            self.deviceserial,
            x0,
            y0,
            x1,
            y1,
            int(delay * 1000),
            exit_keys=exit_keys,
            print_output=print_output,
            timeout=timeout,
        )

    def aa_open_shell(self):
        adb_open_shell(
            self.adb_path,
            self.deviceserial,
        )

    def aa_change_cwd_and_execute_adb_shell(
        self,
        commands,
        folder="/sdcard/",
        exit_keys="ctrl+x",
        print_output=True,
    ):
        return adb_shell_change_to_folder_and_execute(
            self.adb_path,
            self.deviceserial,
            commands,
            folder=folder,
            exit_keys=exit_keys,
            print_output=print_output,
        )

    def aa_push_to_sdcard(self, path):
        return copy_to_sd_card(
            self.adb_path, self.deviceserial, path, sdcard=self.sdcard
        )

    def aa_pull(self, path_android, path_pc, maintain_structure=True):
        if not maintain_structure:
            destfile = os.path.normpath(
                os.path.join(path_pc, regex.split(r"[\\/]+", path_android)[-1])
            )
        else:
            destfile = os.path.normpath(
                os.path.join(
                    os.path.normpath(path_pc),
                    os.path.normpath(path_android).lstrip("/\\"),
                )
            )

        try:
            if not os.path.exists(destfile):
                touch(destfile)
                os.remove(destfile)
        except Exception:
            pass
        print(destfile)
        return pull(
            self.adb_path, self.deviceserial, destfile, path_device=path_android
        )

    def aa_isfolder(self, path, exit_keys="ctrl+x", print_output=False, timeout=None):
        return isfolder(
            self.adb_path,
            self.deviceserial,
            path,
            exit_keys=exit_keys,
            print_output=print_output,
            timeout=timeout,
        )

    def aa_get_screenshots(
        self,
        sleeptime=1,
        number=1,
        gray=False,
        ADAPTIVE_THRESH_MEAN_C=False,
        ADAPTIVE_THRESH_GAUSSIAN_C=False,
        THRESH_OTSU=False,
    ):
        return _get_n_adb_screenshots(
            self.adb_path,
            self.deviceserial,
            sleeptime=sleeptime,
            n=number,
            gray=gray,
            ADAPTIVE_THRESH_MEAN_C=ADAPTIVE_THRESH_MEAN_C,
            ADAPTIVE_THRESH_GAUSSIAN_C=ADAPTIVE_THRESH_GAUSSIAN_C,
            THRESH_OTSU=THRESH_OTSU,
        )

    def aa_path_exists(self, path):
        return adb_path_exists(self.adb_path, self.deviceserial, path)

    def aa_get_screen_resolution(self):
        try:
            return get_screen_height_width(self.adb_path, self.deviceserial)
        except Exception:
            screenshot=_get_n_adb_screenshots(
                self.adb_path,
                self.deviceserial,
                sleeptime=None,
                n=1,
                gray=False,
                ADAPTIVE_THRESH_MEAN_C=False,
                ADAPTIVE_THRESH_GAUSSIAN_C=False,
                THRESH_OTSU=False,
            )
            return screenshot.shape[:2][::-1]

    def aa_connect_to_device(self):
        connect_to_adb(self.adb_path, self.deviceserial)

    def aa_restart_server(self, killadb=True):
        self.aa_kill_server()
        sleep(2)
        if killadb:
            kill_all_running_adbs()

            PROCNAME = "adb.exe"
            for proc in psutil.process_iter():
                try:
                    if proc.name().lower() == PROCNAME:
                        proc.kill()
                except Exception:
                    continue
            sleep(2)
        self.aa_start_server()
        self.aa_connect_to_device()

    def aa_reboot_and_listen_to_usb(
        self,
        exit_keys="ctrl+x",
        print_output=True,
        timeout=None,
    ):
        reboot_and_listen_to_usb(
            self.adb_path,
            exit_keys=exit_keys,
            print_output=print_output,
            timeout=timeout,
        )

    def aa_start_server(
        self,
        *args,
        **kwargs
        # exit_keys="ctrl+x",
        # print_output=True,
        # timeout=None,
    ):
        start_server(
            self.adb_path,
        )

    @staticmethod
    def aa_kill_all_running_adb_instances():
        return kill_all_running_adbs()

    def aa_stop_server(
        self,
        exit_keys="ctrl+x",
        print_output=True,
        timeout=None,
    ):
        stop_server(
            self.adb_path,
            exit_keys=exit_keys,
            print_output=print_output,
            timeout=timeout,
        )

    def aa_kill_server(
        self,
        exit_keys="ctrl+x",
        print_output=True,
        timeout=None,
    ):
        kill_server(
            self.adb_path,
            exit_keys=exit_keys,
            print_output=print_output,
            timeout=timeout,
        )

    def aa_connect_do_all_devices(self, start=4999, end=6000, timeout=10):
        return connect_to_all_localhost_accounts_in_range(
            self.adb_path, start=start, end=end, timeout=timeout
        )

    def aa_execute_non_shell_adb_command(
        self,
        command,
        exit_keys="ctrl+x",
        print_output=True,
        timeout=None,
    ):
        return execute_adb_without_shell(
            self.adb_path,
            command,
            device_serial=self.deviceserial,
            exit_keys=exit_keys,
            print_output=print_output,
            timeout=timeout,
        )

    def aa_execute_multiple_adb_shell_commands(
        self,
        commands,
        exit_keys="ctrl+x",
        print_output=True,
        timeout=None,
    ):
        return execute_multicommands_adb_shell(
            self.adb_path,
            self.deviceserial,
            commands,
            exit_keys=exit_keys,
            print_output=print_output,
            timeout=timeout,
        )

    def aa_ocr_elements_from_activities(
        self,
        allstrings,
        minpercentage=85,
        maxtolerance=10,
        screenshotfolder: Union[str, None] = None,
        max_variation_percent_x: int = 10,
        max_variation_percent_y: int = 10,
        loung_touch_delay: tuple[int, int] = (1000, 1500),
        swipe_variation_startx: int = 10,
        swipe_variation_endx: int = 10,
        swipe_variation_starty: int = 10,
        swipe_variation_endy: int = 10,
        sdcard: str = "/storage/emulated/0/",
        tmp_folder_on_sd_card: str = "AUTOMAT",
        bluestacks_divider: int = 32767,
    ):
        if not isinstance(allstrings, (list, tuple)):
            allstrings = [allstrings]
        with_screenshot = True

        andf = AndroDF(
            adb_path=self.adb_path,
            deviceserial=self.deviceserial,
            screenshotfolder=screenshotfolder,  # screenshots will be saved here
            max_variation_percent_x=max_variation_percent_x,
            max_variation_percent_y=max_variation_percent_y,  # used for one of the click functions, to not click exactly in the center
            loung_touch_delay=loung_touch_delay,
            swipe_variation_startx=swipe_variation_startx,  # swipe coordinate variations in percent
            swipe_variation_endx=swipe_variation_endx,
            swipe_variation_starty=swipe_variation_starty,
            swipe_variation_endy=swipe_variation_endy,
            sdcard=sdcard,
            tmp_folder_on_sd_card=tmp_folder_on_sd_card,
            bluestacks_divider=bluestacks_divider,
        )
        andf.screenshot = self.screenshot
        andf.get_df_from_activity(with_screenshot=with_screenshot)
        df_activities, _, _ = andf.get_all_results()
        return self._ocr_with_tesseract_and_fuzzy_search(
            df_activities,
            "aa_",
            allstrings,
            minpercentage=minpercentage,
            maxtolerance=maxtolerance,
        )

    def aa_ocr_elements_from_uiautomator(
        self,
        allstrings,
        minpercentage=85,
        maxtolerance=10,
        screenshotfolder: Union[str, None] = None,
        max_variation_percent_x: int = 10,
        max_variation_percent_y: int = 10,
        loung_touch_delay: tuple[int, int] = (1000, 1500),
        swipe_variation_startx: int = 10,
        swipe_variation_endx: int = 10,
        swipe_variation_starty: int = 10,
        swipe_variation_endy: int = 10,
        sdcard: str = "/storage/emulated/0/",
        tmp_folder_on_sd_card: str = "AUTOMAT",
        bluestacks_divider: int = 32767,
    ):
        if not isinstance(allstrings, (list, tuple)):
            allstrings = [allstrings]
        with_screenshot = True

        andf = AndroDF(
            adb_path=self.adb_path,
            deviceserial=self.deviceserial,
            screenshotfolder=screenshotfolder,  # screenshots will be saved here
            max_variation_percent_x=max_variation_percent_x,
            max_variation_percent_y=max_variation_percent_y,  # used for one of the click functions, to not click exactly in the center
            loung_touch_delay=loung_touch_delay,
            swipe_variation_startx=swipe_variation_startx,  # swipe coordinate variations in percent
            swipe_variation_endx=swipe_variation_endx,
            swipe_variation_starty=swipe_variation_starty,
            swipe_variation_endy=swipe_variation_endy,
            sdcard=sdcard,
            tmp_folder_on_sd_card=tmp_folder_on_sd_card,
            bluestacks_divider=bluestacks_divider,
        )
        andf.screenshot = self.screenshot
        andf.get_df_from_view(with_screenshot=with_screenshot)
        _, df_uiautomator, _ = andf.get_all_results()
        # df=self.aa_get_all_displayed_items_from_uiautomator()
        return self._ocr_with_tesseract_and_fuzzy_search(
            df_uiautomator,
            "bb_",
            allstrings,
            minpercentage=minpercentage,
            maxtolerance=maxtolerance,
        )

    def _ocr_with_tesseract_and_fuzzy_search(
        self, df, prefix, allstrings, minpercentage=85, maxtolerance=10
    ):
        prefix = "bb_"
        checkpref = [x for x in df.columns if str(x).startswith(prefix)]
        if not checkpref:
            prefix = "aa_"
        # df=update_screenshot_and_get_activities_df(self,screenshotfolder=screenshotfolder)
        drodf = df.dropna(subset=f"{prefix}screenshot").copy()
        tesserscan = drodf.copy()
        tesserscan2 = drodf.copy()
        for key, item in tesserscan.iterrows():
            varx = " ".join(
                self.aa_ocr_with_tesseract(item[f"{prefix}screenshot"])[
                    0
                ].text.to_list()
            )
            tesserscan2.at[key, f"{prefix}scanned_text"] = regex.sub(
                r"\s+", " ", varx.strip()
            )  # print(tesserscan2)

        for ini, searchstring in enumerate(allstrings):
            tesserscan2[searchstring] = tesserscan2[
                f"{prefix}scanned_text"
            ].ds_apply_ignore(pd.NA, lambda x: rapidfuzz.fuzz.ratio(searchstring, x))

        tes3 = tesserscan2.copy()
        alltes = []
        for stri in allstrings:
            tesserscan2 = tes3.drop(columns=[x for x in allstrings if x != stri]).copy()
            # print(tesserscan2)
            tesserscan2 = tesserscan2.rename(columns={stri: f"{prefix}tesseract"})
            tesserscan2[f"{prefix}closest_word"] = stri
            tesserscan2 = tesserscan2.sort_values(
                by=f"{prefix}tesseract", ascending=-False
            )
            tesserscan2[f"{prefix}resultdiff"] = (
                tesserscan2[f"{prefix}tesseract"]
                - tesserscan2[f"{prefix}tesseract"].iloc[0]
            )
            goodres = tesserscan2.loc[
                tesserscan2[f"{prefix}tesseract"].ds_apply_ignore(
                    pd.NA, lambda x: x - tesserscan2[f"{prefix}tesseract"].iloc[0]
                )
                > -maxtolerance
            ]
            alltes.append(goodres)

        dft = pd.concat(alltes).copy()
        dft = dft.loc[dft[f"{prefix}tesseract"] > minpercentage]
        return dft

    def aa_ocr_df_with_tesseract_multiprocessing(
        self,
        df,
        language="eng",
        cpus=5,
    ):
        df = df.reset_index(drop=True)
        prefix = "bb_"
        checkpref = [x for x in df.columns if str(x).startswith(prefix)]
        if not checkpref:
            prefix = "aa_"

        pics = df[f"{prefix}screenshot"].to_list()
        pics = [x if not is_nan(x) else np.array([], dtype=np.uint8) for x in pics]

        output = tesser2df(
            pics,
            language=language,
            pandas_kwargs={"on_bad_lines": "warn"},
            tesser_args=(),
            cpus=cpus,
            tesser_path=self.tesseractpath,
        )

        firstfilter = {
            x[0].img_index.iloc[0]: regex.sub(
                r"\s+", " ", " ".join(x[0].text.fillna("")).strip()
            )
            for x in output
            if not x[0].empty
        }
        for q in range(len(df)):
            if q not in firstfilter:
                firstfilter[q] = ""
        return pd.concat(
            [
                df,
                df.index.map(firstfilter)
                .to_series()
                .reset_index()
                .rename(columns={0: f"{prefix}scanned_text"})[f"{prefix}scanned_text"],
            ],
            axis=1,
        )

    def aa_ocr_with_tesseract(
        self,
        screenshot=None,
        search_for=None,
        gray=False,
        drop_empty_strings=True,
        conf_thresh=0.1,
    ):
        if isinstance(screenshot, type(None)):
            self.aa_update_screenshot()
            if not gray:
                dft = pd.Q_Tesseract_to_DF(self.screenshot)
            else:
                dft = pd.Q_Tesseract_to_DF(self.screenshot_gray)
        else:
            dft = pd.Q_Tesseract_to_DF(screenshot)

        dft["middle_x"] = dft.left + (dft.width // 2)
        dft["middle_y"] = dft.top + (dft.height // 2)
        dft = dft.dropna(subset=["conf", "text"])
        dft["conf"] = dft["conf"].astype("Float64")
        if drop_empty_strings:
            dft = dft.loc[dft["conf"] != -1]
            dft = dft.loc[dft.text.str.strip() != ""]
        if conf_thresh is not None:
            dft = dft.loc[dft["conf"] > conf_thresh]
        dft["end_x"] = dft.left + dft.width
        dft["end_y"] = dft.top + dft.height
        dft.reset_index(drop=True)
        tesser_results1 = dft.copy()
        searchresults = pd.DataFrame()
        searchresults_list = []
        tesser_results1 = tesser_results1[
            [
                x
                for x in tesser_results1.columns
                if not str(x).endswith("_num") and not str(x).startswith("level")
            ]
        ]
        if search_for is not None:
            text_to_search = search_for
            if not isinstance(text_to_search, (list, tuple)):
                text_to_search = [text_to_search]
            for text in text_to_search:
                textresult = (
                    tesser_results1.ds_fuzz_multirow(column="text", fuzzsearch=text)
                    .reset_index(drop=True)
                    .copy()
                )
                if not textresult.empty:
                    textresult["aa_query"] = text
                    searchresults_list.append(textresult.copy())
            searchresults = pd.concat(searchresults_list, ignore_index=True)
            searchresults = searchresults.sort_values(
                by=["aa_weighted", "aa_whole_text_len_difference"],
                ascending=[False, True],
            ).reset_index(drop=True)
        return tesser_results1, searchresults

    def aa_activate_tesseract(
        self, tesseractpath=r"C:\Program Files\Tesseract-OCR\tesseract.exe"
    ):
        self.tesseractpath = tesseractpath
        pd_add_tesseract(tesseractpath=tesseractpath)
        pd_add_regex_fuzz_multiline()
        return self

    def aa_root_bluestacks_instances(self, activate=True):
        # https://forum.xda-developers.com/t/guide-how-to-modify-app-preferences-with-adb-and-set-configuration-for-the-simple-calendar-widget.4447255/
        conffile = tuple(
            flatten_everything(
                [
                    glob.glob(os.path.normpath(os.path.join(x, "bluestacks.conf")))
                    for x in glob.glob(os.environ.get("PROGRAMDATA") + rf"{os.sep}*")
                    if regex.search("bluestacks", x, flags=regex.I)
                ]
            )
        )[0]
        try:
            updatedlines = []
            with open(conffile, mode="rb") as f:
                data = f.read()

            for line in data.splitlines():
                if b'enable_root_access="' in line:
                    if activate:
                        line = regex.sub(
                            b"enable_root_access.*", b'enable_root_access="1"', line
                        )
                    else:
                        line = regex.sub(
                            b"enable_root_access.*", b'enable_root_access="0"', line
                        )

                updatedlines.append(line)

            with open(conffile, mode="wb") as f:
                f.write(b"\n".join(updatedlines))

            return updatedlines
        except Exception as fe:
            print(fe)
            return None

    def _checkifscreenshot(self, screenshot):
        if isinstance(screenshot, type(None)):
            self.aa_update_screenshot()

            screenshot = self.screenshot.copy()
        return screenshot

    def get_shapes_from_screenshot_THRESH_OTSU(
        self, screenshot=None, draw_results=False
    ):
        screenshot = self._checkifscreenshot(screenshot)

        df, bw_pic = get_shapes_using_THRESH_OTSU(
            im=screenshot,
            method=cv2.CHAIN_APPROX_SIMPLE,
            approxPolyDPvar=0.01,
            kernel=(1, 1),
            start_thresh=50,
            end_thresh=255,
            return_bw_pic=True,
        )
        if draw_results:
            bw_pic = _draw_shapes_result(
                open_image_in_cv(bw_pic, channels_in_output=3), df, min_area=200
            )
        return df, bw_pic

    def get_shapes_from_screenshot_ADAPTIVE_THRESH_MEAN_C(
        self, screenshot=None, draw_results=False
    ):
        screenshot = self._checkifscreenshot(screenshot)

        df, bw_pic = get_shapes_using_ADAPTIVE_THRESH_MEAN_C(
            im=screenshot,
            method=cv2.CHAIN_APPROX_SIMPLE,
            approxPolyDPvar=0.01,
            constant_subtracted=2,
            block_size=11,
            return_bw_pic=True,
        )
        if draw_results:
            bw_pic = _draw_shapes_result(
                open_image_in_cv(bw_pic, channels_in_output=3), df, min_area=200
            )
        return df, bw_pic

    def get_shapes_from_screenshot_ADAPTIVE_THRESH_GAUSSIAN_C(
        self, screenshot=None, draw_results=False
    ):
        screenshot = self._checkifscreenshot(screenshot)

        df, bw_pic = get_shapes_using_ADAPTIVE_THRESH_GAUSSIAN_C(
            im=screenshot,
            method=cv2.CHAIN_APPROX_SIMPLE,
            approxPolyDPvar=0.01,
            constant_subtracted=2,
            block_size=11,
            return_bw_pic=True,
        )
        if draw_results:
            bw_pic = _draw_shapes_result(
                open_image_in_cv(bw_pic, channels_in_output=3), df, min_area=200
            )
        return df, bw_pic

    def aa_force_stop(
        self,
        package,
        exit_keys="ctrl+x",
        print_output=True,
        timeout=None,
    ):
        return self.aa_execute_multiple_adb_shell_commands(
            [f"am force-stop {package}"],
            exit_keys=exit_keys,
            print_output=print_output,
            timeout=timeout,
        )

    def aa_show_screenshot_in_browser(self):
        Image.fromarray(
            open_image_in_cv(
                self.screenshot.copy(), channels_in_output=3, bgr_to_rgb=True
            )
        ).show()
