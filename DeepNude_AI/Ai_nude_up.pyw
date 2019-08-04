#-*- coding:utf-8 -*-

from  PyQt5.QtGui  import *
from  PyQt5.QtCore  import *
from  PyQt5.QtWidgets  import *
import sys
import cv2
from run import process
import argparse
import os
import random

#reload(sys)
#sys.setdefaultencoding("utf-8")


global image_name
image_name=""



#*******************************************************************
#*******************************************************************
#***************************布局类**********************************
#*******************************************************************
#*******************************************************************
class graphicsView(QGraphicsView):
    def __init__(self,parent=None):
        super(graphicsView,self).__init__(parent)

        self.image=""
        self.zoomscale=1
        

    def wheelEvent(self, event):
        
        global image_name   
        if image_name!="":
            self=image_name
            angle=event.angleDelta() / 8                                         
            angleX=angle.x()  
            angleY=angle.y()  
            #print(angleX,angleY)
            if angleY >= 0:
                self.zoomscale=self.zoomscale+0.1
                self.item.setScale(self.zoomscale)
                self.setAlignment(Qt.AlignCenter and Qt.AlignTop)
                    
           
            elif angleY <=  0:
                self.zoomscale=self.zoomscale-0.1
                self.item.setScale(self.zoomscale)
                self.setAlignment(Qt.AlignCenter and Qt.AlignTop)
        
                
                    
                
           


        
  
                
           
                
#*******************************************************************
#*******************************************************************
#***************************拖拽类**********************************
#*******************************************************************
#*******************************************************************

class MyLineEdit(QLineEdit):
        def __init__( self, parent=None ):
            super(MyLineEdit, self).__init__(parent)
            self.setDragEnabled(True)

        def dragEnterEvent( self, event ):
            
            data = event.mimeData()
            urls = data.urls()
            if ( urls and urls[0].scheme() == 'file' ):
                event.acceptProposedAction()
        def dragMoveEvent( self, event ):
            data = event.mimeData()
            urls = data.urls()
            if ( urls and urls[0].scheme() == 'file' ):
                event.acceptProposedAction()

        def dropEvent( self, event ):
            data = event.mimeData()
            urls = data.urls()
            if ( urls and urls[0].scheme() == 'file' ):
                filepath = str(urls[0].path())[1:]
                self.setText(filepath)

#*******************************************************************
#*******************************************************************
#***************************功能类**********************************
#*******************************************************************
#*******************************************************************
class Nude_transform_gui(QWidget):
    
    def __init__(self):
        super(Nude_transform_gui,self).__init__()
        #self.setWindowFlags(Qt.Window)
        self.setWindowTitle("Ai_Nude_Tool_a")
        
        self.initUI()
    def initUI(self):


        pic_address=QLabel(u'图片地址：')
        self.pic_address=MyLineEdit()
        pic_button=QPushButton(u"加载")

        save_address=QLabel(u'图片地址：')
        self.save_address=MyLineEdit()
        save_button=QPushButton(u"浏览")

        
        self._tree=graphicsView(self)
 
        
        start_work=QPushButton(u"转换图片")
 


        pbar=QLabel(u"进度")
        self.time_pos=QLineEdit()
        self.pbar = QProgressBar()

        #print dir(self.pbar)

        
        #groupNameData.setFrameStyle(QFrame.Panel|QFrame.Sunken)
        

        
        laty_1=QHBoxLayout()
        laty_1.addWidget(pic_address)
        laty_1.addWidget(self.pic_address)
        laty_1.addWidget(pic_button)
     

        laty_2=QHBoxLayout()
        laty_2.addWidget(self._tree)
        
        
      

        laty_3=QHBoxLayout()
        laty_3.addWidget(save_address)
        laty_3.addWidget(self.save_address)
        laty_3.addWidget(save_button)


        laty_4=QHBoxLayout()
        #print(dir(laty_4))
        laty_4.addStretch(10)
        laty_4.addSpacing(10)
        laty_4.addWidget(self.time_pos,1)
        laty_4.addWidget(pbar,1)
        laty_4.addWidget(self.pbar ,3)
        laty_4.addWidget(start_work,2)




        all_lay=QVBoxLayout()
        all_lay.addLayout(laty_1)
        all_lay.addLayout(laty_2)
        all_lay.addLayout(laty_3)
        all_lay.addLayout(laty_4)


      
        self.setLayout(all_lay)
        
        self.resize(600,700)


        pic_button.clicked.connect(self.get_pic_address)
        save_button.clicked.connect(self.get_save_address)
        start_work.clicked.connect(self.transform_nude)





    def get_pic_address(self):
            pic_address=self.pic_address.text()
            if(pic_address==""):
                QMessageBox.information(self,u"提示", u"请输入图片地址")
                return
            name=pic_address
            if os.path.exists(name):
                self._tree.image=QPixmap(name)
                
                    
                self._tree.graphicsView= QGraphicsScene()            
                self._tree.item = QGraphicsPixmapItem(self._tree.image)               
                self._tree.graphicsView.addItem(self._tree.item)
                self._tree.setAlignment(Qt.AlignCenter and Qt.AlignTop)
                if self._tree.image.width()!=500:
                    self._tree.item.setScale(500/self._tree.image.width()) 
                self._tree.setScene(self._tree.graphicsView)
                global image_name
                image_name=self._tree
                #print(image_name)
                
    def get_save_address(self):
        filename = QFileDialog.getExistingDirectory()
        if filename:
            filename=filename.replace("\\",'/')

    def createRandomString(self,len):
        print ('wet'.center(10,'*'))
        raw = ""
        range1 = range(58, 65) # between 0~9 and A~Z
        range2 = range(91, 97) # between A~Z and a~z

        i = 0
        while i < len:
            seed = random.randint(48, 122)
            if ((seed in range1) or (seed in range2)):
                continue;
            raw += chr(seed);
            i += 1
        return raw
    
    def _process(self,i_image, o_image, use_gpu):
        try:
            dress = cv2.imread(i_image)
            h = dress.shape[0]
            w = dress.shape[1]
            dress = cv2.resize(dress, (512,512), interpolation=cv2.INTER_CUBIC)
            watermark = process(dress, use_gpu)
            watermark =  cv2.resize(watermark, (w,h), interpolation=cv2.INTER_CUBIC)
            cv2.imwrite(o_image, watermark)
            print("[*] Image saved as: %s" % o_image)
            self.pbar.setValue(100)
            name=o_image
            if os.path.exists(name):
                self._tree.image=QPixmap(name)
                self._tree.graphicsView= QGraphicsScene()            
                self._tree.item = QGraphicsPixmapItem(self._tree.image)               
                self._tree.graphicsView.addItem(self._tree.item)
                self._tree.setAlignment(Qt.AlignCenter and Qt.AlignTop)
                if self._tree.image.width()!=500:
                    self._tree.item.setScale(500/self._tree.image.width()) 
                self._tree.setScene(self._tree.graphicsView)
                global image_name
                image_name=self._tree
        except Exception as e:
            print(e)
	
            

    def transform_nude(self):
        self.pbar.setValue(5)
        if str(self.pic_address.text())=="" or str(self.save_address.text())=="":
            QMessageBox.information(self,u"提示", u"请输入图片储存地址，视频名称可不写")
            return
        current_dir = os.path.abspath(os.path.dirname(__file__))
        os.chdir(current_dir)
        if(str(self.time_pos.text())==""):
            use_gpu=False
        else:
            use_gpu=True
        input_address=str(self.pic_address.text())
        if "." in str(self.save_address.text()):
            output_address=str(self.save_address.text())
        else:
            output_address=str(self.save_address.text())+"/"+os.path.splitext(os.path.basename(input_address))[0]+"_"+self.createRandomString(5)+".png"

 
        #print( output_address)
        
        self._process(input_address, output_address, use_gpu)
        #self.pbar.setValue(100)


#*******************************************************************
#*******************************************************************
#***************************主函数***********************************
#*******************************************************************
#******************************************************************* 

if __name__ == '__main__': 
    app = QApplication(sys.argv)
    bili = Nude_transform_gui()
    bili.show()
    sys.exit(app.exec_())
