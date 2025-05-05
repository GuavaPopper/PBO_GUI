from PySide6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                              QPushButton, QLabel, QMessageBox, QTextEdit, QFrame)
from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap, QImage
from PIL import Image
import os
from database import Database

class DeleteWindow(QMainWindow):
    def __init__(self, parent=None, data=None):
        super().__init__()
        self.parent = parent
        self.db = Database()
        self.data = data
        self.setup_ui()
        self.setWindowTitle("Hapus Data")
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
        
        # Confirmation label
        self.confirm_label = QLabel("Apakah Anda yakin ingin menghapus data ini?")
        self.confirm_label.setAlignment(Qt.AlignCenter)
        self.confirm_label.setStyleSheet("color: #FF5252; font-size: 16px; font-weight: bold; margin: 10px 0;")
        main_layout.addWidget(self.confirm_label)
        
        # File name label
        self.file_name_label = QLabel()
        self.file_name_label.setAlignment(Qt.AlignCenter)
        self.file_name_label.setStyleSheet("color: #FFFFFF; margin: 5px 0;")
        main_layout.addWidget(self.file_name_label)
        
        # Content area (image and extraction result)
        content_layout = QHBoxLayout()
        
        # Image preview section
        preview_frame = QFrame()
        preview_frame.setObjectName("card")
        preview_layout = QVBoxLayout(preview_frame)
        
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
        
        self.delete_btn = QPushButton("HAPUS")
        self.delete_btn.setObjectName("danger")
        self.delete_btn.clicked.connect(self.hapus_data)
        buttons_layout.addWidget(self.delete_btn)
        
        main_layout.addLayout(buttons_layout)
        
        # Back button
        back_layout = QHBoxLayout()
        back_btn = QPushButton("Kembali")
        back_btn.setObjectName("secondary")
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
        
    def hapus_data(self):
        # Confirm deletion
        result = QMessageBox.question(
            self, 
            "Konfirmasi Hapus", 
            f"Anda yakin ingin menghapus data {self.data['nama_file']}?",
            QMessageBox.Yes | QMessageBox.No
        )
        
        if result == QMessageBox.Yes:
            # Delete from database
            self.db.conn.execute("DELETE FROM files WHERE id=?", (self.data['id'],))
            self.db.conn.commit()
            
            QMessageBox.information(self, "Sukses", "Data berhasil dihapus!")
            self.kembali()
        
    def kembali(self):
        if self.parent:
            self.parent.show()
            self.parent.populate_table()
        self.close() 