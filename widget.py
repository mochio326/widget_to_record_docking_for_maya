## -*- coding: utf-8 -*-
from maya.app.general.mayaMixin import MayaQWidgetDockableMixin
from vendor.Qt import QtCore, QtGui, QtWidgets

import os
import json
import pymel.core as pm


class MyDockableWidget(MayaQWidgetDockableMixin, QtWidgets.QWidget):
    TITLE = "DockableButton"

    def __init__(self, parent=None):
        super(MyDockableWidget, self).__init__(parent=parent)
        # オブジェクト名とタイトルの変更
        self.setObjectName(self.TITLE)
        self.setWindowTitle(self.TITLE)
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose, True)
        self.setSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)


def get_ui():
    ui = {w.objectName(): w for w in QtWidgets.QApplication.allWidgets()}
    if MyDockableWidget.TITLE in ui:
        return ui[MyDockableWidget.TITLE]
    return None


def get_docking_filepath():
    _dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(_dir, 'docking.json')


def get_show_repr():
    dict_ = {}
    dict_['display'] = False
    dict_['dockable'] = True
    dict_['floating'] = True
    dict_['area'] = None
    dict_['x'] = 0
    dict_['y'] = 0
    dict_['width'] = 400
    dict_['height'] = 150

    _ui = get_ui()
    if _ui is None:
        return dict_
    if _ui.isVisible() is False:
        return dict_

    dict_['display'] = True
    dict_['dockable'] = _ui.isDockable()
    dict_['floating'] = _ui.isFloating()
    dict_['area'] = _ui.dockArea()
    if dict_['dockable'] is True:
        dock_dtrl = _ui.parent()
        _pos = dock_dtrl.mapToGlobal(QtCore.QPoint(0, 0))
    else:
        _pos = _ui.pos()
    _sz = _ui.geometry().size()
    dict_['x'] = _pos.x()
    dict_['y'] = _pos.y()
    dict_['width'] = _sz.width()
    dict_['height'] = _sz.height()
    return dict_


def quit_app():
    dict_ = get_show_repr()
    f = open(get_docking_filepath(), 'w')
    json.dump(dict_, f)
    f.close()


def make_quit_app_job():
    pm.scriptJob(e=("quitApplication", pm.Callback(quit_app)))


def restoration_docking_ui():
    '''
    ドッキングした状態のUIを復元する。
    
    前回終了時の状態が
    ・表示されている
    ・Mayaの何処かにドッキングされている
    ・フローティング状態ではない
    場合のみ動作する
    :return:
    '''
    path = get_docking_filepath()
    if os.path.isfile(path) is False:
        return
    f = open(path, 'r')
    _dict = json.load(f)
    if _dict['display'] is False:
        return
    if _dict['floating'] is False and _dict['area'] is not None:
        window = MyDockableWidget()
        window.show(
            dockable=True,
            area=_dict['area'],
            floating=_dict['floating'],
            width=_dict['width'],
            height=_dict['height']
        )
        

def main():
    # 同名のウインドウが存在したら削除
    ui = get_ui()
    if ui is not None:
        print ui
        ui.close()

    button = MyDockableWidget()
    button.show(dockable=True)
    
if __name__ == '__main__':
    main()

#-----------------------------------------------------------------------------
# EOF
#-----------------------------------------------------------------------------
