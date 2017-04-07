Mayaにドッキングできるウインドウの作成および終了時に状態を記録。  
次回起動時に復元するサンプルです。  

## 利用準備

サンプルをダウンロードし、フォルダをpython pathの通ったところに配置。  
_userSetup.pyの内容をuserSetup.pyに追記（もしくはuserSetup.pyにリネームして配置）  
  
userSetup.pyは C:\Users\ユーザー名\Documents\maya\バージョン\ja_JP\scripts など  

## UIの呼び出し

    import widget_to_record_docking_for_maya.widget as wrd
    wrd.main()

という感じで実行  

## ドッキングできるUI

Mayaの組み込みクラスである MayaQWidgetDockableMixin を継承することで容易にドッキングするウインドウを作成することが可能。  
詳細は公式ヘルプを参照。  
  
<https://knowledge.autodesk.com/ja/search-result/caas/CloudHelp/cloudhelp/2016/JPN/Maya-SDK/files/GUID-66ADA1FF-3E0F-469C-84C7-74CEB36D42EC-htm.html>


## 終了時の記録

userSetup.pyでMaya終了時に実行されるスクリプトジョブを登録  
モジュールと同階層にdocking.jsonというファイルが作成される。  
記録内容はドッキングの有無、ドッキング場所など。  
  
内容は MayaQWidgetDockableMixin クラス内の showRepr関数を改造した。  
ちなみに、外部ファイルではなくoptionVarなどに記録すればいいと思い試したものの、
optionVarはMaya終了時のイベントではタイミングの問題か情報が記録できなかったので現状の形に落ち着いた。  


## 起動時の復元

userSetup.pyで復元用の関数を呼び出し  
注意しないといけないのはuserSetup.pyはMayaのUIが構築される前に呼び出されるので、  

    import maya.utils
    maya.utils.executeDeferred()

としてUI構築後に関数が実行されるようにすること。  
サンプルでは前回終了時に  

* ウインドウが表示されている
* いずれかの場所にドッキングされている

という条件の場合のみ復元するようにしている。  
（フローティング状態でMayaを終了すると復元されない）  


## その他
動作はMaya2015で確認  
  
Maya2017からWorkspaceというレイアウトを覚えておく機能（概念）が出来たらしく、
ワークスペースを操作するworkspaceControlとworkspaceControlStateというMELコマンドをキチンと理解して
Panelと同様Mayaに正しいやり方で登録してあげることが出来れば、このサンプルの様な手段は必要ないはず。  
ただし、2017以前のバージョンには使えるかな、とは思う。
