import sys
import cv2
import os
import numpy as np
import source 
import imutils

from deteksi_nanas import *
from PyQt5 import QtWidgets,QtGui,QtCore
from PyQt5.QtWidgets import QApplication,QMessageBox,QFileDialog,QWidget
from PyQt5.QtGui import QIcon,QPixmap,QImage,QColor,QImageWriter
from PyQt5.QtCore import QTimer
from PyQt5.uic import loadUi

class MainWindow(QWidget):
	def __init__(self):
		super().__init__()
		self.ui=Ui_Dialog()
		self.ui.setupUi(self)
		self.timer=QTimer()
		self.timer.timeout.connect(self.viewCam)
		self.ui.Start_pushButton.clicked.connect(self.kontrolTimer)
		self.ui.Capture_pushButton_2.clicked.connect(self.capture)
		self.ui.Proses_pushButton_4.clicked.connect(self.proses)
		self.ui.Save_pushButton_3.clicked.connect(self.save)
		self.ui.Exit_pushButton_5.clicked.connect(self.exit)

	def viewCam(self):
		ret,img=self.cap.read()
		img=cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
		img=cv2.resize(img,(261,191),interpolation=cv2.INTER_AREA)
		height,width,channel=img.shape
		step=channel*width
		img1=QImage(img.data,width,height,step,QImage.Format_RGB888)
		self.ui.kamera.setPixmap(QPixmap.fromImage(img1))

	def kontrolTimer(self):
		if not self.timer.isActive():
			self.cap=cv2.VideoCapture(0)
			self.timer.start(20)
		else:
			self.timer.stop()
			self.cap.release()
			self.ui.Start_pushButton.setText("Start")

	def capture(self):
		ret,img=self.cap.read()
		rows,cols,_=img.shape
		up=(int(cols/6),int(rows/6))
		bottom=(int(cols*5/6),int(rows*5/6))
		img=img[up[1]:bottom[1],up[0]:bottom[0]]
		self.imgg=cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
		img=cv2.resize(self.imgg,(261,191),interpolation=cv2.INTER_AREA)
		height,width,channel=img.shape
		step=channel*width
		self.img1=QImage(img.data,width,height,step,QImage.Format_RGB888)
		self.ui.capture.setPixmap(QPixmap.fromImage(self.img1))

	def proses(self):

		#self.img2=cv2.resize(self.img2,(261,191),interpolation=cv2.INTER_AREA)
		#seluruh mata nanas
		self.img2 = self.imgg.copy()
		blur = cv2.GaussianBlur(self.img2,(17,17),0)
		rgb = cv2.cvtColor(blur,cv2.COLOR_BGR2RGB)
		mata_low = np.array([0,0,0],np.uint8)
		mata_high = np.array([165,150,90],np.uint8)
		mata = cv2.inRange(blur,mata_low,mata_high)
		kernel=np.ones((5,5),"uint8")
		dilasi=cv2.dilate(mata,kernel)
		#dilasi=cv2.erode(kuning,kernel)
		#dilasi=cv2.morphologyEx(kuning,cv2.MORPH_CLOSE,kernel)
		#dilasi=cv2.morphologyEx(kuning,cv2.MORPH_OPEN,kernel)
		#res = cv2.bitwise_and(self.img2,self.img2,mask=mata)
		(cnts,hierarch)=cv2.findContours(dilasi,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
		i = 0
		for c in cnts:
			area=cv2.contourArea(c)
			if area>1:
				#cv2.drawContours(self.img2,[c],-1,(255,0,255),3)
				#x,y,w,h = cv2.boundingRect(c)
				#self.img2=cv2.rectangle(self.img2,(x,y),(x+w,y+h),(0,255,0),2)
				#result_konturs = cv2.drawContours(self.img2,cnts,-1,(255,0,0),6)
				M=cv2.moments(c)
				cx=int(M["m10"]/M["m00"])
				cy=int(M["m01"]/M["m00"])

				#cv2.circle(self.img2,(cx,cy),7,(255,255,0),-1)
				#cv2.putText(self.img2,"center",(cx-20,cy-20),cv2.FONT_HERSHEY_SIMPLEX,0.5,(255,0,0),1)
				i +=1

		jumlah1 =int(i)-1
		#result_kontur = cv2.drawContours(self.img2,cnts,-1,(0,255,0),2)
		self.ui.lineEdit.setStyleSheet("color:rgb(0,0,0);\n" "background-color:rgb(255,255,255);")
		self.ui.lineEdit.setText(str(round(jumlah1)))

		#mendeteksi warna kuning
		#self.img2 = self.imgg.copy()
		bler = cv2.GaussianBlur(self.img2,(17,17),0)
		rgb = cv2.cvtColor(bler,cv2.COLOR_BGR2HSV)
		kuning_low = np.array([20,30,0],np.uint8)
		kuning_high = np.array([255,255,150],np.uint8)
		kuning = cv2.inRange(rgb,kuning_low,kuning_high)
		kernel=np.ones((1,1),"uint8")
		dilasi=cv2.dilate(kuning,kernel)
		#dilasi=cv2.erode(kuning,kernel)
		#dilasi=cv2.morphologyEx(kuning,cv2.MORPH_CLOSE,kernel)
		#dilasi=cv2.morphologyEx(kuning,cv2.MORPH_OPEN,kernel)
		res = cv2.bitwise_and(self.img2,self.img2,mask=kuning)
		(contours,hierarchy)=cv2.findContours(dilasi,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
		countours_count = 0
		result_konturs = cv2.drawContours(self.img2,contours,-1,(255,255,0),2)
		for pic, contour in enumerate(contours):
			area = cv2.contourArea(contour)
			if(area>150):
				x,y,w,h = cv2.boundingRect(contour)
				self.img2=cv2.rectangle(self.img2,(x,y),(x+w,y+h),(0,255,0),2)
				
				tek = "Terdapat {} poin dalam gambar".format(countours_count)
				font = cv2.FONT_HERSHEY_PLAIN
				#cv2.putText(result_konturs,tek,(15,20),font,2,(0,255,0),2,cv2.LINE_AA)
				#cv2.drawContours(self.img2,[contour],-1,(255,0,0),2)
				M=cv2.moments(contour)
				cx=int(M["m10"]/M["m00"])
				cy=int(M["m01"]/M["m00"])

				cv2.circle(self.img2,(cx,cy),3,(255,25,0),-1)
				#cv2.putText(self.img2,"center",(cx-20,cy-20),cv2.FONT_HERSHEY_SIMPLEX,0.5,(255,0,0),1)
				countours_count +=1
		#self.img2 = cv2.drawContours(self.img2,contours,-1,(0,0,150),2)
		jumlah2 =int(countours_count)
		self.ui.lineEdit_2 .setStyleSheet("color:rgb(0,0,0);\n" "background-color:rgb(255,255,255);")
		self.ui.lineEdit_2 .setText(str(round(jumlah2)))


		#menghitung jumlah kematangan nanas
		kematangan = jumlah2/ jumlah1*100.0 if jumlah1 !=0 else 0
		kematangan=int(kematangan)
		self.ui.lineEdit_3.setStyleSheet("color:rgb(0,0,0);\n" "background-color:rgb(255,255,255);")
		self.ui.lineEdit_3.setText(str(round(kematangan)))


		#self.img2=cv2.cvtColor(self.img2,cv2.COLOR_BGR2RGB)
		self.img2=cv2.resize(self.img2,(261,191),interpolation=cv2.INTER_AREA)
		height,width,channel=self.img2.shape
		step=channel*width
		self.img2=QImage(self.img2.data,width,height,step,QImage.Format_RGB888)
		self.ui.hasil.setPixmap(QPixmap.fromImage(self.img2))
	def save(self):
		if self.img1 is None:
			QMessageBox.about(self,"Peringatan!","Gambar belum di Capture")
		else:
			files_types="JPG(*.jpg);;PNG(*.png);;JPEG(*.jpeg);;TIFF(*.tiff);;BMP(*.bmp)"
			new_img_path,_=QFileDialog.getSaveFileName(self,'Save Image','./',files_types)
			img=self.imgg
			if new_img_path!='':
				new_img_path=str(new_img_path)
				nameFile=new_img_path.split(".")[0]
				ekstensiFile=new_img_path.split(".")[-1]
				cv2.imwrite(nameFile+'_Capture.'+ekstensiFile,cv2.cvtColor(self.imgg,cv2.COLOR_BGR2RGB))
			if ekstensiFile=='jpg'or ekstensiFile=='png'or ekstensiFile=='jpeg'or ekstensiFile=='bmp'or ekstensiFile=='tiff':
				QMessageBox.about(self,"Pemberitahuan!","Gambar tersimpan")

	def exit(self):
		qm=QMessageBox.question(self,'Confirm Quit',"Apakah Anda Yakin Ingin Keluar?",QMessageBox.Yes|QMessageBox.No)
		if qm ==QMessageBox.Yes:
			self.close()
			return True 
		else:
			return False




if __name__=='__main__':
	app=QApplication(sys.argv)
	x=MainWindow()
	x.show()
	sys.exit(app.exec_())

