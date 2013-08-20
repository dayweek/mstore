from distutils.core import setup

setup(name='mstore',
       version='0.0.1',
       scripts=['mstore'],
       data_files = [
                    ('share/pixmaps',             ['mstore_icon_26x26.png']),
                    ('share/applications/hildon', ['mstore.desktop']),
                    ('share/mstore/', ['store.py', 'ValidatedEntry.py', 'common.py', 'glade.py', 'main.py', 'store.py', 'adminstore.py', 'config.py', 'gtkcommon.py', 'validation_functions.py', 'cart.py', 'db.py', 'htmloutput.py', 'stats.py', 'document-print.png', 'edit-find-replace.png', 'filesave.png', 'go-up.png', 'list-remove.png', 'edit-clear.png', 'edit-paste.png', 'folder-new.png', 'gtk-cancel.png', 'edit-cut.png', 'file-new.png', 'go-home.png', 'list-add.png', 'mstore-data', 'ui_dlg.glade', 'ui.glade','styles.css']),
                    ]
      )
