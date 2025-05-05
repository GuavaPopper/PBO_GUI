from PySide6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                              QPushButton, QLabel, QMessageBox, QTextEdit, 
                              QFileDialog, QFrame)
from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap, QImage
from PIL import Image
import os
import shutil
from datetime import datetime
from database import Database
from ekstraksi import EkstraksiTeks

class EditWindow(QMainWindow):
    def __init__(self, parent=None, data=None):
        super().__init__()
        self.parent = parent
        self.db = Database()
        self.ekstractor = EkstraksiTeks()
        self.data = data
        self.path_gambar = data['lokasi_file'] if data else None
        self.hasil_ekstraksi = data['hasil_ekstraksi'] if data else ""
        self.setup_ui()
        self.setWindowTitle("Ubah Data")
        self.setMinimumSize(800, 600)
        
        # Load existing data
        if self.data:
            self.load_data()
        
    def setup_ui(self):
        # Main widget and layout
        main_widget = QWidget()
        main_layout = QVBoxLayout(main_widget)
        
        # Title
        title = QLabel("Aplikasi Ekstraksi Text dari Citra")
        title.setObjectName("title")
        title.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(title)
        
        # Content area (image and extraction result)
        content_layout = QHBoxLayout()
        
        # Image preview section
        preview_frame = QFrame()
        preview_frame.setObjectName("card")
        preview_layout = QVBoxLayout(preview_frame)
        
        # File name label
        self.file_name_label = QLabel()
        self.file_name_label.setAlignment(Qt.AlignCenter)
        preview_layout.addWidget(self.file_name_label)
        
        # Image preview area
        self.image_label = QLabel()
        self.image_label.setMinimumSize(400, 300)
        self.image_label.setAlignment(Qt.AlignCenter)
        self.image_label.setStyleSheet("""
            QLabel {
                background-color: #1E1E1E;
                border: 2px dashed #333333;
                border-radius: 4px;
                color: #666666;
            }
        """)
        preview_layout.addWidget(self.image_label)
        
        # Open file button
        open_btn = QPushButton("Ubah File")
        open_btn.clicked.connect(self.buka_file)
        open_btn.setMinimumHeight(40)
        preview_layout.addWidget(open_btn)
        
        # Result section
        result_frame = QFrame()
        result_frame.setObjectName("card")
        result_layout = QVBoxLayout(result_frame)
        
        result_title = QLabel("Hasil Ekstraksi")
        result_title.setObjectName("title")
        result_layout.addWidget(result_title)
        
        self.result_text = QTextEdit()
        self.result_text.setReadOnly(True)
        self.result_text.setMinimumHeight(100)
        result_layout.addWidget(self.result_text)
        
        # Add frames to content layout with proper proportions
        content_layout.addWidget(preview_frame)
        content_layout.addWidget(result_frame)
        
        main_layout.addLayout(content_layout)
        
        # Buttons
        buttons_layout = QHBoxLayout()
        
        cancel_btn = QPushButton("Batal")
        cancel_btn.clicked.connect(self.clear_fields)
        cancel_btn.setObjectName("secondary")
        buttons_layout.addWidget(cancel_btn)
        
        save_btn = QPushButton("Simpan")
        save_btn.clicked.connect(self.simpan_data)
        buttons_layout.addWidget(save_btn)
        
        main_layout.addLayout(buttons_layout)
        
        # Back button
        back_layout = QHBoxLayout()
        back_btn = QPushButton("Kembali")
        back_btn.setObjectName("danger")
        back_btn.clicked.connect(self.kembali)
        back_layout.addWidget(back_btn)
        
        main_layout.addLayout(back_layout)
        
        # Set central widget
        self.setCentralWidget(main_widget)
        
        # Set dark theme stylesheet
        self.setStyleSheet("""
            QMainWindow, QWidget {
                background-color: #1E1E1E;
                color: #FFFFFF;
            }
            QPushButton {
                background-color: #2176AE;
                color: white;
                border: none;
                padding: 8px 16px;
                border-radius: 4px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #1565C0;
            }
            QPushButton#secondary {
                background-color: #333333;
                color: #FFFFFF;
            }
            QPushButton#secondary:hover {
                background-color: #404040;
            }
            QPushButton#danger {
                background-color: #C62828;
            }
            QPushButton#danger:hover {
                background-color: #B71C1C;
            }
            QTextEdit {
                background-color: #2D2D2D;
                border: 1px solid #333333;
                padding: 8px;
                border-radius: 4px;
                color: #FFFFFF;
            }
            QLabel {
                color: #FFFFFF;
            }
            QLabel#title {
                font-size: 18px;
                font-weight: bold;
                margin: 10px 0;
            }
            QFrame#card {
                background-color: #2D2D2D;
                border-radius: 8px;
                padding: 16px;
                margin: 8px;
            }
        """)
        
    def load_data(self):
        # Set file name label
        self.file_name_label.setText(self.data['nama_file'])
        
        # Load image if exists
        if os.path.exists(self.data['lokasi_file']):
            img = Image.open(self.data['lokasi_file'])
            img.thumbnail((300, 300))
            
            # Convert PIL image to QPixmap
            img_data = img.convert("RGBA").tobytes("raw", "RGBA")
            qimg = QImage(img_data, img.width, img.height, QImage.Format_RGBA8888)
            pixmap = QPixmap.fromImage(qimg)
            
            self.image_label.setPixmap(pixmap)
        
        # Set result text
        self.result_text.setText(self.data['hasil_ekstraksi'])
        
    def buka_file(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Pilih Gambar", "", "Image Files (*.jpg *.jpeg *.png)"
        )
        
        if file_path:
            self.path_gambar = file_path
            nama_file = os.path.basename(file_path)
            self.file_name_label.setText(nama_file)
            
            # Display image
            img = Image.open(file_path)
            img.thumbnail((300, 300))
            
            # Convert PIL image to QPixmap
            img_data = img.convert("RGBA").tobytes("raw", "RGBA")
            qimg = QImage(img_data, img.width, img.height, QImage.Format_RGBA8888)
            pixmap = QPixmap.fromImage(qimg)
            
            self.image_label.setPixmap(pixmap)
            
            # Extract text
            hasil = self.ekstractor.ekstrak(file_path)
            self.result_text.setText(hasil)
            self.hasil_ekstraksi = hasil
            
    def simpan_data(self):
        if not self.path_gambar:
            QMessageBox.warning(self, "Peringatan", "Pilih gambar terlebih dahulu!")
            return
            
        hasil_ekstraksi = self.result_text.toPlainText()
        if not hasil_ekstraksi:
            QMessageBox.warning(self, "Peringatan", "Hasil ekstraksi tidak boleh kosong!")
            return
            
        # Handle file if changed
        nama_file = os.path.basename(self.path_gambar)
        lokasi_file = self.path_gambar
        
        # If file path changed, save to gambar folder
        if self.path_gambar != self.data['lokasi_file']:
            folder_gambar = "gambar"
            if not os.path.exists(folder_gambar):
                os.makedirs(folder_gambar)
                
            lokasi_baru = os.path.join(folder_gambar, nama_file)
            shutil.copy(self.path_gambar, lokasi_baru)
            lokasi_file = lokasi_baru
            
        tanggal_input = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # Update database
        self.db.conn.execute(
            "UPDATE files SET nama_file=?, lokasi_file=?, hasil_ekstraksi=?, tanggal=? WHERE id=?",
            (nama_file, lokasi_file, hasil_ekstraksi, tanggal_input, self.data['id'])
        )
        self.db.conn.commit()
        
        QMessageBox.information(self, "Sukses", "Data berhasil diubah!")
        self.kembali()
        
    def clear_fields(self):
        # Reset to original data
        self.load_data()
        QMessageBox.information(self, "Info", "Form telah direset ke data semula")
        
    def kembali(self):
        if self.parent:
            self.parent.show()
            self.parent.populate_table()
        self.close() 