# Easier ADB automation 

## Tested against Windows 10, Python 3.9.13, BlueStacks 5.9.300.1014 N32

### pip install adbkit

**23/02/2023: New methods**
```python
from adbkit import ADBTools
adb_path = "C:\\Users\\Gamer\\AppData\\Local\\Android\\Sdk\\platform-tools\\adb.exe"
deviceserial = "localhost:5555"
self = ADBTools(adb_path=adb_path, deviceserial=deviceserial)
self.aa_connect_to_device()
self.aa_activate_tesseract(
    tesseractpath=r"C:\Program Files\Tesseract-OCR\tesseract.exe"
)

#####################################################################################
# This method uses Tesseract! You can download it here: https://digi.bib.uni-mannheim.de/tesseract/tesseract-ocr-w64-setup-5.3.0.20221222.exe
self.aa_update_screenshot() # Update the screenshot before 
df=self.aa_ocr_elements_from_activities(['Play Store'], # pass all strings as a list 
minpercentage=85, # fuzzy match
maxtolerance=10,
screenshotfolder="f:\\compare_android",  # screenshots will be saved here

	max_variation_percent_x=10,  # used for one of the click functions, to not click exactly in the center - more information below
	max_variation_percent_y=10,  # used for one of the click functions, to not click exactly in the center
	loung_touch_delay=(
		1000,
		1500,
	),  # with this settings longtouch will take somewhere between 1 and 1,5 seconds
	swipe_variation_startx=10,  # swipe coordinate variations in percent
	swipe_variation_endx=10,
	swipe_variation_starty=10,
	swipe_variation_endy=10,
	sdcard="/storage/emulated/0/",  # sdcard will be used if you use the sendevent methods, don't pass a symlink - more information below
	tmp_folder_on_sd_card="AUTOMAT",  # this folder will be created in the sdcard folder for using sendevent actions
	bluestacks_divider=32767,  # coordinates must be recalculated for BlueStacks https://stackoverflow.com/a/73733261/15096247 when using sendevent
)

    aa_area       aa_bounds  aa_center_x  aa_center_x_cropped  aa_center_y  aa_center_y_cropped   aa_class_name aa_clickable aa_complete_dump aa_context_clickable  aa_cropped_x_end  aa_cropped_x_start  aa_cropped_y_end  aa_cropped_y_start aa_depth aa_drawn aa_enabled aa_focusable  aa_has_screenshot aa_hashcode_hex aa_hashcode_int  aa_height  aa_height_cropped aa_id_information  aa_is_child aa_long_clickable aa_mID_hex aa_mID_int aa_old_index aa_pflag_activated aa_pflag_dirty_mask aa_pflag_focused aa_pflag_hovered aa_pflag_invalidated aa_pflag_is_root_namespace aa_pflag_prepressed aa_pflag_selected aa_pure_id   aa_screenshot aa_scrollbars_horizontal aa_scrollbars_vertical      aa_shapely  aa_valid_square aa_visibility  aa_width  aa_width_cropped  aa_x_end aa_x_end_relative  aa_x_start aa_x_start_relative  aa_y_end aa_y_end_relative  aa_y_start aa_y_start_relative ee_aa_longtouch ee_aa_longtouch_bs ee_aa_longtouch_offset ee_aa_longtouch_offset_bs ee_aa_touch ee_aa_touch_bs ee_aa_touch_offset ee_aa_touch_offset_bs ff_aa_downswipe ff_aa_save_screenshot ff_aa_show_screenshot ff_aa_tap_center_offset ff_aa_tap_center_offset_long ff_aa_tap_center_variation ff_aa_tap_center_variation_long ff_aa_tap_exact_center ff_aa_tap_exact_center_long ff_aa_upswipe ff_show_parents  parent_000  parent_001  parent_002  parent_003  parent_004  parent_005  parent_006  parent_007  parent_008  parent_009  parent_010  parent_011 aa_scanned_text  aa_tesseract aa_closest_word  aa_resultdiff
32  30192.0  (26, 26, 23...          128             128               100             100       com.bluesta...         True             ...            False                  230                26                 174                26            8     True       True        False            True            7529967       122853735        148             148               <NA>           True            True         <NA>       <NA>           14           False              False               False            False            False                False                      False               False         <NA>  [[[41, 12, ...           False                    False         POLYGON ((2...            True              V       204             204         230             204            26               0           174             148            26               0                  ()              ()                 ()                     ()                    ()             ()              ()                 ()                    ()              ()                    ()                    ()                      ()                           ()                         ()                              ()                     ()                        ()              ()           9           8           6           5           4           3           2           0        <NA>        <NA>        <NA>        <NA>      Play Store         100.0      Play Store            0.0



#####################################################################################
# Another example (Play Store written wrong)

df2=self.aa_ocr_elements_from_uiautomator(['blai Store'],minpercentage=70, maxtolerance=10, )

    aa_area       aa_bounds  aa_center_x  aa_center_x_cropped  aa_center_y  aa_center_y_cropped   aa_class_name aa_clickable aa_complete_dump aa_context_clickable  aa_cropped_x_end  aa_cropped_x_start  aa_cropped_y_end  aa_cropped_y_start aa_depth aa_drawn aa_enabled aa_focusable  aa_has_screenshot aa_hashcode_hex aa_hashcode_int  aa_height  aa_height_cropped aa_id_information  aa_is_child aa_long_clickable aa_mID_hex aa_mID_int aa_old_index aa_pflag_activated aa_pflag_dirty_mask aa_pflag_focused aa_pflag_hovered aa_pflag_invalidated aa_pflag_is_root_namespace aa_pflag_prepressed aa_pflag_selected aa_pure_id   aa_screenshot aa_scrollbars_horizontal aa_scrollbars_vertical      aa_shapely  aa_valid_square aa_visibility  aa_width  aa_width_cropped  aa_x_end aa_x_end_relative  aa_x_start aa_x_start_relative  aa_y_end aa_y_end_relative  aa_y_start aa_y_start_relative ee_aa_longtouch ee_aa_longtouch_bs ee_aa_longtouch_offset ee_aa_longtouch_offset_bs ee_aa_touch ee_aa_touch_bs ee_aa_touch_offset ee_aa_touch_offset_bs ff_aa_downswipe ff_aa_save_screenshot ff_aa_show_screenshot ff_aa_tap_center_offset ff_aa_tap_center_offset_long ff_aa_tap_center_variation ff_aa_tap_center_variation_long ff_aa_tap_exact_center ff_aa_tap_exact_center_long ff_aa_upswipe ff_show_parents  parent_000  parent_001  parent_002  parent_003  parent_004  parent_005  parent_006  parent_007  parent_008  parent_009  parent_010  parent_011 aa_scanned_text  aa_tesseract aa_closest_word  aa_resultdiff
32  30192.0  (26, 26, 23...          128             128               100             100       com.bluesta...         True             ...            False                  230                26                 174                26            8     True       True        False            True            7529967       122853735        148             148               <NA>           True            True         <NA>       <NA>           14           False              False               False            False            False                False                      False               False         <NA>  [[[41, 12, ...           False                    False         POLYGON ((2...            True              V       204             204         230             204            26               0           174             148            26               0                  ()              ()                 ()                     ()                    ()             ()              ()                 ()                    ()              ()                    ()                    ()                      ()                           ()                         ()                              ()                     ()                        ()              ()           9           8           6           5           4           3           2           0        <NA>        <NA>        <NA>        <NA>      Play Store         100.0      Play Store            0.0

#####################################################################################
# Pass a list of tuples:
((x,y),time in seconds)

self.aa_multi_input_tap_with_delay([((100,100),2), ((200,200),3)])
#####################################################################################

self.aa_input_tap(x=100,y=100)

#####################################################################################
# https://github.com/hansalemaos/adbescapes
# Converts Unicode string to ASCII and escapes all characters that need to be escaped. 
# You have to activate it, before using it. The first start takes some time because numba needs to compile the code 
self.aa_activate_input_text_formated()

# input 
text="""
"'ąćęłń'\tóśźż\nĄĆĘŁŃÓŚŹŻ\n\"Junto à Estação de \nCarcavelos;\"" "äöüÄÖÜß"
"""
self.aa_input_text_formated_with_delay(text,delay=(0.01, 0.2),respect_german_letters=False, exit_keys="ctrl+x")


# output
"'aceln'    oszz
ACELNOSZZ
"Junto a Estacao de 
Carcavelos;"" "aouAOUb"

# If you want it the German way :)
self.aa_input_text_formated(text,respect_german_letters=True, exit_keys="ctrl+x")

"'aceln'    oszz
ACELNOSZZ
"Junto a Estacao de 
Carcavelos;"" "aeoeueAeOeUess"
#####################################################################################
self.aa_install_apk_from_hdd(r"C:\Users\Gamer\anaconda3\envs\instcont\instagram.apk")
#####################################################################################
self.aa_uninstall_package('com.instagram.lite')
#####################################################################################
# First argument is a regex 
self.aa_copy_apk_to_hdd('com.insta.*', 'c:\\instaapkdownload')
#####################################################################################
```



**17/01/2023: Screenshot fix**


```python
$pip install adbkit
from adbkit import ADBTools
adb_path = "C:\\Users\\Gamer\\AppData\\Local\\Android\\Sdk\\platform-tools\\adb.exe"
deviceserial = "localhost:5875"

# Create an instance
# Don't get confused about the instance name "self". I did it because it is faster copying methods from the class 
self = ADBTools(adb_path, deviceserial, sdcard="/sdcard/")
self = ADBTools(adb_path=adb_path, deviceserial=deviceserial)

# connect to the device 
self.aa_connect_to_device()
```



```python
# If you are using BlueStacks and want to have root access, call:
self.aa_root_bluestacks_instances() 
# This method will basically do this steps: https://appuals.com/root-bluestacks/ to root BlueStacks
# You can run the script every time you use this module. It won't hurt. 
# The first time, you might have to restart BlueStacks to enable the root access 
```



```python
# If your device/BlueStacks is rooted, enable root so that all commands will be sent as root 
self.aa_enable_root() 
# can be disabled by calling :
self.aa_disable_root()
```



```python
# Activates self.bb_adbkeyboard 
# Read more about it: https://github.com/hansalemaos/adb_unicode_keyboard
self.aa_activate_adb_keyboard(exit_keys="ctrl+x") 
```



```python
# Activates self.bb_sendevent_keyboard (needs root access)
# Read more about it: https://github.com/hansalemaos/sendevent_getevent_keyboard

self.aa_activate_sendevent_keyboard(
    sdcard="/storage/emulated/0/",
    tmp_folder_on_sd_card="AUTOMAT",
    exit_keys="ctrl+x",
)  # needs root access

# Here is one example: 
self.bb_adbkeyboard.press_7_keycode_0()
```



```python
# Activates self.self.bb_getevent_sendevent
# Read more about it: https://github.com/hansalemaos/sendevent_getevent_keyboard

self.aa_activate_getevent_sendevent(
    sdcard="/storage/emulated/0/",
    tmp_folder_on_sd_card="AUTOMAT",
    bluestacks_divider=32767,
    exit_keys="ctrl+x",
)  # needs root access
```



```python
# Activates self.bb_sendevent_touch
# Read more about it: https://github.com/hansalemaos/sendevent_touch

self.aa_activate_sendevent_touch(
    sdcard="/storage/emulated/0/",
    tmp_folder_on_sd_card="AUTOMAT",
    bluestacks_divider=32767,
    use_bluestacks_coordinates=True,
)  # needs root access

# Here is one example:
self.bb_sendevent_touch.touch(10,10)
```



```python
# Activates https://github.com/hansalemaos/a_pandas_ex_tesseract_multirow_regex_fuzz
# You can download the 64 bit version of tesseract here: 
# https://digi.bib.uni-mannheim.de/tesseract/tesseract-ocr-w64-setup-5.3.0.20221222.exe

self.aa_activate_tesseract(
        tesseractpath=r"C:\Program Files\Tesseract-OCR\tesseract.exe"
    )

# Once activated, you can call:
# self.aa_ocr_with_tesseract()

    left  top  width  height       conf        text  middle_x  middle_y  end_x  end_y
8    382   42    499      49  37.512093         RH,       631        66    881     91
9    728   34     98      61  30.925949          2.       777        64    826     95
13   370  101     37      11   84.72541     'system       388       106    407    112
14   411  101     24      10  79.929901        Apps       423       106    435    111
15   536   90     36      28  85.425911      Roblox       554       104    572    118
16   676  100     55       9  88.744247  BlueStacks       703       104    731    109
17   735  101      7       8  80.470955           X       738       105    742    109
18   814  101     31      10  90.271423      Spiele       829       106    845    111
19   848  101     18       8  93.303749         und       857       105    866    109
20   869  103     41       9  87.963295     gewinne       889       107    910    112
28    72  100     20      12  96.004517        Play        82       106     92    112
29    95  101     27       8  86.986359       Store       108       105    122    109
33   225  211     49      12  76.804665   Globoplay       249       217    274    223
37   326  489     25      28  91.894142       Tibia       338       503    351    517
38   401  500     50       8  91.477989   Guardians       426       504    451    508
39   455  499     10       9  72.064316          of       460       503    465    508
41   415  512     37       9  75.078018     Cloudia       433       516    452    521

# and even perform a multiline fuzzy search:
xxx = self.aa_ocr_with_tesseract(search_for='Kontakte verwalten')
```
```python
# Use this method to update the screenshot 
# The updated screenshot can be found here: self.screenshot
self.aa_update_screenshot()

```



```python
# get 5 screenshot within 5 seconds
xx=self.aa_get_screenshots(
        sleeptime=1,
        number=5)

```



```python
# Now you can use self.df to do operations on the screenshot 
# More information about a_pandas_ex_image_tools:
# https://github.com/hansalemaos/a_pandas_ex_image_tools
self.aa_update_imagedf()
```


```python
# If you want to capture the logcat output and analyze it in a DataFrame,
use: 
logcatcap = self.aa_capture_logcat(
        exit_keys="ctrl+x",
        timeout=None,
    )  

# When you exit using "ctrl+x", the method will return a DataFrame
# By the way: almost all methods can be interrupted using a key command 
```



```python
# Those 2 methods will help you to identify and interact with views:
# Read more about it: https://github.com/hansalemaos/androdf
df1 = self.aa_get_all_displayed_items_from_uiautomator(
	screenshotfolder="f:\\compare_android",  # screenshots will be saved here
	max_variation_percent_x=10,  # used for one of the click functions, to not click exactly in the center - more information below
	max_variation_percent_y=10,  # used for one of the click functions, to not click exactly in the center
	loung_touch_delay=(
		1000,
		1500,
	),  # with this settings longtouch will take somewhere between 1 and 1,5 seconds
	swipe_variation_startx=10,  # swipe coordinate variations in percent
	swipe_variation_endx=10,
	swipe_variation_starty=10,
	swipe_variation_endy=10,
	sdcard="/storage/emulated/0/",  # sdcard will be used if you use the sendevent methods, don't pass a symlink - more information below
	tmp_folder_on_sd_card="AUTOMAT",  # this folder will be created in the sdcard folder for using sendevent actions
	bluestacks_divider=32767,  # coordinates must be recalculated for BlueStacks https://stackoverflow.com/a/73733261/15096247 when using sendevent
)

df3 = self.aa_get_all_displayed_items_from_activities(
	screenshotfolder="f:\\compare_android",  # screenshots will be saved here
	max_variation_percent_x=10,  # used for one of the click functions, to not click exactly in the center - more information below
	max_variation_percent_y=10,  # used for one of the click functions, to not click exactly in the center
	loung_touch_delay=(
		1000,
		1500,
	),  # with this settings longtouch will take somewhere between 1 and 1,5 seconds
	swipe_variation_startx=10,  # swipe coordinate variations in percent
	swipe_variation_endx=10,
	swipe_variation_starty=10,
	swipe_variation_endy=10,
	sdcard="/storage/emulated/0/",  # sdcard will be used if you use the sendevent methods, don't pass a symlink - more information below
	tmp_folder_on_sd_card="AUTOMAT",  # this folder will be created in the sdcard folder for using sendevent actions
	bluestacks_divider=32767,  # coordinates must be recalculated for BlueStacks https://stackoverflow.com/a/73733261/15096247 when using sendevent
)
```



```python
# Uses: https://github.com/hansalemaos/a_pandas_ex_adb_to_df
# lists all files in DataFrame and adds useful functions
# self.aa_list_all_files_on_device()

dffiles = self.aa_list_folder_content(folder_to_search="data/")  
print(dffiles)
                  aa_date  ... ff_pull_file_cat
0     2022-12-11 06:48:00  ...               ()
1     2022-12-26 22:16:00  ...               ()
2     2022-12-06 19:10:00  ...               ()
3     2022-12-06 13:38:00  ...               ()
4     2022-12-26 22:16:00  ...               ()
                   ...  ...              ...
26120 2021-09-16 04:21:00  ...               ()
26121 2021-09-16 03:53:00  ...               ()
26122 2021-09-16 03:53:00  ...               ()
26123 2021-09-16 04:35:00  ...               ()
26124 2021-09-16 04:31:00  ...               ()
[26125 rows x 16 columns]
```



```python
# Search with grep 
# Uses https://github.com/hansalemaos/adb_grep_search
dfgrep = self.aa_grep_search(
        folder_to_search="data/data",
        filetype="*.db",
        regular_expression=r"CREATE.TABLE",
        exit_keys="ctrl+x",
        timeout=None,
        remove_control_characters=True,
    )

dfgrep
Out[19]: 
                                               aa_file  ...      aa_regex
0    data/data/com.android.providers.media/database...  ...  CREATE.TABLE
1    data/data/com.android.providers.media/database...  ...  CREATE.TABLE
2    data/data/com.android.providers.media/database...  ...  CREATE.TABLE
3    data/data/com.android.providers.media/database...  ...  CREATE.TABLE
4    data/data/com.globo.globotv/databases/mcsdk_bf...  ...  CREATE.TABLE
..                                                 ...  ...           ...
103  data/data/com.roblox.client/databases/google_a...  ...  CREATE.TABLE
104  data/data/com.roblox.client/databases/google_a...  ...  CREATE.TABLE
105  data/data/com.roblox.client/databases/google_a...  ...  CREATE.TABLE
106  data/data/com.roblox.client/databases/google_a...  ...  CREATE.TABLE
107  data/data/com.roblox.client/databases/google_a...  ...  CREATE.TABLE
[108 rows x 5 columns]
```



```python
# Uses https://github.com/hansalemaos/a_pandas_ex_adb_settings_to_df
self.aa_parse_settings_from_all_packages(
        tempfolder="f:\\tmpfolder", datafolder="data/"
    )

        index          aa_all_keys  ... level_22 level_23
0         0.0         (long, name)  ...      NaN      NaN
1         1.0        (long, value)  ...      NaN      NaN
2         0.0   (boolean, 0, name)  ...      NaN      NaN
3         1.0  (boolean, 0, value)  ...      NaN      NaN
4         2.0   (boolean, 1, name)  ...      NaN      NaN
       ...                  ...  ...      ...      ...
110795    NaN            (6, desc)  ...      NaN      NaN
110796    NaN           (6, label)  ...      NaN      NaN
110797    NaN             (6, pkg)  ...      NaN      NaN
110798    NaN          (6, source)  ...      NaN      NaN
110799    NaN             (6, url)  ...      NaN      NaN
[110800 rows x 31 columns]

You might see this error messages several times:

"Go to: https://www.sqlite.org/download.html ,
download the dll and put it in the DLLs folder of your env!"

You can ignore it.
```



```python
#This method helps you find all executable activities from a package 
# More about it: https://github.com/hansalemaos/a_pandas_ex_adb_execute_activities

self.aa_get_activity_execution_df_from_one_package(
        packagename="com.roblox.client"
    ) 
```



```python
# adds new contact, can be saved straight away
addcon = self.aa_add_new_contact(
	"hans", "+55119897827552", "hans@something.com", "my address", save=False
)
```



```python
# If you play Roblox, you can enable/disable some textures to get higher fps
self.aa_enable_roblox_textures(
	exit_keys="ctrl+x",
	print_output=True,
	timeout=None,
)

self.aa_disable_roblox_textures(
	exit_keys="ctrl+x",
	print_output=True,
	timeout=None,
)
```



```python
# goes to the home screen, doesn't close anything
self.aa_go_to_home_screen()
```



```python
# repeat=5 usually deletes more than 5 characters!!
self.aa_press_delete_key_repeated_times(repeat=5)
```



```python
# starts the android file manager, pass the file type you want to see
self.aa_get_content(type_="text/plain")
```



```python
# Here are some methods to get useful information. 
# Returns DataFrames 
print(self.aa_whole_dumpsys_to_df())
print(self.aa_list_all_packages())
print(self.aa_list_broadcast_stats())
print(self.aa_list_pending_intents())
print(self.aa_list_all_activities_from_device())
print(self.aa_list_all_services())
print(self.aa_list_all_receivers())
print(self.aa_list_all_activities())
print(self.aa_get_procstats())
print(self.aa_list_all_devices()) # devices on the device (dev ...)
print(self.aa_list_devices()) # all adb devices (localhost:5555 ...)
print(self.aa_list_pids_basic())
print(self.aa_list_pids_complete())
print(self.aa_list_memory())
print(self.aa_getprop())
print(self.aa_list_all_broadcasts())
print(self.aa_list_all_broadcasts_history())
print(self.aa_list_users())
print(self.aa_list_permission_groups())
print(self.aa_list_disabled_packages())
print(self.aa_list_apps_in_use())
print(self.aa_list_3rd_party_packages())
print(self.aa_list_features())
```



```python
# Smile! :)
self.aa_open_camera_photo_mode()
```



```python
# works with and without http://
print(self.aa_open_website("google.com"))
```



```python
# switches to gallery
self.aa_start_gallery()
```



```python
# cheeeese
self.aa_take_a_picture()
```



```python
# useful for some apps 
self.aa_adb_turn_screen_compatibility_off()
self.aa_adb_turn_screen_compatibility_on()
```



```python
# Be careful! 
self.aa_remove_file('/sdcard/9.png')
```



```python
# Essential when you use your cell phone (with Whatsapp, Facebook ...) to automize things.
self.aa_enable_notifications()
self.aa_disable_notifications()
```



```python
# More useful stuff for notifications
self.aa_expand_settings() 
self.aa_expand_notifications()
```



```python
# Changes the screen orientation
# You can pass:
# horizontal_upside_down or 2
# vertical or 1
# horizontal or 0
# vertical_upside_down or 3
self.aa_change_screen_orientation("horizontal")
```



```python
self.aa_get_display_orientation()
#Out[4]: 0 
# 0 means horizontal
```



```python
# Sometimes you upload new media files, but you can't see the thumbnails immediately
# This method updates all thumbnails
self.aa_rescan_media()
```



```python
# If you are in the middle of a text and want to go to the end of the line
self.aa_move_to_end_of_line()
```



```python
# Useful keyboard stuff 
self.aa_hide_keyboard()
self.aa_is_keyboard_shown()
```



```python
# Doesn't work on BlueStacks, but on my pixel 6 there are no problems
# (Actually it is not necessary when using BlueStacks hahaha)
self.aa_is_screen_unlocked()
```



```python
# Don't use this command on BlueStacks, you will have to reboot the device
self.aa_lock_screen()
```



```python
# Useful commands 
self.aa_press_home() #back to home screen
self.aa_press_app_switch()
```



```python
# Configured for my Pixel 6, but should work on any device with a 
# newer android version. 
self.aa_swipe_up_to_unlock_screen('3333')
```



```python
# doesn't work with BlueStacks, because of the app switch design, 
# but it does on my pixel and should work with any device that 
# has a recent Android version
self.aa_close_all_apps_with_swipe()
```



```python
# uninstalls a package
self.aa_uninstall_package('com.google.android.youtube')
```



```python
# Returns the activity needed to open the package 
self.aa_resolve_activity('com.roblox.client')
b'priority=0 preferredOrder=0 match=0x108000 specificIndex=-1 isDefault=true\r\n'
b'com.roblox.client/.startup.ActivitySplash\r\n'
```



```python
# But you can also open any package using:
self.aa_open_app('com.roblox.client')
```



```python
# This method makes swiping easy
# x (start), y (start), x (end) y (end), last number in seconds
self.aa_swipe(500, 400, 500, 100, 1.1) 
```



```python
#opens a separate shell window using cmd.exe 
self.aa_open_shell() 
```



```python
# It changes the dictionary that you are in
# and executes a command 
self.aa_change_cwd_and_execute_adb_shell('ls', 'data/')
b'5.3.10.1001\r\n'
b'5.9.300.1014\r\n'
b'adb\r\n'
b'anr\r\n'
b'app\r\n'
b'app-asec\r\n'
b'app-ephemeral\r\n'
b'app-lib\r\n'
b'app-private\r\n'
b'arm\r\n'
....
```



```python
# This can also be accomplished by sending multiple commands: 
self.aa_execute_multiple_adb_shell_commands(['cd data/', 'ls|grep system'])
Out[28]: [b'system\r\n', b'system_ce\r\n', b'system_de\r\n']
```



```python
# You can also send non-shell commands: 
self.aa_execute_non_shell_adb_command('devices')
```



```python
# This method pushes a file to your sdcard:
self.aa_push_to_sdcard(r'F:\donedone.png')
```



```python
# This method pulls a file to your hdd
self.aa_pull('/sdcard/donedone.png', 'f:\\dfdffasd')
```



```python
# A fast way of scanning all connected devices:
# start/end means the ports you want to start/end with
# After 10 seconds, all processes that have not completed the search
# will be killed 
self.aa_connect_do_all_devices(start=4999, end=6000, timeout=10)
    '''self.aa_list_devices()
b'List of devices attached\r\n'
b'localhost:5037\toffline\r\n'
b'localhost:5040\toffline\r\n'
b'localhost:5357\toffline\r\n'
b'localhost:5725\tdevice\r\n'
b'localhost:5800\toffline\r\n'
b'localhost:5875\tdevice\r\n'
b'localhost:5900\toffline\r\n'
b'localhost:5955\tdevice\r\n'
b'\r\n'''

    '''
Killing the process
Killing the process
Killing the process
Killing the process
Killing the process
Killing the process
Killing the process
Killing the process
Killing the process'''
```



```python
# Uses https://github.com/hansalemaos/a_cv2_shape_finder 
# to detect shapes in the screenshot 
self.get_shapes_from_screenshot_THRESH_OTSU()
self.get_shapes_from_screenshot_ADAPTIVE_THRESH_MEAN_C()
self.get_shapes_from_screenshot_ADAPTIVE_THRESH_GAUSSIAN_C()
```



```python
#Some self-explaining stuff  

self.aa_isfolder('/sdcard/donedone.png')
False
self.aa_isfolder('/sdcard/')
True
next(self.aa_get_screenshots())

self.aa_path_exists('/sdcard/')
True
self.aa_path_exists('/sdcard2/')
False

self.aa_get_screen_resolution()
(960, 540)

self.aa_restart_server()
self.aa_reboot_and_listen_to_usb()
self.aa_start_server()
self.aa_stop_server()
self.aa_kill_server()
self.aa_force_stop('com.roblox.client') #root
self.aa_show_screenshot_in_browser()
```

