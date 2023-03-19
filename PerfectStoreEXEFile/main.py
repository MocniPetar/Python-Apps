import kivy
kivy.require("2.1.0")

from kivymd.app import MDApp
from kivy.uix.screenmanager import ScreenManager, NoTransition
from kivymd.uix.screen import MDScreen
from kivy.properties import DictProperty
from kivy.core.window import Window
from kivymd.uix.list import TwoLineIconListItem, IconLeftWidget
from kivymd.uix.card import MDCard
from kivymd.uix.button import MDFlatButton, MDFloatingActionButton
from kivymd.uix.textfield import MDTextField
from kivymd.uix.floatlayout import MDFloatLayout
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.menu import MDDropdownMenu
from kivy.uix.textinput import TextInput
from kivymd.uix.swiper import MDSwiper, MDSwiperItem
from kivymd.uix.label import MDLabel
from kivymd.uix.snackbar import Snackbar
from database import save_to_database
from ItemsDatabase import items_database

##Mail##
class MailScreen(MDScreen):
    pass

##Phonebook##
class PhonebookScreen(MDScreen):
    
    card = None
    textField_1 = None
    textField_2 = None
    listOfPeople = []
        
    def add_card(self):
        
        self.textField_1 = MDTextField(
            hint_text = "Name",
            helper_text = "Max. Num. of characters is 16",
            helper_text_mode = "persistent",
            font_size = 25,
            size_hint_x = .8,
            pos_hint = {'center_x': .5,'center_y': .8}
        )
        
        self.textField_2 = MDTextField(
            hint_text = "Number",
            helper_text = "Max. Num. of characters is 12",
            helper_text_mode = "persistent",
            font_size = 25,
            size_hint_x = .8,
            pos_hint = {'center_x': .5,'center_y': .45}
        )
        
        self.card = MDCard(
            MDFloatLayout(
                self.textField_1,
                self.textField_2,
                MDFlatButton(
                    text = "OK",
                    size_hint = (.2, .2),
                    pos_hint = {'center_x': 0.85,'center_y': 0.15},
                    on_release = self.AddPerson
                ),
                MDFlatButton(
                    text = "CANCEL",
                    size_hint = (.2, .2),
                    pos_hint = {'center_x': 0.6,'center_y': 0.15},
                    on_release = self.Cancel
                ),
                size = self.size
            ),
            orientation = 'vertical',
            size_hint = (.7, .2),
            pos_hint = {'center_x': 0.5,'center_y': 0.5},
            elevation = 3,
            radius = [10]
        )
        self.add_widget(self.card)
            
    def AddPerson(self, obj):
        
        name = str(self.textField_1.text)
        number = str(self.textField_2.text)
        
        if len(name) > 16 or len(number) > 12:
            Snackbar(text="Maximum number of characters exceeded!", snackbar_x=10, snackbar_y=10, size_hint_y=.08,
                     size_hint_x=(Window.width - (10 * 2)) / Window.width, bg_color=(0, 153/250, 1, 255/250)).open()
        else:
            database = r"database.db"
            conn = save_to_database.create_connection(database)

            with conn:
                    phonebook = (str(name), str(number))
                    phonebook_id = save_to_database.create_phonebook(conn, phonebook)

                    save = []
                    save.append(str(name))
                    save.append(phonebook_id)
                    self.listOfPeople.append(save)

            self.manager.get_screen('P').ids.PhoneBookNumbers.add_widget(
                TwoLineIconListItem(
                    IconLeftWidget(
                        icon="account"
                    ),
                    text = str(name) + ' ',
                    secondary_text = "Number: " + str(number),
                    on_release = self.PressedItem,
                    bg_color = (1,1,1,1),
                    radius = [10]
                    )
            )

            self.remove_widget(self.card)
            conn.close()
    
    def Cancel(self, obj):
        self.remove_widget(self.card)
            
    def PressedItem(self, obj):
        if PerfectStoreApp.delPerson:
            PerfectStoreApp.delPerson.bg_color = (1,1,1,1)
            if PerfectStoreApp.delPerson != obj:
                PerfectStoreApp.delPerson = obj
                PerfectStoreApp.delPerson.bg_color = "#00B4D8"
            else:
                PerfectStoreApp.delPerson = None
        else:
            PerfectStoreApp.delPerson = obj
            PerfectStoreApp.delPerson.bg_color = "#00B4D8"
            
    def deleteItem(self):

        if PerfectStoreApp.delPerson:
            priority = 0
            for i in self.listOfPeople:
                nameFromList = str(i[0].strip())
                nameFromItem = str(PerfectStoreApp.delPerson.text.strip())
                if nameFromItem == nameFromList:
                    priority = i[1]
                    break
            
            database = r"database.db"
            conn = save_to_database.create_connection(database)
            with conn:
                save_to_database.delete_phonebook(conn, priority)
            
            self.manager.get_screen('P').ids.PhoneBookNumbers.remove_widget(PerfectStoreApp.delPerson)
            PerfectStoreApp.delPerson = None
            conn.close()

##Settings##
class SettingsScreen(MDScreen):
            
    def ChangeText(self, theme):
            if theme == "DARK":
                self.manager.get_screen('S').ids.ThemeLabel.text = '[b][color=FFFFFF]THEME[/color][/b]'
                self.manager.get_screen('main').ids.mainTitle.text = '[b][color=FFFFFF][size=80]P[/size][size=75]erfect[/size][/color][i][color=0099FF][size=80]S[/size][size=75]tore[/size][/color][/i][/b]'
                self.manager.get_screen('main').ids.HelloText.text = '[b][color=FFFFFF]Hello\nWe are hoping that you have a great day[/color][/b]'
                self.manager.get_screen('main').ids.tasksLabel.text = '[b][color=FFFFFF]My Tasks:[/color][/b]'
                
            elif theme == "LIGHT":
                self.manager.get_screen('S').ids.ThemeLabel.text = '[b][color=000000]THEME[/color][/b]'
                self.manager.get_screen('main').ids.mainTitle.text = '[b][color=000000][size=80]P[/size][size=75]erfect[/size][/color][i][color=0099FF][size=80]S[/size][size=75]tore[/size][/color][/i][/b]'
                self.manager.get_screen('main').ids.HelloText.text = '[b][color=000000]Hello\nWe are hoping that you have a great day[/color][/b]'
                self.manager.get_screen('main').ids.tasksLabel.text = '[b][color=000000]My Tasks:[/color][/b]'

class MainScreen(MDScreen):
    def ChangeScreen(self, ScreenName):
        self.manager.current = ScreenName
                  
class PerfectStoreApp(MDApp):

    #database
    TasksList = []
    bills_database = []
    itemsFromDatabase = None

    #class objects
    obj_p = PhonebookScreen()
    delPerson = None
    
    #Screen properties
    Window.size = (475, 725)
    #Window.borderless = True
    sm = ScreenManager(transition = NoTransition())
    
    #Storing bill data
    string = ""
    Bill = []
    menuForDisplaying = None
    menuForDeleting = None
    
    #Data for creating a bill
    card = None
    textField_1 = None
    textField_2 = None
    textInput_3 = None
    
    #Amount sold screen data
    totalProfit = 0
    ListOfItems = []
    menuForItems = None
    InStorage = 100
    
    #Tasks Screen
    textField_1_task = None
    textInput_2_task = None
    card_task = None
    TaskItem = None
    listOfTasks = []
    listOfDeleteButtons = []
    listOfCheckButtons = []
    checkbutton = None
    deleteButton = None
    

    def build(self):
        self.theme_cls.theme_style = "Light"
        self.theme_cls.primary_palette = "Blue"
        
        self.sm.add_widget(MainScreen(name = 'main'))
        self.sm.add_widget(MailScreen(name = 'M'))
        self.sm.add_widget(PhonebookScreen(name = 'P'))
        self.sm.add_widget(SettingsScreen(name = 'S'))
            
        return self.sm

    def callback(self, instance):
        self.sm.current = instance
    
    def DropDownMenuForDisplaying(self):
        
        if len(self.Bill) == 0:
             Snackbar(text="Bills to select: None", snackbar_x=10, snackbar_y=10, size_hint_y=.08,
                     size_hint_x=(Window.width - (10 * 2)) / Window.width, bg_color=(0, 153/250, 1, 255/250)).open()
        else:
            bill_items = [
                {
                    "text": str(i['Name']),
                    "viewclass": "OneLineListItem",
                    "on_release": lambda x=str(i['Name']): self.LoadBill(x),
                }for i in self.Bill
            ]

            self.menuForDisplaying = MDDropdownMenu(
                caller = self.sm.get_screen('main').ids.SelectItem,
                items = bill_items,
                width_mult = 2,
                max_height = 300,
            )

            self.menuForDisplaying.open()
    
    def DropDownMenuForDeleting(self):
        
        if len(self.Bill) == 0:
             Snackbar(text="Bills to delete: None", snackbar_x=10, snackbar_y=10, size_hint_y=.08,
                     size_hint_x=(Window.width - (10 * 2)) / Window.width, bg_color=(0, 153/250, 1, 255/250)).open()
        else:
            bill_items = [
                {
                    "text": str(i['Name']),
                    "viewclass": "OneLineListItem",
                    "on_release": lambda x=str(i['Name']): self.DeleteBills(x),
                }for i in self.Bill
            ]

            self.menuForDeleting = MDDropdownMenu(
                caller = self.sm.get_screen('main').ids.DeleteItem,
                items = bill_items,
                width_mult = 2,
                max_height = 300,
            )

            self.menuForDeleting.open()
    
    def ChangeTheme(self, theme):
            if theme == "DARK":
                self.theme_cls.theme_style = "Dark"
                self.theme_cls.primary_palette = "Blue"

            elif theme == "LIGHT":
                self.theme_cls.theme_style = "Light"
                self.theme_cls.primary_palette = "Blue"
        
    def CreateBillPopUp(self):
        
        self.textField_1 = MDTextField(
            hint_text = "Bill Name:",
            helper_text = "Max. Num. of characters is 12",
            helper_text_mode = "persistent",
            font_size = 25,
            size_hint_x = .8,
            pos_hint = {'center_x': .5,'center_y': .9},
        )
        
        self.textField_2 = MDTextField(
            hint_text = "Date:",
            helper_text = "YYYY-MM-DD",
            helper_text_mode = "persistent",
            font_size = 25,
            size_hint_x = .8,
            pos_hint = {'center_x': .5,'center_y': .72},
        )
        
        self.textInput_3 = TextInput(
            hint_text = "Items",
            font_size = 30,
            size_hint = (.8, .5),
            pos_hint = {'center_x': .5,'center_y': .35},
            multiline = True,
            background_color = (0,0,0,0),
        )
        
        self.card = MDCard(
            MDFloatLayout(
                self.textField_1,
                self.textField_2,
                self.textInput_3,
                MDFlatButton(
                    text = "OK",
                    size_hint = (.2, .2),
                    pos_hint = {'center_x': 0.85,'center_y': 0.15},
                    on_release = self.AddBill,
                ),
                MDFlatButton(
                    text = "CANCEL",
                    size_hint = (.2, .2),
                    pos_hint = {'center_x': 0.6,'center_y': 0.15},
                    on_release = self.Cancel,
                )
            ),
            orientation = 'vertical',
            size_hint = (.8, .4),
            pos_hint = {'center_x': 0.5,'center_y': 0.5},
            elevation = 4,
            radius = [20],
        )
        self.sm.get_screen('main').add_widget(self.card)
    
    def checkDate(self, date, lastDate):
        if int(date[0]) <= int(lastDate[0]):
            if int(date[1]) <= int(lastDate[1]):
                if int(date[2]) <= int(lastDate[2]):
                    return True
                else:
                    return False
            else:
                return False   
        else:
            return False

    def checkStorage(self, ID, amount):

        database = r"database.db"
        conn = items_database.create_connection(database)
        InfoFromStorage = 0
        amountToInt = int(amount)

        with conn:
            InfoFromStorage = items_database.select_item_amount_by_id(conn, ID)

        newAmount = InfoFromStorage - amountToInt
        if newAmount < 0:

            conn.close()
            return False
        else: 

            with conn:
                items_database.update_amount(conn, (newAmount,ID))

            conn.close()
            return True


    def AddBill(self, obj):
        
        count = 1
        state = True
        PastDate = False
        billNum = 0
        lastBillNum = -1
        date = ["","",""]
        lastDate = ["","",""]
        index = 0
        itemName = ""
        itemPrice = ""
        listOfItemNames = []
        listOfItemPrices = []
        itemsExists = True
        IsInStorage = True

        for i in self.textInput_3.text:
            if i != " " and i != "\n":
                if i.isdigit() == False:
                    if i != ".":
                        itemName += i
                    else:
                        itemPrice += i
                else:
                    itemPrice += i
            else:
                count += 1
                if itemName != "":
                    listOfItemNames.append(itemName)
                    itemName = ""

                if itemPrice != "":
                    listOfItemPrices.append(itemPrice)
                    itemPrice = ""

        if itemPrice != []:
            listOfItemPrices.append(itemPrice)

        if (count%3) == 0:

            listOfItemNames.sort()
            price = []
            amount = []
            priceIndex = 0

            for i in range(0,len(listOfItemPrices)):
                if (i%2) != 0:
                    price.append(listOfItemPrices[i])
                else:
                    amount.append(listOfItemPrices[i])

            for i in self.itemsFromDatabase:
                if i[1] == listOfItemNames[index]:

                    if i[2] == price[index]:
                        itemsExists = True

                    IsInStorage = self.checkStorage(i[0], amount[index])

                    index += 1

                    if index == len(listOfItemNames):
                        break
                else:
                    itemsExists = False

            listOfItemNames.clear()
            listOfItemPrices.clear()
            price.clear()

        index = 0
                    
        for i in self.textField_2.text:
            if i.isdigit() == False:
                if i != '-' and i != '\n':
                    state = False
                index += 1
            else:
                date[index] += i

        if self.Bill != []:

            index = 0

            for i in self.textField_1.text:
                if i.isdigit():
                    billNum = int(i)

            for i in self.Bill[-1]['Name']:
                if i.isdigit():
                    lastBillNum = int(i)

            for i in self.Bill[-1]['Date']:
                if i.isdigit() == False:
                    index += 1
                else:
                    lastDate[index] += i

            PastDate = self.checkDate(date,lastDate)

        if len(self.textField_1.text) == 0 or len(self.textField_2.text) == 0 or len(self.textInput_3.text) == 0:
            Snackbar(text="Please fill in every text field!", snackbar_x=10, snackbar_y=10, size_hint_y=.08,
                     size_hint_x=(Window.width - (10 * 2)) / Window.width, bg_color=(0, 153/250, 1, 255/250)).open()
        elif billNum <= lastBillNum:
            Snackbar(text="Bill number ID has to be bigger!", snackbar_x=10, snackbar_y=10, size_hint_y=.08,
                    size_hint_x=(Window.width - (10 * 2)) / Window.width, bg_color=(0, 153/250, 1, 255/250)).open()
        elif state == False:
            Snackbar(text="Incorrect date format!", snackbar_x=10, snackbar_y=10, size_hint_y=.08,
                     size_hint_x=(Window.width - (10 * 2)) / Window.width, bg_color=(0, 153/250, 1, 255/250)).open()
        elif PastDate == True:
            Snackbar(text="The entered date is before the previous bill date!", snackbar_x=10, snackbar_y=10, size_hint_y=.08,
                    size_hint_x=(Window.width - (10 * 2)) / Window.width, bg_color=(0, 153/250, 1, 255/250)).open()
        elif len(self.textField_1.text) > 12:
            Snackbar(text="Name of the bill exceeded 12 characters!", snackbar_x=10, snackbar_y=10, size_hint_y=.08,
                     size_hint_x=(Window.width - (10 * 2)) / Window.width, bg_color=(0, 153/250, 1, 255/250)).open()
        elif itemsExists == False:
            Snackbar(text="The item or an items price doesn't exist in the database!", snackbar_x=10, snackbar_y=10, size_hint_y=.08,
                     size_hint_x=(Window.width - (10 * 2)) / Window.width, bg_color=(0, 153/250, 1, 255/250)).open()
        elif (count%3) != 0:
            Snackbar(text="Missing item information!", snackbar_x=10, snackbar_y=10, size_hint_y=.08,
                     size_hint_x=(Window.width - (10 * 2)) / Window.width, bg_color=(0, 153/250, 1, 255/250)).open()
        elif IsInStorage == False:
            Snackbar(text="Items on the bill are NOT in stock!", snackbar_x=10, snackbar_y=10, size_hint_y=.08,
                     size_hint_x=(Window.width - (10 * 2)) / Window.width, bg_color=(0, 153/250, 1, 255/250)).open()
        else:
            items = []
            string_list = []
            string = ""
            dic = {'Name' : "", 'Date' : "", 'Items' : []}

            dic['Name'] = str(self.textField_1.text)
            dic['Date'] = str(self.textField_2.text + "\n")

            database = r"database.db"
            conn = save_to_database.create_connection(database)

            string = ""
            item = ""
            listOfItemInfo = []
            for i in self.textInput_3.text.splitlines():
                items.append(str(i)+"\n")
                item = items[-1:][0]
                for x in item:

                    if x != " " and x != "\n":
                        string += x
                    else:
                        listOfItemInfo.append(string)
                        string = ""
                with conn:
                    bill = (self.textField_1.text, self.textField_2.text, str(listOfItemInfo[0]), str(listOfItemInfo[1]), str(listOfItemInfo[2]))
                    bill_id = save_to_database.create_bills(conn, bill)
                    
                listOfItemInfo.clear()
            dic['Items'] = items
            self.Bill.append(dic)

            for x in items:
                for y in x:
                    if y != ' ' and y != '\n':
                        string += y
                    else:
                        string_list.append(string)
                        string = ""

            self.TotalAmount(string_list)

            self.totalProfit = round(self.totalProfit,2)
            self.sm.get_screen('main').ids.TotalProfit.text = f"TOTAL PROFIT: {self.totalProfit}EU"

            with conn:
                bills = save_to_database.selec_all_bills(conn)

            if self.bills_database != []:
                ID_list = []
                bill_database_len = 0
                for i in bills:
                    ID_list.append(i[0])
    
                for i in ID_list:
                    if i > len(self.bills_database):
                        database_dict = {'ID':0, 'Name':""}
                        database_dict['ID'] = i
                        database_dict['Name'] = self.textField_1.text
                        self.bills_database.append(database_dict)

            else:
                for i in bills:
                    database_dict = {'ID':0, 'Name':""}
                    database_dict['ID'] = int(i[0])
                    database_dict['Name'] = i[1]
                    self.bills_database.append(database_dict)

            self.sm.get_screen('main').remove_widget(self.card)
            conn.close()

    def LoadBill(self, item):

        for i in self.Bill:
            if i['Name'] == item:
                self.string = f"{str(i['Name'])}\n{str(i['Date'])}{''.join(i['Items'])}\n"
        self.sm.get_screen('main').ids.BillContent.text = f'[b]{self.string}[/b]'
        self.string = ""

    def LoadBills(self):

        if self.Bill == []:
            self.string = "Missing Bills"
            self.sm.get_screen('main').ids.BillContent.text = f'[b]{self.string}[/b]'
            self.string = ""
        else:
            for i in self.Bill:
                self.string += f"{str(i['Name'])}\n{str(i['Date'])}{''.join(i['Items'])}\n"
            self.sm.get_screen('main').ids.BillContent.text = f'[b]{self.string}[/b]'
            self.string = ""

    def DeleteBills(self, item):
        
        string_list = []
        string_list_2 = []
        string = ""
        numbers = ""
        bill_database_copy = []
        id_list = []

        for i in self.bills_database:
            print(i)

        for i in self.bills_database:
            if i['Name'] == item:
                id_list.append(i['ID'])
            else:
                bill_database_copy.append(i)

        self.bills_database.clear()
        self.bills_database = bill_database_copy
        id_list = list(dict.fromkeys(id_list))

        print(id_list)
        for i in self.bills_database:
            print(i)
        print("\n")

        for i in self.Bill:
            if i['Name'] == item:
                for x in i['Items']:
                    for y in x:
                        if ord(y) >= 65 and ord(y) <= 90:
                            string+=y
                        elif ord(y) >= 97 and ord(y) <= 122:
                            string+=y
                        else:
                            if y != ' ' and y != '\n':
                                numbers+=y
                            elif numbers != '':
                                string_list_2.append(numbers)
                                numbers = ""

                    string_list.append(string)
                    string = ""

                string_list = list(dict.fromkeys(string_list))

                database = r"database.db"
                conn = save_to_database.create_connection(database)
                for x in id_list:
                    with conn:
                        save_to_database.delete_bills(conn, x)
                    
                self.Bill.remove(i)
                for i in string_list:
                    for y in self.ListOfItems:
                        if i == y:
                            self.ListOfItems.remove(y)
                            break

        subtract_number = 0

        if len(string_list_2) > 2:

            current_index = 0
            for i in range(0,len(string_list_2)-2):
                current_index += i + 1
                subtract_number += float(string_list_2[current_index-1]) * float(string_list_2[current_index])
        else:
            subtract_number = float(string_list_2[0]) * float(string_list_2[1]) 

        self.totalProfit -= round(subtract_number,2)
        self.sm.get_screen('main').ids.TotalProfit.text = f"TOTAL PROFIT: {str(self.totalProfit)}EU"
        self.menuForDeleting.dismiss()

        conn.close()

    def Cancel(self, obj):
        if self.card:
            self.sm.get_screen('main').remove_widget(self.card)
            self.card = None
        
        if self.card_task:
            self.sm.get_screen('main').remove_widget(self.card_task)
            self.card_task = None
              
    def DisplayItem(self):
        
        if len(self.ListOfItems) == 0:
             Snackbar(text="Items: None", snackbar_x=10, snackbar_y=10, size_hint_y=.08,
                     size_hint_x=(Window.width - (10 * 2)) / Window.width, bg_color=(0, 153/250, 1, 255/250)).open()
        else:
            items_ = [
                {
                    "text": str(i),
                    "viewclass": "OneLineListItem",
                    "on_release": lambda x=str(i): self.ShowItem(x),
                }for i in self.ListOfItems
            ]
            self.menuForItems = MDDropdownMenu(
                caller = self.sm.get_screen('main').ids.SelectItem,
                items = items_,
                width_mult = 2,
                border_margin = 24,
                max_height = 350,
                ver_growth = "down",
            )

            self.menuForItems.open()
            
    def ShowItem(self, instance):
        
        total_amount = 0
        Stock = 0
        items = []
        price = 0

        database = r"database.db"
        conn = items_database.create_connection(database)

        with conn:
            storage = items_database.select_all_from_storage(conn)
            items = items_database.select_items(conn)


        for i in storage:
            if i[1] == instance:
                total_amount = 100 - i[2]
                Stock = i[2]
                break

        for i in items:
            if i[1] == instance:
                price = i[2]
                break
        
        self.sm.get_screen('main').ids.item.text = f"Item: {instance}"
        self.sm.get_screen('main').ids.amount.text = f"Amount Sold: {str(total_amount)}"
        self.sm.get_screen('main').ids.price.text = f"Price: {str(price)}EU"
        self.sm.get_screen('main').ids.storage.text = f"In Storage: {str(Stock)}"
        self.menuForItems.dismiss()

        conn.close()
    
    def AddSwiperItem(self):
        
        self.textField_1_task = MDTextField(
            hint_text = "Task Name",
            helper_text = "Max. Num. of characters is 16",
            helper_text_mode = "persistent",
            font_size = 25,
            size_hint_x = .8,
            pos_hint = {'center_x': .5,'center_y': .85},
        )
        
        self.textInput_2_task = TextInput(
            hint_text = "Description\nMaximum number of characters is 60",
            font_size = 35,
            hint_text_color = (0, 153/250, 1, 135/250),
            size_hint = (.8, .5),
            pos_hint = {'center_x': .5,'center_y': .45},
            multiline = True,
            background_color = (0,0,0,0),
        )
        
        self.card_task = MDCard(
            MDFloatLayout(
                self.textField_1_task,
                self.textInput_2_task,
                MDFlatButton(
                    text = "OK",
                    size_hint = (.2, .2),
                    pos_hint = {'center_x': 0.85,'center_y': 0.15},
                    on_release = self.addTask
                ),
                MDFlatButton(
                    text = "CANCEL",
                    size_hint = (.2, .2),
                    pos_hint = {'center_x': 0.6,'center_y': 0.15},
                    on_release = self.Cancel
                )
            ),
            orientation = 'vertical',
            size_hint = (.8, .4),
            pos_hint = {'center_x': 0.5,'center_y': 0.5},
            elevation = 4,
            radius = [20],
        )
        
        self.sm.get_screen('main').add_widget(self.card_task)
    
    def addTask(self, obj):
        
        if self.card_task:
            if len(self.textField_1_task.text) > 16:
                Snackbar(text="Name of the task exceeded 12 characters!", snackbar_x=10, snackbar_y=10, size_hint_y=.08,
                         size_hint_x=(Window.width - (10 * 2)) / Window.width, bg_color=(0, 153/250, 1, 255/250)).open()
            elif len(self.textInput_2_task.text) > 60:
                Snackbar(text="Description of the task exceeded 12 characters!", snackbar_x=10, snackbar_y=10, size_hint_y=.08,
                         size_hint_x=(Window.width - (10 * 2)) / Window.width, bg_color=(0, 153/250, 1, 255/250)).open()
            elif len(self.textField_1_task.text) == 0 or len(self.textInput_2_task.text) == 0:
                Snackbar(text="Please fill in every text field!", snackbar_x=10, snackbar_y=10, size_hint_y=.08,
                         size_hint_x=(Window.width - (10 * 2)) / Window.width, bg_color=(0, 153/250, 1, 255/250)).open()
            else:
                self.creatingASwiperItem(self.textField_1_task.text, self.textInput_2_task.text, 0)
                self.sm.get_screen('main').remove_widget(self.card_task)
                self.card_task = None

                name = self.textField_1_task.text
                description = self.textInput_2_task.text

                database = r"database.db"
                conn = save_to_database.create_connection(database)
                with conn:
                    tasks = (name,description,0)
                    tasks_id = save_to_database.create_task(conn,tasks)
                    self.TasksList.append(tasks_id)

                conn.close()
        
    def CheckTask(self, instance):
        
        if instance.md_bg_color == [0.5019607843137255, 0.5019607843137255, 0.5019607843137255, 1.0]:
            instance.md_bg_color = "#72CC50"

            for i in range(0,len(self.listOfCheckButtons)):
                if instance == self.listOfCheckButtons[i]:

                    ID = self.TasksList[i]
                    database = r"database.db"
                    conn = save_to_database.create_connection(database)

                    with conn:
                        save_to_database.set_state(conn, (1,ID))

                    conn.close()
        else:
            instance.md_bg_color = "gray"

            for i in range(0,len(self.listOfCheckButtons)):
                if instance == self.listOfCheckButtons[i]:

                    ID = self.TasksList[i]
                    database = r"database.db"
                    conn = save_to_database.create_connection(database)

                    with conn:
                        save_to_database.set_state(conn, (0,ID))

                    conn.close()
                     
    def removeTask(self, instance):
        
        ID = 0
        for i in range(len(self.listOfDeleteButtons)):
            if self.listOfDeleteButtons[i] is instance:
                self.sm.get_screen('main').ids.TaskSwiper.remove_widget(self.listOfTasks[i])
                self.listOfTasks.remove(self.listOfTasks[i])
                self.listOfDeleteButtons.remove(self.listOfDeleteButtons[i])
                
                ID = self.TasksList[i]
                database = r"database.db"
                conn = save_to_database.create_connection(database)
                with conn:
                    save_to_database.delete_task(conn, ID)
                self.TasksList.remove(self.TasksList[i])

                conn.close()
                break
                
    def on_start(self):
        
        database = r"database.db"
        conn = save_to_database.create_connection(database)
        sql_task = """ CREATE TABLE IF NOT EXISTS tasks (
                        id integer PRIMARY KEY,
                        name text NOT NULL,
                        description text NOT NULL,
                        state integer NOT NULL
                    ); """
                    
        sql_phonebook = """ CREATE TABLE IF NOT EXISTS phonebook (
                            id integer PRIMARY KEY,
                            name text NOT NULL,
                            number text NOT NULL
                        ); """
                        
        sql_bills = """ CREATE TABLE IF NOT EXISTS bills(
                            id integer PRIMARY KEY,
                            name text NOT NULL,
                            date text NOT NULL,
                            item text NOT NULL,
                            amount text NOT NULL,
                            price text NOT NULL
                        ); """
        
        if conn != None:
            save_to_database.create_table(conn, sql_task)
            save_to_database.create_table(conn, sql_phonebook)
            save_to_database.create_table(conn, sql_bills)
        else:
            print("Error! No connection with database.")
            
        phonebookList = None
        taskList = None
        bills = None

        with conn:
            phonebookList = save_to_database.select_all_phonebook(conn)
            taskList = save_to_database.select_every_task(conn)
            bills = save_to_database.selec_all_bills(conn)
            self.itemsFromDatabase = items_database.select_items(conn)
            
        if len(phonebookList) != 0:
            for i in phonebookList:
                self.sm.get_screen('P').ids.PhoneBookNumbers.add_widget(
                    TwoLineIconListItem(
                        IconLeftWidget(
                            icon="account"
                        ),
                        text = str(i[1]).strip('\n'),
                        secondary_text = "Number: " + str(i[2]).strip('\n'),
                        on_release = self.obj_p.PressedItem,
                        bg_color = (1,1,1,1),
                        radius = [10]
                    )
                )
                save = []
                save.append(str(i[1]))
                save.append(i[0])
                PhonebookScreen.listOfPeople.append(save)
            
        if len(taskList) != 0:
            for i in taskList:
                self.creatingASwiperItem(i[1], i[2], i[3])
                self.TasksList.append(i[0])

        for i in bills:
            database_dict = {'ID':0, 'Name':""}
            database_dict['ID'] = int(i[0])
            database_dict['Name'] = i[1]
            self.bills_database.append(database_dict)

        if len(bills) != 0:

            listOfBillNames = []
            items = []
            index = 0

            for i in bills:
                listOfBillNames.append(i[1])
            listOfBillNames = list(dict.fromkeys(listOfBillNames))

            for i in listOfBillNames:
                dic = {'Name': "", 'Date': "", 'Items': []}
                while i == bills[index][1]:
                    items.append(f'{str(bills[index][3])} {str(bills[index][4])} {str(bills[index][5])}\n')
                    index += 1
                    if index == len(bills):
                        break
                dic['Name'] = bills[index-1][1]
                dic['Date'] = f'{bills[index-1][2]}\n'
                dic['Items'] = items
                self.Bill.append(dic)
                items = []

        string = ""
        string_list = []
        for i in self.Bill:
            for x in i['Items']:
                for y in x:
                    if y != ' ' and y != '\n':
                        string += y
                    else:
                        string_list.append(string)
                        string = ""

        self.TotalAmount(string_list)
        
        self.totalProfit = round(self.totalProfit,2)
        self.sm.get_screen('main').ids.TotalProfit.text = f"TOTAL PROFIT: {str(self.totalProfit)}EU"

        storage = []
        with conn:
            storage = items_database.select_all_from_storage(conn)

        index = 0
        for i in storage:
            self.sm.get_screen('main').ids.itemsTableLayout.add_widget(
                MDBoxLayout(
                    MDLabel(
                        text = f'{i[1]}'
                        ),
                    MDLabel(
                        text = f'{self.itemsFromDatabase[index][2]}EU'
                        ),
                    MDLabel(
                        text = f'{i[2]}'
                        ),
                    
                    padding = 10,
                    spacing = 25
                    )
                )
            index += 1

        conn.close()
                
    def on_stop(self):
        
        #database
        self.bills_database.clear()
        del self.itemsFromDatabase    
        
        #Storing bill data
        self.Bill.clear()
        
        #Amount sold screen data
        self.ListOfItems.clear()
        
        #Tasks Screen
        self.TasksList.clear()
        self.listOfTasks.clear()
        self.listOfDeleteButtons.clear()
        self.listOfCheckButtons.clear()

    def TotalAmount(self, string_list):
        
        temp_list = []
        
        for i in string_list:
           test = str(i)
           res = test.replace('.','',1).isdigit()
           if res:
               if test.isdigit():
                   amount = int(test)
               if not test.isdigit():
                   self.totalProfit += float(test) * amount
           elif not res:
               temp_list.append(test)
            
        if self.ListOfItems is []:
            self.ListOfItems = list(set(temp_list))
            self.ListOfItems.sort()
        else:
            temp_list += self.ListOfItems
            self.ListOfItems = list(set(temp_list))
            self.ListOfItems.sort()
            
    def creatingASwiperItem(self, task, description, state):

        checkButtonColor = ""

        if state == 1:
            checkButtonColor = "#72CC50"
        elif state == 0:
            checkButtonColor = "gray"
        else:
            raise Exception("Memory Error!! Wrong data stored in database")


        self.checkbutton = MDFloatingActionButton(
                           icon = 'check-bold',
                           pos_hint = {'center_x': 0.55,'center_y': 0.2},
                           md_bg_color = checkButtonColor,
                           elevation = 0,
                           on_release = self.CheckTask
                        )
        self.deleteButton = MDFloatingActionButton(
                       icon = 'delete',
                       pos_hint = {'center_x': 0.82,'center_y': 0.2},
                       md_bg_color = "red",
                       elevation = 0,
                       on_release = self.removeTask
                    )
        self.TaskItem = MDSwiperItem(
               MDFloatLayout(
                   self.checkbutton,
                   self.deleteButton,
                   MDCard(
                       MDLabel(
                           markup = True,
                           text = f'[b]{task}[/b]',
                           font_size = 55,
                           halign = 'center'
                       ),
                       orientation = 'vertical',
                       elevation = 2,
                       md_bg_color = (1,1,1,1),
                       size_hint = (0.9, 0.1),
                       pos_hint = {'center_x': 0.5,'center_y': 0.9}
                   ),
                   MDCard(
                       MDFloatLayout(
                           MDLabel(
                               markup = True,
                               text = f'[b]{description}[/b]',
                               pos_hint = {'center_x': 0.5,'center_y': 0.9},
                               font_size = 45
                           )
                       ),
                       orientation = 'vertical',
                       elevation = 2,
                       md_bg_color = (1,1,1,1),
                       size_hint = (.9, .4),
                       pos_hint = {'center_x': 0.5,'center_y': 0.6},
                       padding = 20,
                       spacing = 10
                   )
               ),
               radius = [15,],
               md_bg_color = (0, 153/250, 1, 255/250)
            )
        self.listOfTasks.append(self.TaskItem)
        self.listOfDeleteButtons.append(self.deleteButton)
        self.listOfCheckButtons.append(self.checkbutton)
        self.sm.get_screen('main').ids.TaskSwiper.add_widget(self.TaskItem)
        
if __name__ == '__main__':
    PerfectStoreApp().run()