import sys
from PyQt6.QtWidgets import *
from PyQt6 import uic 
from PyQt6.QtCore import *

import json
import re
import tkinter as tk
from tkinter import Listbox



# Đọc dữ liệu từ tệp JSON
with open('./account.json', 'r') as file:
    data_account = json.load(file)
    
with open('./note.json', 'r') as file:
    data_main = json.load(file)

    
class LoginPage(QMainWindow, QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi("login.ui", self)
        self.btnLogin.clicked.connect(self.checkLogin)
        self.btn_register.clicked.connect(self.register)
    def checkLogin(self):
        email = self.txtEmail.text()
        password = self.txtPassword.text()
        found = False
        for account in data_account:
            if account['email'] == email and account['password'] == password:
                msg_box.setText("Right")
                msg_box.exec()
                MainPage.show()
                self.close()
                found = True
                break

        if not found:
            msg_box.setText("Incorrect email or password")
            msg_box.exec()
    def register(self):
        RegisterPage.show()
        self.close()
        return
        

class RegisterPage(QMainWindow, QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi("register.ui", self)
        self.btnRegister.clicked.connect(self.checkRegister)
    def checkRegister(self):
        name = self.txtFullName.text()
        email = self.txtEmail.text()
        password = self.txtPassword.text()
        email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'

        if name == '':
            msg_box.setText('Vui lòng nhập tên')
            msg_box.exec()
            return
        # Check if email is empty
        if email == '':
            msg_box.setText('Vui lòng nhập tài khoản')
            msg_box.exec()
            return
    
    # Use re.match to see if the email matches the pattern
        if not re.match(email_regex, email):
            msg_box.setText('Tài khoản chưa nhập đúng định dạng')
            msg_box.exec()
            return 
            

        # Check if email already exists
        for account in data_account:  # Ensure data_account is accessible
            if email == account['email']:
                msg_box.setText('Tài khoản đã tồn tại')
                msg_box.exec()
                return
            
        # Check password length
        if len(password) < 8:
            msg_box.setText("Password must be at least 8 characters long.")
            msg_box.exec()
            return
        
        # Check for presence of at least one digit
        if not re.search(r"\d", password):
            msg_box.setText("Password must include at least one digit.")
            msg_box.exec()
            return
        
        # Check for presence of at least one uppercase letter
        if not re.search(r"[A-Z]", password):
            msg_box.setText("Password must include at least one uppercase letter.")
            msg_box.exec()
            return
        
        # Check for presence of at least one lowercase letter
        if not re.search(r"[a-z]", password):
            msg_box.setText("Password must include at least one lowercase letter.")
            msg_box.exec()
            return
        
        # Check for presence of at least one special character
        if not re.search(r"[!@#\$%\^&\*]", password):
            msg_box.setText("Password must include at least one special character.")
            msg_box.exec()
            return

        # If all checks pass
        new_account = {
        "email": email,
        "password": password
        }
        data_account.append(new_account)    
        with open('account.json', "w") as json_file:
            json.dump(data_account, json_file, indent=4) 
        LoginPage.show()
        self.close()
        
    
        

            
class MainPage(QMainWindow, QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi("main1.ui", self)
        self.anime_item_list = self.load_data()
        self.load_data_UI(self.anime_item_list)

        # self.load_data()
        self.searchAnime.clicked.connect(self.search_item)
        self.editButton.clicked.connect(self.edit_item)
        self.removeButton.clicked.connect(self.delete_item)
        self.addButton.clicked.connect(self.open_add_dialog)
    def load_data(self):
        with open('note.json', 'r') as f:
            # self.anime_item_list = json.load(f)
            return json.load(f)
    def load_data_UI(self,anime_item_list):
        # with open('note.json', 'r') as file:
        #     data = json.load(file)
        
        for item in anime_item_list:
            title = item['title']
            self.animeList1.addItem(QListWidgetItem(title))
        if self.animeList1.count() > 0:
            self.animeList1.setCurrentRow(0)  # Set the first item as selected
    def search_item(self):
        search_text = self.inputAnime.text().lower()  # Get text from QLineEdit and convert to lower case
        self.animeList1.clear()  # Clear all items in the list
        for item in self.anime_item_list:
            if search_text in item['title'].lower():  # Check if search text is in the title
                self.animeList1.addItem(QListWidgetItem(item['title']))
    
    def open_add_dialog(self):
        dialog = AddDialog()
        if dialog.exec():
            self.load_data_UI()  # Reload data into the UI after adding
    
    def edit_item(self):
        current_item = self.animeList1.currentItem()
        if current_item:
            anime_info = self.find_anime_info(current_item.text())
            if anime_info:
                dialog = EditDialog(anime_info)
                if dialog.exec():
                    updated_info = dialog.get_updated_info()
                    self.update_anime_info(current_item.text(), updated_info)
    
            
    def update_anime_info(self, old_title, new_info):
        for i, anime in enumerate(self.animeList):
            if anime['title'] == old_title:
                self.animeList[i] = new_info
                self.refresh_ui()
                break
    def find_anime_info(self, title):
        for anime in self.anime_item_list:
            if anime['title'] == title:
                return anime

    def refresh_ui(self):
        self.animeList1.clear()
        for anime in self.animeList:
            self.animeList1.addItem(anime['title'])
        self.animeList1.setCurrentRow(0)
                
    # def edit_item(self):
    #     EditDialog.show()
    def delete_item(self):
        current_item = self.animeList1.currentItem()
        if not current_item:
            QMessageBox.warning(self, "Selection Required", "Please select an item to delete.")
            return

        reply = QMessageBox.question(self, "Confirm Delete", "Are you sure you want to delete this item?",
                                     QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                                     QMessageBox.StandardButton.No)

        if reply == QMessageBox.StandardButton.Yes:
            title = current_item.text()
            # Xóa khỏi QListWidget
            row = self.animeList1.row(current_item)
            self.animeList1.takeItem(row)
            # Xóa khỏi cơ sở dữ liệu
            self.delete_item_from_data(title)
            QMessageBox.information(self, "Item Deleted", "The item has been successfully deleted.")

    def delete_item_from_data(self, title):
        for i, item in enumerate(self.anime_item_list):
            if item['title'] == title:
                del self.anime_item_list[i]
                break
        # Lưu lại thay đổi vào file JSON
        with open('note.json', 'w') as file:
            json.dump(self.anime_item_list, file, indent=4)
    
        
class EditDialog(QDialog):
    def __init__(self,anime_info):
        super().__init__()
        uic.loadUi("edit_dialog.ui", self)
        self.titleInput.setText(anime_info['title'])
        self.releasedateInput.setDate(QDate.fromString(anime_info['release_date'], "dd/MM/yyyy"))
        self.ratingInput.setText(str(anime_info['rating']))
        self.urlInput.setText(anime_info['image'])
    def load_data(self):
        with open('note.json', 'r') as f:
            # self.anime_item_list = json.load(f)
            return json.load(f)
    def get_updated_info(self):
        return {
            'title': self.newTitleLineEdit.text(),
            'release_date': self.newReleaseDateEdit.date().toPyDate(),
            'rating': int(self.newRatingLineEdit.text()),
            'url': self.newUrlLineEdit.text()
        }
        
class AddDialog(QDialog):
    def __init__(self):
        super().__init__()
        uic.loadUi("add_dialog.ui", self)
        self.buttonBox.clicked.connect(self.save_item)

    def save_item(self):
        title = self.titleInput.text()
        release_date = self.releasedateInput.text()  # Giả sử đây là QLineEdit
        rating = self.ratingInput.text()
        url = self.urlInput.text()

        new_item = {
            "title": title,
            "release_date": release_date,
            "rating": rating,
            "url": url
        }

        if self.add_item_to_json(new_item):
            QMessageBox.information(self, "Success", "Item added successfully.")
            self.accept()  # Close the dialog after saving
        else:
            QMessageBox.warning(self, "Error", "Failed to add item.")
    def add_item_to_json(self, item):
        try:
            with open('note.json', 'r+') as file:
                data = json.load(file)
                data.append(item)
                file.seek(0)  # Rewind file to the beginning
                json.dump(data, file, indent=4)
                file.truncate()  # Remove leftover data
            return True
        except Exception as e:
            print(f"An error occurred: {e}")
            return False
        
        
        
        
        
        
if __name__ == '__main__':
    app = QApplication(sys.argv)
    msg_box = QMessageBox()
    LoginPage = LoginPage()
    RegisterPage = RegisterPage()
    # EditDialog = EditDialog()
    MainPage = MainPage()
    # MainPage.load_json_to_listwidget('note.json')  
    MainPage.show()

    sys.exit(app.exec())