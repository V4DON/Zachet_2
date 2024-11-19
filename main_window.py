from PySide6.QtWidgets import QMainWindow, QWidget, QTableWidget, QTableWidgetItem, QVBoxLayout, QHBoxLayout, QLineEdit, QPushButton
from user_class import TimeEntries, Connect
from PySide6.QtGui import QIcon


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        
        self.setWindowTitle("Задачи")
        self.resize(800, 600)
        self.session = Connect.create_connection()
        self.setWindowIcon(QIcon('ivon.png')) # Иконка окна
        self.setStyleSheet("@widget { background-color: white }")
        self.setup_ui()
    
    def search(self, text):
        if self.current_table_data is None:
            return

        self.table.setRowCount(0)
        for item in self.current_table_data:
            if self.matches_search(item, text):
                row_position = self.table.rowCount()
                self.table.insertRow(row_position)
                self.populate_row(row_position, item)
    
    def matches_search(self, item, text):
        text = text.lower()
        if isinstance(item, TimeEntries):
            return text in item.description.lower()
        else:
            print("BBBB")
    
    def setup_ui(self):
        self.table = QTableWidget()
        self.table.setHorizontalHeaderLabels([])

        self.search_line = QLineEdit()
        self.search_line.setPlaceholderText("Введите Данные")
        self.search_line.setFixedSize(200, 30)
        self.search_line.textChanged.connect(self.search)
        
        self.button1 = QPushButton(text="Задачи")
        self.button1.setFixedSize(100, 60)
        self.button1.clicked.connect(self.update_table)
        
        self.add_button = QPushButton(text="Добавить")
        self.add_button.setFixedSize(100, 60)
        self.add_button.clicked.connect(self.add_partner)
        
        self.layout2 = QVBoxLayout()
        self.layout2.addWidget(self.search_line)
        self.layout2.addWidget(self.button1)
        self.layout2.addWidget(self.add_button)
        
        self.layout = QHBoxLayout()
        self.layout.addLayout(self.layout2)
        self.layout.addWidget(self.table)
        
        widget = QWidget()
        widget.setLayout(self.layout)
        self.setCentralWidget(widget)

    def update_table(self):
        self.search_line.setMaxLength(20)
        self.search_line.setPlaceholderText(" ")
        self.table.setRowCount(0)
        timeentries = self.session.query(TimeEntries).order_by(TimeEntries.id).all()
        self.table.setColumnCount(3)
        self.current_table_data = timeentries
        self.table.setHorizontalHeaderLabels(["ID", "Описание", "Продолжительность"])
        for timeentry in timeentries:
            row_position = self.table.rowCount()
            self.table.insertRow(row_position)
            self.populate_row(row_position, timeentry)

    def populate_row(self, row_position, item):
        if isinstance(item, TimeEntries):
            self.table.setItem(row_position, 0, QTableWidgetItem(str(item.id)))
            self.table.setItem(row_position, 1, QTableWidgetItem(str(item.description)))
            self.table.setItem(row_position, 2, QTableWidgetItem(str(item.duration)))


    def add_partner(self):
        # Открываем окно для ввода информации о новом партнёре
        from PySide6.QtWidgets import (
            QDialog,
            QVBoxLayout,
            QLabel,
            QLineEdit,
            QPushButton
        )

        dialog = QDialog(self)
        dialog.setWindowTitle("Добавить задачу")
        dialog.setModal(True)
        dialog.resize(300, 200)

        layout = QVBoxLayout()

        description_label = QLabel("Название задачи:")
        description_input = QLineEdit()
        layout.addWidget(description_label)
        layout.addWidget(description_input)

        duration_label = QLabel("Время:")
        duration_input = QLineEdit()
        layout.addWidget(duration_label)
        layout.addWidget(duration_input)

        save_button = QPushButton("Сохранить")
        cancel_button = QPushButton("Отмена")
        layout.addWidget(save_button)
        layout.addWidget(cancel_button)
    


        def save_partner():
            description_n = description_input.text().strip()
            duration_n = duration_input.text().strip()
            if not description_n or not description_n:
                from PySide6.QtWidgets import QMessageBox
                QMessageBox.warning(dialog,"Ошибка","Все поля должны быть заполнены!")
                return
            # Сохраняем данные в базу
            new_timeentries = TimeEntries(description=description_n, duration=duration_n)
            self.session.add(new_timeentries)
            self.session.commit()
            # Обновляем таблицу и закрываем диалог
            self.update_table()
            dialog.accept()

        save_button.clicked.connect(save_partner)
        cancel_button.clicked.connect(dialog.reject)

        dialog.setLayout(layout)
        dialog.exec_()

