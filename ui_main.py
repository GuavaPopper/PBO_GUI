from PySide6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                              QPushButton, QLabel, QLineEdit, QTableWidget, 
                              QTableWidgetItem, QHeaderView, QMessageBox, 
                              QTextEdit, QFrame, QGridLayout)
from PySide6.QtCore import Qt, Signal, QSize
from PySide6.QtGui import QPixmap, QImage, QColor, QFont
from database import Database
from PIL import Image
import os

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.db = Database()
        self.setup_ui()
        self.populate_table()
        self.current_image = None
        self.setMinimumSize(1000, 600)
        # Set stylesheet for Material Design look
        self.setStyleSheet("""
            QMainWindow, QWidget {
                background-color: #F5F5F5;
                color: #424242;
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
            QPushButton#danger {
                background-color: #F44336;
            }
            QPushButton#danger:hover {
                background-color: #D32F2F;
            }
            QPushButton#warning {
                background-color: #FF9800;
                color: #212121;
            }
            QPushButton#warning:hover {
                background-color: #F57C00;
            }
            QLineEdit, QTextEdit {
                border: 1px solid #BDBDBD;
                padding: 8px;
                border-radius: 4px;
                background-color: white;
            }
            QLabel#title {
                font-size: 20px;
                font-weight: bold;
                color: #212121;
            }
            QTableWidget {
                border: 1px solid #E0E0E0;
                gridline-color: #E0E0E0;
                selection-background-color: #2176AE;
                selection-color: white;
            }
            QHeaderView::section {
                background-color: #EEEEEE;
                padding: 4px;
                border: 1px solid #E0E0E0;
                font-weight: bold;
            }
            QFrame#card {
                background-color: white;
                border-radius: 4px;
                border: 1px solid #E0E0E0;
            }
        """)

    def setup_ui(self):
        # Main widget and layout
        main_widget = QWidget()
        main_layout = QVBoxLayout(main_widget)
        
        # Title
        title = QLabel("Aplikasi Ekstraksi Text dari Citra")
        title.setObjectName("title")
        title.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(title)
        
        # Content area
        content_layout = QHBoxLayout()
        
        # Left section (Database table)
        left_frame = QFrame()
        left_frame.setObjectName("card")
        left_layout = QVBoxLayout(left_frame)
        
        # Database title
        db_title = QLabel("Database Gambar")
        db_title.setObjectName("title")
        left_layout.addWidget(db_title)
        
        # Search
        search_layout = QHBoxLayout()
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Tulis lalu Enter untuk mencari")
        self.search_input.returnPressed.connect(self.search_data)
        search_btn = QPushButton("Cari")
        search_btn.clicked.connect(self.search_data)
        search_layout.addWidget(self.search_input)
        search_layout.addWidget(search_btn)
        left_layout.addLayout(search_layout)
        
        # Table
        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(["No", "Nama Gambar", "Lokasi File", "Tanggal Ditambahkan"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.setSelectionBehavior(QTableWidget.SelectRows)
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.table.selectionModel().selectionChanged.connect(self.item_selected)
        left_layout.addWidget(self.table)
        
        # Right section (Preview and Results)
        right_frame = QFrame()
        right_frame.setObjectName("card")
        right_layout = QVBoxLayout(right_frame)
        
        # Preview title with dynamic filename
        preview_title = QLabel("Pratinjau Gambar: ")
        preview_title.setObjectName("title")
        right_layout.addWidget(preview_title)
        
        self.file_name_label = QLabel()
        self.file_name_label.setAlignment(Qt.AlignCenter)
        right_layout.addWidget(self.file_name_label)
        
        # Image preview
        self.image_label = QLabel()
        self.image_label.setMinimumSize(400, 300)
        self.image_label.setAlignment(Qt.AlignCenter)
        self.image_label.setStyleSheet("background-color: #F5F5F5; border: 1px solid #E0E0E0; border-radius: 4px;")
        right_layout.addWidget(self.image_label)
        
        # Extraction results
        result_title = QLabel("Hasil Ekstraksi")
        result_title.setObjectName("title")
        right_layout.addWidget(result_title)
        
        self.result_text = QTextEdit()
        self.result_text.setReadOnly(True)
        self.result_text.setMinimumHeight(100)
        self.result_text.setStyleSheet("background-color: white;")
        right_layout.addWidget(self.result_text)
        
        # Add sections to content layout with proper proportions
        content_layout.addWidget(left_frame, 3)  # Left section takes 3 parts
        content_layout.addWidget(right_frame, 2)  # Right section takes 2 parts
        
        main_layout.addLayout(content_layout)
        
        # Buttons
        buttons_layout = QHBoxLayout()
        
        self.add_btn = QPushButton("TAMBAH")
        self.add_btn.clicked.connect(self.open_add)
        buttons_layout.addWidget(self.add_btn)
        
        self.edit_btn = QPushButton("UBAH")
        self.edit_btn.setObjectName("warning")
        self.edit_btn.clicked.connect(self.open_edit)
        buttons_layout.addWidget(self.edit_btn)
        
        self.delete_btn = QPushButton("HAPUS")
        self.delete_btn.setObjectName("danger")
        self.delete_btn.clicked.connect(self.open_delete)
        buttons_layout.addWidget(self.delete_btn)
        
        main_layout.addLayout(buttons_layout)
        
        # Exit button
        exit_layout = QHBoxLayout()
        self.exit_btn = QPushButton("KELUAR")
        self.exit_btn.setObjectName("danger")
        self.exit_btn.clicked.connect(self.close)
        exit_layout.addStretch()
        exit_layout.addWidget(self.exit_btn)
        
        main_layout.addLayout(exit_layout)
        
        # Set the central widget
        self.setCentralWidget(main_widget)

    def populate_table(self):
        # Clear existing rows
        self.table.setRowCount(0)
        
        # Get data from database
        cursor = self.db.conn.execute("SELECT id, nama_file, lokasi_file, hasil_ekstraksi, tanggal FROM files ORDER BY id ASC")
        
        for row_data in cursor:
            row = self.table.rowCount()
            self.table.insertRow(row)
            
            # Add data to row (skip the number column)
            self.table.setItem(row, 0, QTableWidgetItem(row_data[1]))  # nama_file
            self.table.setItem(row, 1, QTableWidgetItem(row_data[2]))  # lokasi_file
            self.table.setItem(row, 2, QTableWidgetItem(row_data[4]))  # tanggal
            self.table.setItem(row, 3, QTableWidgetItem(row_data[3]))  # hasil_ekstraksi
            
            # Store the DB ID as data in the first column
            self.table.item(row, 0).setData(Qt.UserRole, row_data[0])

    def search_data(self):
        search_text = self.search_input.text().lower()
        
        # If search is empty, reset display
        if not search_text:
            self.populate_table()
            self.reset_preview()
            return
        
        # Clear table
        self.table.setRowCount(0)
        
        # Get all data from database
        cursor = self.db.conn.execute("SELECT id, nama_file, lokasi_file, hasil_ekstraksi, tanggal FROM files ORDER BY id ASC")
        
        found = False
        found_data = None
        
        # Filter and display matching rows
        for idx, row in enumerate(cursor, start=1):
            # Check if search text matches No or nama_file
            if (search_text == str(idx).lower() or search_text in str(row[1]).lower()):
                self.table.insertRow(self.table.rowCount())
                
                # Add data to row
                self.table.setItem(self.table.rowCount() - 1, 0, QTableWidgetItem(row[1]))
                self.table.setItem(self.table.rowCount() - 1, 1, QTableWidgetItem(row[2]))
                self.table.setItem(self.table.rowCount() - 1, 2, QTableWidgetItem(row[4]))
                self.table.setItem(self.table.rowCount() - 1, 3, QTableWidgetItem(row[3]))
                
                # Store the DB ID as data in the first column
                self.table.item(self.table.rowCount() - 1, 0).setData(Qt.UserRole, row[0])
                
                found = True
                found_data = {'id': row[0], 'nama_file': row[1], 'lokasi_file': row[2], 
                            'hasil_ekstraksi': row[3], 'tanggal': row[4]}
        
        if found:
            # Show success message
            QMessageBox.information(self, "Sukses", f"{found_data['nama_file']} ditemukan")
            
            # Display preview
            self.display_preview(found_data)
            
            # Auto select row if only one result
            if self.table.rowCount() == 1:
                self.table.selectRow(0)
        else:
            QMessageBox.information(self, "Info", "Data tidak ditemukan")
            self.reset_preview()
            self.populate_table()

    def item_selected(self):
        selected = self.table.selectedItems()
        if not selected:
            return
        
        row = selected[0].row()
        db_id = self.table.item(row, 0).data(Qt.UserRole)
        
        # Get full data from database
        cursor = self.db.conn.execute("SELECT id, nama_file, lokasi_file, hasil_ekstraksi, tanggal FROM files WHERE id=?", (db_id,))
        row_data = cursor.fetchone()
        
        if row_data:
            data = {
                'id': row_data[0],
                'nama_file': row_data[1],
                'lokasi_file': row_data[2],
                'hasil_ekstraksi': row_data[3],
                'tanggal': row_data[4]
            }
            self.display_preview(data)

    def display_preview(self, data):
        # Display file name
        self.file_name_label.setText(data['nama_file'])
        
        # Display image
        if os.path.exists(data['lokasi_file']):
            # Load image with PIL
            img = Image.open(data['lokasi_file'])
            img.thumbnail((250, 250))
            
            # Convert PIL image to QPixmap
            img_data = img.convert("RGBA").tobytes("raw", "RGBA")
            qimg = QImage(img_data, img.width, img.height, QImage.Format_RGBA8888)
            pixmap = QPixmap.fromImage(qimg)
            
            self.image_label.setPixmap(pixmap)
        
        # Display extraction results
        self.result_text.setText(data['hasil_ekstraksi'])

    def reset_preview(self):
        # Reset image
        self.image_label.clear()
        self.current_image = None
        
        # Reset extraction results
        self.result_text.clear()
        
        # Reset file name
        self.file_name_label.setText("Nama File.jpg")

    def open_add(self):
        from ui_tambah import AddWindow
        self.add_window = AddWindow(self)
        self.add_window.show()
        self.hide()

    def open_edit(self):
        selected = self.table.selectedItems()
        if not selected:
            QMessageBox.warning(self, "Peringatan", "Pilih data yang ingin diubah!")
            return
        
        row = selected[0].row()
        db_id = self.table.item(row, 0).data(Qt.UserRole)
        
        # Get full data from database
        cursor = self.db.conn.execute("SELECT id, nama_file, lokasi_file, hasil_ekstraksi, tanggal FROM files WHERE id=?", (db_id,))
        row_data = cursor.fetchone()
        
        data = {
            'id': row_data[0],
            'nomor_urut': self.table.item(row, 0).text(),
            'nama_file': row_data[1],
            'lokasi_file': row_data[2],
            'hasil_ekstraksi': row_data[3],
            'tanggal': row_data[4]
        }
        
        from ui_ubah import EditWindow
        self.edit_window = EditWindow(self, data)
        self.edit_window.show()
        self.hide()

    def open_delete(self):
        selected = self.table.selectedItems()
        if not selected:
            QMessageBox.warning(self, "Peringatan", "Pilih data yang ingin dihapus!")
            return
        
        row = selected[0].row()
        db_id = self.table.item(row, 0).data(Qt.UserRole)
        
        # Get full data from database
        cursor = self.db.conn.execute("SELECT id, nama_file, lokasi_file, hasil_ekstraksi, tanggal FROM files WHERE id=?", (db_id,))
        row_data = cursor.fetchone()
        
        data = {
            'id': row_data[0],
            'nomor_urut': self.table.item(row, 0).text(),
            'nama_file': row_data[1],
            'lokasi_file': row_data[2],
            'hasil_ekstraksi': row_data[3],
            'tanggal': row_data[4]
        }
        
        from ui_hapus import DeleteWindow
        self.delete_window = DeleteWindow(self, data)
        self.delete_window.show()
        self.hide()