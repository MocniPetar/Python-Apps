import kivy
kivy.require("2.1.0")

from kivymd.app import MDApp
from kivy.utils import platform
from kivy.uix.screenmanager import ScreenManager, NoTransition
from kivymd.uix.screen import MDScreen
from kivy.core.window import Window
from kivymd.uix.list import TwoLineIconListItem, IconLeftWidget
from kivymd.uix.card import MDCard
from kivymd.uix.button import MDFlatButton, MDIconButton, MDRaisedButton
from kivymd.uix.textfield import MDTextField, MDTextFieldRect
from kivymd.uix.floatlayout import MDFloatLayout
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.menu import MDDropdownMenu
from kivy.uix.textinput import TextInput
from kivymd.uix.swiper import MDSwiperItem
from kivymd.uix.label import MDLabel
from kivymd.uix.snackbar import Snackbar
from database import save_to_database
from ItemsDatabase import items_database
from kivymd.uix.scrollview import MDScrollView
from kivymd.uix.list import MDList
from kivy.graphics import *

##Mail##
class MailScreen(MDScreen):
    pass

##Phonebook##
class PhonebookScreen(MDScreen):
    
    card = None
    textField_1 = None
    textField_2 = None
    listOfPeople = []
    FadeCardForPhoneBookClass = None
        
    def add_card(self):

        self.FadeCardForPhoneBookClass = FadeCard()

        self.manager.get_screen('P').add_widget(self.FadeCardForPhoneBookClass)
        self.manager.get_screen('P').ids.PhoneBookScrollView.disabled = True
        self.manager.get_screen('P').ids.AddPersonButton.disabled = True
        self.manager.get_screen('P').ids.DeletePersonButton.disabled = True
        self.manager.get_screen('P').ids.BackButton.disabled = True
        

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
            size_hint = (.7, .3),
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
            self.manager.get_screen('P').remove_widget(self.FadeCardForPhoneBookClass)
            self.FadeCardForPhoneBookClass = None
            self.manager.get_screen('P').ids.PhoneBookScrollView.disabled = False
            self.manager.get_screen('P').ids.AddPersonButton.disabled = False
            self.manager.get_screen('P').ids.DeletePersonButton.disabled = False
            self.manager.get_screen('P').ids.BackButton.disabled = False
            conn.close()
    
    def Cancel(self, obj):
        self.manager.get_screen('P').remove_widget(self.FadeCardForPhoneBookClass)
        self.FadeCardForPhoneBookClass = None
        self.manager.get_screen('P').ids.PhoneBookScrollView.disabled = False
        self.manager.get_screen('P').ids.AddPersonButton.disabled = False
        self.manager.get_screen('P').ids.DeletePersonButton.disabled = False
        self.manager.get_screen('P').ids.BackButton.disabled = False
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
                self.manager.get_screen('main').ids.HelloText.text = '[b][size=35][color=0099FF]Hello[/color][color=FFFFFF]\nWe are hoping that you[/color] [color=0099FF]have a great day[/color][/size][/b]'
                self.manager.get_screen('main').ids.tasksLabel.text = '[b][color=FFFFFF]My Tasks:[/color][/b]'
                
            elif theme == "LIGHT":
                self.manager.get_screen('S').ids.ThemeLabel.text = '[b][color=000000]THEME[/color][/b]'
                self.manager.get_screen('main').ids.mainTitle.text = '[b][color=000000][size=80]P[/size][size=75]erfect[/size][/color][i][color=0099FF][size=80]S[/size][size=75]tore[/size][/color][/i][/b]'
                self.manager.get_screen('main').ids.HelloText.text = '[b][size=35][color=0099FF]Hello[/color][color=000000]\nWe are hoping that you[/color] [color=0099FF]have a great day[/color][/size][/b]'
                self.manager.get_screen('main').ids.tasksLabel.text = '[b][color=000000]My Tasks:[/color][/b]'

class MainScreen(MDScreen):
    pass

class FadeCard(MDBoxLayout):
    def __init__(self, **kwargs):
        super(FadeCard, self).__init__(**kwargs)

class BillItem(MDBoxLayout):
    def __init__(self, *args, **kwargs):
        super(BillItem, self).__init__(*args, **kwargs)
                  
class PerfectStoreApp(MDApp):

    #database
    TasksList = []
    bills_database = []
    itemsFromDatabase = None

    #class objects
    obj_p = PhonebookScreen()
    obj_m = MainScreen()
    delPerson = None
    
    #Screen properties
    sm = ScreenManager(transition = NoTransition())
    
    #Storing bill data
    string = ""
    Bill = []
    menuForDisplaying = None
    menuForDeleting = None
    
    #Data for creating a bill
    card = None
    textField_1 = None
    yearTextField = None
    monthTextField = None
    dayTextField = None
    itemAmountTextField = None
    billListWidget = None
    BillItemList = []
    listOfItemsOnBill = None
    layoutOfCard = None
    
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

    #NewsInfo
    infoCard = None
    FadeCardInstance = None

    def build(self):

        if(platform == 'android' or platform == 'ios'):
            Window.maximize()
        else:
            Window.size = (620, 1024)

        self.theme_cls.theme_style = "Light"
        self.theme_cls.primary_palette = "Blue"
        
        self.sm.add_widget(MainScreen(name = 'main'))
        self.sm.add_widget(MailScreen(name = 'M'))
        self.sm.add_widget(PhonebookScreen(name = 'P'))
        self.sm.add_widget(SettingsScreen(name = 'S'))
            
        return self.sm
    
    def NewsInfo(self, topic):

        if self.infoCard == None:

            self.sm.get_screen('main').add_widget(self.FadeCardInstance)

            self.sm.get_screen('main').ids.PhoneBookButton.disabled = True
            self.sm.get_screen('main').ids.MailButton.disabled = True
            self.sm.get_screen('main').ids.SettingsButton.disabled = True
            self.sm.get_screen('main').ids.NewsScrollView.disabled = True

            InfoToShow = ""

            topics = [
                "Lemon",
                "Fanta",
                "Goods",
                "Banknotes",
                "Prices"
            ]

            topicInfo = [
                """Today, the prices of lemons have soared to new heights, leaving many consumers feeling the pinch. According to local vendors, the sudden surge in prices is due to a shortage of lemons caused by unfavorable weather conditions in the regions where they are cultivated.\n\nMany shoppers were caught off guard by the sudden price increase, with some expressing frustration at having to pay exorbitant amounts for a single lemon.\n\nThe high prices have also affected local businesses, particularly those in the food and beverage industry that rely heavily on lemons for their products. Some restaurants have had to adjust their menus or switch to alternative ingredients to cope with the shortage and high prices.\n\nDespite the current situation, some experts predict that the lemon market will eventually stabilize as the weather conditions improve and the supply chain recovers. However, for now, consumers will have to make do with paying more for their lemons or finding substitutes for their favorite recipes.""",

                """Recent tests conducted by health authorities have revealed that larger amounts of ethylene oxide, a carcinogenic chemical, have been found in cans of Fanta sold in stores. The chemical is used in the production of plastic products and can pose a serious risk to human health if ingested in large amounts.\n\nFollowing the discovery, several countries have issued recalls of Fanta products and urged consumers to avoid consuming them until further notice. Coca-Cola, the company that produces Fanta, has also issued a statement acknowledging the issue and promising to take appropriate measures to address it.\n\nHealth officials are currently investigating the source of the contamination and working to determine how widespread the issue is. In the meantime, consumers are advised to be cautious and vigilant when purchasing soft drinks and to always check for any potential health risks or recalls before consuming them.""",

                """The government has announced a reduction in customs duties on goods imported from the United Kingdom, in a move aimed at boosting trade relations between the two countries. The decision comes following a series of negotiations between the governments of both nations, which have been working to establish more favorable trade terms in the wake of Brexit.\n\nUnder the new regulations, many goods previously subject to high tariffs will now be exempt or subject to lower duties, making them more accessible and affordable for consumers. This is expected to have a positive impact on a range of industries, from manufacturing and agriculture to retail and e-commerce.\n\nThe decision has been met with mixed reactions, with some experts praising it as a positive step towards strengthening economic ties between the UK and other countries, while others have expressed concerns about the potential impact on local industries and employment.\n\nDespite the differing opinions, the government has emphasized the need for continued collaboration and cooperation in order to achieve mutually beneficial outcomes for all parties involved. As such, officials have stated that they will remain open to further negotiations and discussions in the future in order to ensure a fair and equitable trade relationship between the UK and its international partners.""",

                """Several shops in the city have reported running out of euro banknotes due to an influx of careless customers who have been mishandling and damaging the currency. According to reports, many customers have been crumpling, tearing, or otherwise damaging the notes, making them unfit for circulation.\n\nThe shortage of banknotes has led to frustration among business owners, many of whom rely heavily on cash transactions. Some have reported having to turn away customers or resorting to alternative payment methods such as credit cards or mobile payments.\n\nTo address the issue, officials are urging customers to treat banknotes with care and to avoid any behavior that could damage them. They are also encouraging businesses to adopt alternative payment methods and to report any instances of damaged currency to the appropriate authorities.\n\nDespite these efforts, some experts warn that the issue may persist unless more comprehensive measures are put in place to safeguard the integrity of the currency. This may include improved education and awareness campaigns for the public, stricter penalties for currency mishandling, and more rigorous quality control standards for banknotes in circulation.""",

                """In an effort to curb inflation and ease the burden on consumers, the government has announced a ban on raising the prices of basic food staples such as bread, milk, and meat. The move comes amid rising food prices and concerns about food insecurity, particularly among low-income households.\n\nUnder the new regulations, retailers and producers are prohibited from increasing the prices of these essential food items, and must instead maintain their current prices or risk facing penalties. The ban is expected to remain in place for an indefinite period, or until the government determines that it is no longer necessary.\n\nThe decision has been met with mixed reactions, with some applauding the government's efforts to protect consumers and ensure access to affordable food, while others have expressed concerns about the potential impact on the food industry and supply chain.\n\nDespite these differing opinions, officials have emphasized the need for cooperation and collaboration between all stakeholders to ensure the continued availability and affordability of essential food items. As such, they have pledged to work closely with retailers, producers, and other stakeholders to monitor the situation and address any issues that may arise."""
            ]

            for i in range(0,len(topics)):
                if topics[i] == topic:
                    InfoToShow = topicInfo[i]

            def cardPopUp(heightOfBoxLayout,y,x):

                self.infoCard = MDCard (
                    MDFloatLayout(
                        MDScrollView(

                            MDBoxLayout(
                                MDLabel(
                                    markup = True,
                                    text = f'[b][size=20sp]{str(InfoToShow)}[/size][/b]',
                                    pos_hint = {'center_x': 0.5,'center_y': 0.5}
                                ),
                                orientation = 'vertical',
                                size_hint_y = None,
                                height = heightOfBoxLayout,
                                padding = "20sp",
                                spacing = "20sp"
                            ),

                            do_scroll_x = False,
                            do_scroll_y = True,
                            size_hint_y = .8,
                            size_hint_x = .85,
                            #bar_color: 0, 153/250, 1, 255/250
                            #bar_inactive_color: 0, 153/250, 1, 255/250
                            pos_hint = {'center_x': 0.5,'center_y': 0.55}
                        ),

                       MDFlatButton(
                           text = "CLOSE",
                           size_hint = (".05sp", ".05sp"),
                           pos_hint = {'center_x': 0.85,'center_y': 0.1},
                           on_release = self.closeInfoCard,
                       ),
                    ),
                    orientation = 'vertical',
                    size_hint = (y, x),
                    pos_hint = {'center_x': 0.5,'center_y': 0.5},
                    elevation = 4,
                    radius = [20],
                    )
                self.sm.get_screen('main').add_widget(self.infoCard)       

            if(platform == 'android' or platform == 'ios'):

                if len(InfoToShow) <= 1100:
                    cardPopUp("1350sp", ".4sp", ".2sp")
                elif (len(InfoToShow) > 1100) and (len(InfoToShow) < 1300):
                    cardPopUp("1700sp", ".4sp", ".2sp")
                else:
                    cardPopUp("1850sp", ".4sp", ".2sp")

            else:
                
                if len(InfoToShow) <= 1100:
                    cardPopUp("1000sp", ".6sp", ".5sp")
                elif (len(InfoToShow) > 1100) and (len(InfoToShow) < 1300):
                    cardPopUp("1250sp", ".6sp", ".5sp")
                else:
                    cardPopUp("1300sp", ".6sp", ".5sp")

    def closeInfoCard(self, instance):
        self.sm.get_screen('main').remove_widget(self.infoCard)
        self.sm.get_screen('main').remove_widget(self.FadeCardInstance)
        self.sm.get_screen('main').ids.PhoneBookButton.disabled = False
        self.sm.get_screen('main').ids.MailButton.disabled = False
        self.sm.get_screen('main').ids.SettingsButton.disabled = False
        self.sm.get_screen('main').ids.NewsScrollView.disabled = False
        self.infoCard = None

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
                width_mult = 3,
                ver_growth = "up"
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
                width_mult = 3,
                ver_growth = "down"
            )

            self.menuForDeleting.open()
    
    def ChangeTheme(self, theme):
            if theme == "DARK":
                self.theme_cls.theme_style = "Dark"
                self.theme_cls.primary_palette = "Blue"

            elif theme == "LIGHT":
                self.theme_cls.theme_style = "Light"
                self.theme_cls.primary_palette = "Blue"
        
    def sizeOfList(self, instance):

            if self.itemAmountTextField.text != '':

                if self.itemAmountTextField.text.isdigit():

                    if self.listOfItemsOnBill != None:
                        if self.BillItemList != []:
                            for i in self.BillItemList:
                                self.listOfItemsOnBill.remove_widget(i)
                    
                        self.BillItemList = []

                    size = int(self.itemAmountTextField.text)
                    self.listOfItemsOnBill = MDList(
                        spacing = 60
                    )

                    if size > 0:

                        for i in range(0,size):
                            self.BillItemList.append(BillItem())

                        for i in self.BillItemList:
                            self.listOfItemsOnBill.add_widget(i)

                    self.billListWidget = MDScrollView(
                        self.listOfItemsOnBill,
                        do_scroll_x = False,
                        size_hint_y = None,
                        size_hint_x = None, # Sets the size hint of the x and y to None
                        height = 180,
                        width = 300,
                        pos_hint = {'center_x': .52, 'center_y': .3}
                    )

                    self.layoutOfCard.add_widget(self.billListWidget)

                else:
                    return
            else:
                return
        
    def CreateBillPopUp(self):
        
        self.textField_1 = MDTextField(
            hint_text = "Bill Name:",
            helper_text = "Max. Num. of characters is 12",
            helper_text_mode = "persistent",
            font_size = 20,
            size_hint_x = .8,
            pos_hint = {'center_x': .5,'center_y': .87}
        )

        self.yearTextField = MDTextFieldRect(
            hint_text = "YYYY",
            font_size = 20,
            size_hint_x = .17,
            size_hint_y = .1,
            pos_hint = {'center_x': .22, 'center_y': .67},
            halign = 'center',
            padding = [10,]
        )

        self.monthTextField = MDTextFieldRect(
            hint_text = "MM",
            font_size = 20,
            size_hint_x = .17,
            size_hint_y = .1,
            pos_hint = {'center_x': .5, 'center_y': .67},
            halign = 'center',
            padding = [10,]
        )
        
        self.dayTextField = MDTextFieldRect(
            hint_text = "DD",
            font_size = 20,
            size_hint_x = .17,
            size_hint_y = .1,
            pos_hint = {'center_x': .78, 'center_y': .67},
            halign = 'center',
            padding = [10,]
        )

        self.itemAmountTextField = MDTextFieldRect(
            hint_text = "XXX",
            font_size = 18,
            size_hint = (.18, .1),
            pos_hint = {'center_x': .51, 'center_y': .55},
            halign = 'center',
            padding = [10,]
        )

        self.layoutOfCard = MDFloatLayout(
            self.textField_1,
            self.yearTextField,
            self.monthTextField,
            self.dayTextField,
            self.itemAmountTextField,
            MDLabel(
                markup = True,
                text = "[b][color=000000]Num. of Items[/b]",
                font_style = 'Body2',
                pos_hint = {'center_x': .54,'center_y': .55},
            ),
            MDRaisedButton(
                markup = True,
                text = "[b][color=000000]Enter[/b]",
                size_hint = (None, None),
                height = 18,
                width = 8,
                pos_hint = {'center_x': .75,'center_y': .55},
                on_release = self.sizeOfList
            ),
            MDFlatButton(
                text = "OK",
                size_hint = (None, None),
                width = 100,
                height = 50,
                pos_hint = {'center_x': .85,'center_y': .1},
                on_release = self.AddBill,
            ),
            MDFlatButton(
                text = "CANCEL",
                size_hint = (None, None),
                width = 100,
                height = 50,
                pos_hint = {'center_x': .6,'center_y': .1},
                on_release = self.Cancel,
            )
        )

        # IMPLEMENT A WAY TO HAVE A LIST OF MDTextFieldRect's FOR ENTERING NAMES,AMOUNT AND PRICES OF ITEMS IN A LIST INSIDE A SCROLL VIEW
        # UPDATED: The MDTextFieldRect's are now interactible and in the desired size. The problem that the size of the MDScrollView or
        # MDBoxLayout is not correct. It doesn't work for now. Make it work!!

        self.card = MDCard(
            self.layoutOfCard,
            size_hint = (None, None),
            width = 525,
            height = 575,
            pos_hint = {'center_x': 0.5,'center_y': 0.5},
            elevation = 4,
            radius = [20]
        )

        self.sm.get_screen('main').add_widget(self.FadeCardInstance)
        self.sm.get_screen('main').ids.SelectItem.disabled = True
        self.sm.get_screen('main').ids.printAll.disabled = True
        self.sm.get_screen('main').ids.Clearcard.disabled = True
        self.sm.get_screen('main').ids.CreateBill.disabled = True
        self.sm.get_screen('main').ids.DeleteItem.disabled = True
        self.sm.get_screen('main').ids.BillScrollView.disabled = True
        self.sm.get_screen('main').add_widget(self.card)
    
    def checkDate(self, lastDate):

        # 0 -> the date si fine
        # 1 -> the date is older then the last
        # 2 -> the date is not entered correctly
    
        for i in self.yearTextField.text:
            if i.isdigit() == False:
                return 2
            
        for i in self.monthTextField.text:
            if i.isdigit() == False:
                return 2
            
        for i in self.dayTextField.text:
            if i.isdigit() == False:
                return 2
            
        if int(self.yearTextField.text) < int(lastDate[0]):
            return 1
        elif int(self.yearTextField.text) == int(lastDate[0]):
            if int(self.monthTextField.text) < int(lastDate[1]):
                return 1
            elif int(self.monthTextField.text) == int(lastDate[1]):
                if int(self.dayTextField.text) < int(lastDate[2]):
                    return 1
                else:
                    return 0
            else:
                return 0
        else:
            return 0
            
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

        DATE = True
        numOfMonthsAndDays = True
        ITEMS = True

        if len(self.yearTextField.text) == 0 or len(self.monthTextField.text) == 0 or len(self.dayTextField.text) == 0:
            DATE = False

        if int(self.monthTextField.text) > 12 or int(self.dayTextField.text) > 31:
            numOfMonthsAndDays = False

        for i in self.BillItemList:
            if i.ids.ItemField.text == '' or i.ids.AmountField.text == '' or i.ids.PriceField.text == '':
                ITEMS = False

        if len(self.textField_1.text) == 0 or ITEMS == False or DATE == False:
            Snackbar(text="Please fill in every text field!", snackbar_x=10, snackbar_y=10, size_hint_y=.08,
                     size_hint_x=(Window.width - (10 * 2)) / Window.width, bg_color=(0, 153/250, 1, 255/250)).open()
            
        elif numOfMonthsAndDays == False:
            Snackbar(text="Month > 12 or Day > 31!", snackbar_x=10, snackbar_y=10, size_hint_y=.08,
                     size_hint_x=(Window.width - (10 * 2)) / Window.width, bg_color=(0, 153/250, 1, 255/250)).open()
            
        else:
            PastDate = 0
            billNum = 0
            lastBillNum = -1
            lastDate = ["","",""]
            index = 0
            itemsExists = True
            IsInStorage = True

            for i in self.itemsFromDatabase:

                #   i[1] --> Name of item
                #   i[2] --> Price of item

                if self.BillItemList[index].ids.ItemField.text == i[1] and self.BillItemList[index].ids.PriceField.text == i[2]:
                    
                    IsInStorage = self.checkStorage(i[0], self.BillItemList[index].ids.AmountField.text)

                    itemsExists = True
                    index += 1

                else:
                    itemsExists = False
                
                if index >= len(self.BillItemList):
                    break

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

                PastDate = self.checkDate(lastDate)

            if billNum <= lastBillNum:
                Snackbar(text="Bill number ID has to be bigger!", snackbar_x=10, snackbar_y=10, size_hint_y=.08,
                        size_hint_x=(Window.width - (10 * 2)) / Window.width, bg_color=(0, 153/250, 1, 255/250)).open()
                
            elif PastDate == 1:
                Snackbar(text="The entered date is before the previous bill date!", snackbar_x=10, snackbar_y=10, size_hint_y=.08,
                        size_hint_x=(Window.width - (10 * 2)) / Window.width, bg_color=(0, 153/250, 1, 255/250)).open()
                
            elif PastDate == 2:
                Snackbar(text="The entered date is not typed correctly!", snackbar_x=10, snackbar_y=10, size_hint_y=.08,
                        size_hint_x=(Window.width - (10 * 2)) / Window.width, bg_color=(0, 153/250, 1, 255/250)).open()
                
            elif len(self.textField_1.text) > 12:
                Snackbar(text="Name of the bill exceeded 12 characters!", snackbar_x=10, snackbar_y=10, size_hint_y=.08,
                         size_hint_x=(Window.width - (10 * 2)) / Window.width, bg_color=(0, 153/250, 1, 255/250)).open()

            elif itemsExists == False:
                Snackbar(text="The item or an items price doesn't exist in the database!", snackbar_x=10, snackbar_y=10, size_hint_y=.08,
                         size_hint_x=(Window.width - (10 * 2)) / Window.width, bg_color=(0, 153/250, 1, 255/250)).open()
                
            elif IsInStorage == False:
                Snackbar(text="Items on the bill are NOT in stock!", snackbar_x=10, snackbar_y=10, size_hint_y=.08,
                         size_hint_x=(Window.width - (10 * 2)) / Window.width, bg_color=(0, 153/250, 1, 255/250)).open()
                
            else:
                items = []
                string_list = []
                string = ""
                dic = {'Name' : "", 'Date' : "", 'Items' : []}
                dateString = str(self.yearTextField.text + "-" + self.monthTextField.text + "-" + self.dayTextField.text)

                dic['Name'] = str(self.textField_1.text)
                dic['Date'] = str(self.yearTextField.text + "-" + self.monthTextField.text + "-" + self.dayTextField.text + "\n")

                database = r"database.db"
                conn = save_to_database.create_connection(database)

                string = ""
                listOfItemInfo = []
                for i in self.BillItemList:
                    
                    listOfItemInfo.append(i.ids.ItemField.text)
                    listOfItemInfo.append(i.ids.AmountField.text)
                    listOfItemInfo.append(i.ids.PriceField.text)
                    
                    ItemInALine = i.ids.ItemField.text + " " + i.ids.AmountField.text + " " + i.ids.PriceField.text + "\n"

                    items.append(ItemInALine)

                    with conn:
                        bill = (self.textField_1.text, dateString, str(listOfItemInfo[0]), str(listOfItemInfo[1]), str(listOfItemInfo[2]))
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
                self.sm.get_screen('main').remove_widget(self.FadeCardInstance)
                self.sm.get_screen('main').ids.SelectItem.disabled = False
                self.sm.get_screen('main').ids.printAll.disabled = False
                self.sm.get_screen('main').ids.Clearcard.disabled = False
                self.sm.get_screen('main').ids.CreateBill.disabled = False
                self.sm.get_screen('main').ids.DeleteItem.disabled = False
                self.sm.get_screen('main').ids.BillScrollView.disabled = False
                conn.close()

    def LoadBill(self, item):

        for i in self.Bill:
            if i['Name'] == item:
                self.string = f"{str(i['Name'])}\n{str(i['Date'])}{''.join(i['Items'])}\n"
        self.sm.get_screen('main').ids.BillContent.text = f'[b]{self.string}[/b]'
        self.string = ""

        self.menuForDisplaying.dismiss()

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
            self.sm.get_screen('main').ids.SelectItem.disabled = False
            self.sm.get_screen('main').ids.printAll.disabled = False
            self.sm.get_screen('main').ids.Clearcard.disabled = False
            self.sm.get_screen('main').ids.CreateBill.disabled = False
            self.sm.get_screen('main').ids.DeleteItem.disabled = False
            self.sm.get_screen('main').ids.BillScrollView.disabled = False
            self.card = None
        
        if self.card_task:
            self.sm.get_screen('main').remove_widget(self.card_task)
            self.sm.get_screen('main').ids.plusButton.disabled = False
            self.sm.get_screen('main').ids.TaskSwiper.disabled = False
            self.card_task = None

        self.sm.get_screen('main').remove_widget(self.FadeCardInstance)
              
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

        self.sm.get_screen('main').add_widget(self.FadeCardInstance)
        self.sm.get_screen('main').ids.TaskSwiper.disabled = True
        self.sm.get_screen('main').ids.plusButton.disabled = True
        
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

                self.sm.get_screen('main').remove_widget(self.FadeCardInstance)
                self.sm.get_screen('main').ids.plusButton.disabled = False
                self.sm.get_screen('main').ids.TaskSwiper.disabled = False
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
                    
                    padding = "1sp",
                    spacing = "10sp"
                    )
                )
            index += 1

        self.FadeCardInstance = FadeCard()

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

        #Remove Objects
        self.FadeCardInstance = None

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

        self.checkbutton = MDIconButton(
                           icon = 'check-bold',
                           pos_hint = {'center_x': 0.45,'center_y': 0.2},
                           md_bg_color = checkButtonColor,
                           on_release = self.CheckTask,
                        )
        self.deleteButton = MDIconButton(
                       icon = 'delete',
                       pos_hint = {'center_x': 0.75,'center_y': 0.2},
                       md_bg_color = "red",
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