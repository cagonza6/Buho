pyuic4 src/Gui/Main_window.ui     -o src/Gui/Main_window.py
pyuic4 src/Gui/mNewItem.ui        -o src/Gui/mNewItem.py
pyuic4 src/Gui/mNewReader.ui      -o src/Gui/mNewReader.py
pyuic4 src/Gui/mLoanReturnBook.ui -o src/Gui/mLoanReturnBook.py
pyuic4 src/Gui/mSearch.ui         -o src/Gui/mSearch.py
pyuic4 src/Gui/MainPage.ui        -o src/Gui/mMainPage.py
pyuic4 src/Gui/mLoanInfo.ui       -o src/Gui/mLoanInfo.py
pyuic4 src/Gui/mReaderInfo.ui     -o src/Gui/mReaderInfo.py
pyuic4 src/Gui/mItemInfo.ui     -o src/Gui/mItemInfo.py
pyuic4 src/Gui/dialogs/mExportPDF.ui     -o src/Gui/dialogs/mExportPDF.py
pyuic4 src/Gui/dialogs/mSelectTargetFile.ui     -o src/Gui/dialogs/mSelectTargetFile.py
pyuic4 src/Gui/dialogs/mPrintCards.ui     -o src/Gui/dialogs/mPrintCards.py

pyuic4 src/Gui/mAbout.ui     -o src/Gui/mAbout.py
pyrcc4 src/Gui/myicons.qrc        -o src/Gui/myicons_rc.py
pyrcc4 src/Gui/myicons.qrc        -o src/Gui/dialogs/myicons_rc.py

#pylupdate4 src/make.pro
#lupdate-qt4 src/make.pro
