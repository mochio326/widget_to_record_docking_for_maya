# Maya Save shelf state on exit
import widget_to_record_docking_for_maya.widget as wrd
wrd.make_quit_app_job()
# Restore docking state at startup
import maya.utils
maya.utils.executeDeferred(wrd.restoration_docking_ui)
