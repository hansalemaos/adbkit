# video -Brazilian Portugues- https://youtu.be/pWoDaTeobCw
from adbkit import ADBTools
from kthread_sleep import sleep
from mydevice import deviceserial

def get_uiautomator_frame(screenshotfolder='c:\\ttscreenshots'):
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


ADBTools.aa_kill_all_running_adb_instances()
adb_path = r'C:\ProgramData\chocolatey\bin\adb.exe'
adb = ADBTools(adb_path=adb_path, deviceserial=deviceserial)
adb.aa_start_server() # creates a new process which is not a child process
sleep(3)
adb.aa_connect_to_device()
adb.aa_activate_scrcpy_screenshots_usb(adb_host_address="127.0.0.1",
                        adb_host_port=5037, lock_video_orientation=0)

adb.aa_activate_adb_keyboard()

adb.aa_push_file_to_path(file=r"C:\xdf.m4v", dest='/sdcard/DCIM/0/')
adb.aa_execute_multiple_adb_shell_commands(
    'am start -a "com.ss.intent.action.redirect.record"')
sleep(2)
df = get_uiautomator_frame()
while df.loc[df.bb_pure_id == 'id/kap'].empty:
	df = get_uiautomator_frame()
df.loc[df.bb_pure_id == 'id/kap'].ff_bb_tap_exact_center.iloc[0]()


df = get_uiautomator_frame()
while df.loc[df.bb_pure_id == 'id/aqt'].empty:
	df = get_uiautomator_frame()

df.loc[df.bb_pure_id == 'id/aqt'].iloc[0].ff_bb_tap_exact_center()

df = get_uiautomator_frame()
while df.loc[(df.bb_text == 'Camera') & (df.bb_pure_id == 'id/dhc')].empty:
	df = get_uiautomator_frame()

df.loc[(df.bb_text == 'Camera') & (df.bb_pure_id == 'id/dhc')].ff_bb_tap_exact_center.iloc[0]()

df = get_uiautomator_frame()

while df.loc[df.bb_pure_id == 'id/bvb'].empty:
	df = get_uiautomator_frame()

timestamp=df.loc[df.bb_pure_id == 'id/bvb'
].sort_values(by='bb_keys_hierarchy')
timestamp.iloc[0].ff_bb_tap_exact_center()

df = get_uiautomator_frame()

while df.loc[df.bb_pure_id == 'id/fl3'].empty:
	df = get_uiautomator_frame()


df.loc[df.bb_pure_id == 'id/fl3'
].ff_bb_tap_center_offset.iloc[0](0,10)

adb.bb_adbkeyboard.activate_adb_keyboard()
while not adb.bb_adbkeyboard.is_keyboard_shown():
    df = get_uiautomator_frame()
    try:
        df.loc[(df.bb_class == 'android.widget.EditText')
               & (df.bb_pure_id == 'id/c0t'
                  )].iloc[0].ff_bb_tap_exact_center()
    except Exception:
        continue
adb.bb_adbkeyboard.send_unicode_text_with_delay('''Oi, 
galera, tudo bem? Aqui está meu novo vídeo''')
adb.bb_adbkeyboard.disable_adb_keyboard()

adb.aa_update_screenshot()
adb.aa_show_screenshot( sleeptime=1, killkeys="ctrl+alt+h")

