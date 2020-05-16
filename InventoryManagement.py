from tkinter import *
import sqlite3
from tkinter import ttk
import tkinter.messagebox as tkMessageBox
from tkinter.filedialog import askopenfile 
from PollyReports import *
from reportlab.pdfgen.canvas import Canvas
import os
import datetime

Home = Tk()
Home.title("Inventory Management System")
width = Home.winfo_screenwidth()/2
height = Home.winfo_screenheight()/2
screen_width = Home.winfo_screenwidth()
screen_height = Home.winfo_screenheight()
x = (screen_width/2) - (width/2)
y = (screen_height/2) - (height/2)
Home.geometry("%dx%d+%d+%d" % (width, height, x, y))
Home.resizable(0, 0)

#========================================VARIABLES========================================
NAME = StringVar()
LEDGERNUMBER = StringVar()
LEDGERPAGENUMBER = StringVar()
PAGENUMBER = IntVar()
QUANTITY = IntVar()
SEARCH = StringVar()
FIRSTNAME = StringVar()
LASTNAME = StringVar()
DESIGNATION = StringVar()
ITEMNAME = StringVar()
ATTACHEDFILE = StringVar()
BALANCE = IntVar()
SHOWBALANCE = StringVar()
RESULT = StringVar()
COMBOBOX = StringVar()
NAMEFILTER = StringVar()
ITEMFILTER = StringVar()
ITEMCOST = DoubleVar()
ITEMTYPE = StringVar()
CRVNUMBER = StringVar()
RIVNUMBER = StringVar()
ISINSTALLED = IntVar()
CONDEMNEDNUMBER = StringVar()
SECTION = StringVar()
DATE = StringVar()
#========================================METHODS==========================================


def ResetAllEntries():

    #Reset user details
    FIRSTNAME.set("")
    LASTNAME.set("")
    DESIGNATION.set("")

    #Reset new item details
    NAME.set("")
    LEDGERNUMBER.set("")
    LEDGERPAGENUMBER.set("")
    PAGENUMBER.set(0)
    ITEMNAME.set("")
    ATTACHEDFILE.set("")
    QUANTITY.set(0)
    BALANCE.set(0)
    ITEMCOST.set(0.00)
    ITEMTYPE.set("")
    CRVNUMBER.set("")
    RIVNUMBER.set("")
    CONDEMNEDNUMBER.set("")
    ISINSTALLED.set(0)

    #Reset extra details
    NAMEFILTER.set("")
    ITEMFILTER.set("")
    SEARCH.set("")
    RESULT.set("")


def Database(section):
    global conn, cursor
    conn = sqlite3.connect(f"{SECTION.get()}.db")
    cursor = conn.cursor()
    cursor.execute("""CREATE TABLE IF NOT EXISTS LogTableInfo (IndexId INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                      Name TEXT, LedgerNumber TEXT, LedgerPageNumber TEXT, PageNumber INTEGER, ItemName TEXT,
                     Quantity INTEGER, Date TEXT, Type TEXT, Balance INTEGER, Section TEXT)""")
    cursor.execute("""CREATE TABLE IF NOT EXISTS InventTable (Section TEXT, LedgerNumber TEXT,
                      LedgerPageNumber TEXT, PageNumber INTEGER, ItemName TEXT, AttachedFiles TEXT,
                      Quantity INTEGER, Balance INTEGER, ItemCost FLOAT, CRVNumber TEXT, RIVNumber TEXT,
                      ItemType TEXT, CondemnedNumber TEXT,PRIMARY KEY (LedgerNumber, LedgerPageNumber, PageNumber))""")
    cursor.execute("""CREATE TABLE IF NOT EXISTS UserInfo (IndexId INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                      FirstName TEXT, LastName TEXT, Designation TEXT, Section TEXT)""")
    conn.commit()
        
def PrintInventoryDetails():
    global printinventorydetails
    printinventorydetails = Toplevel()
    printinventorydetails.title("Inventory Management System / Print details")
    width =500
    height = 500
    screen_width = Home.winfo_screenwidth()
    screen_height = Home.winfo_screenheight()
    x = (screen_width/2) - (width/2)
    y = (screen_height/2) - (height/2)
    printinventorydetails.geometry("%dx%d+%d+%d" % (width, height, x, y))
    printinventorydetails.resizable(0, 0)
    PrintingDetails()

def PrintingDetails():
    ResetAllEntries()
    global ledgerpagenumber, pagenumber
    TopPrintingDetails = Frame(printinventorydetails, width=600, height=100, bd=1, relief=SOLID)
    TopPrintingDetails.pack(side=TOP, pady=20)
    MidPrintingDetails = Frame(printinventorydetails, width=600)
    MidPrintingDetails.pack(side=TOP, pady=20)
    lbl_text = Label(TopPrintingDetails, text="Print", font=('arial', 18), width=600)
    lbl_text.pack(fill=X)
    lbl_result = Label(MidPrintingDetails, textvariable=RESULT, font=('arial', 10), bd=10, fg="red")
    lbl_result.grid(row=4, columnspan=2)
    lbl_ledgernumber = Label(MidPrintingDetails, text="Ledger number:", font=('arial', 16), bd=10)
    lbl_ledgernumber.grid(row=0, sticky=W)
    lbl_ledgerpagenumber = Label(MidPrintingDetails, text="Ledger page number:", font=('arial', 16), bd=10)
    lbl_ledgerpagenumber.grid(row=1, sticky=W)
    lbl_pagenumber = Label(MidPrintingDetails, text="Page number:", font=('arial', 16), bd=10)
    lbl_pagenumber.grid(row=2, sticky=W)
    ledgernumber = ttk.Combobox(MidPrintingDetails, values = LedgerNumber(), textvariable=LEDGERNUMBER, font=('arial', 16), width=15)
    ledgernumber.bind("<<ComboboxSelected>>", LedgerNumberSelection)
    ledgernumber.grid(row=0, column=1)
    ledgerpagenumber = ttk.Combobox(MidPrintingDetails, values = [], textvariable=LEDGERPAGENUMBER, font=('arial', 16), width=15)
    ledgerpagenumber.bind("<<ComboboxSelected>>", LedgerPageNumberSelection)
    ledgerpagenumber.grid(row=1, column=1)
    pagenumber = ttk.Combobox(MidPrintingDetails, values = [], textvariable=PAGENUMBER, font=('arial', 16), width=15)
    pagenumber.grid(row=2, column=1)
    btn_add = Button(MidPrintingDetails, text="Print", font=('arial', 16), width=30, bg="#009ACD", command=PrintData)
    btn_add.grid(row=3, columnspan=2, pady=20)
    
def LedgerNumberSelection(event = None):
    if(LEDGERNUMBER.get()!=""):
        LEDGERPAGENUMBER.set("")
        PAGENUMBER.set(0)
        Database(SECTION.get())
        cursor.execute(f"""SELECT DISTINCT LedgerPageNumber FROM InventTable 
                           WHERE LedgerNumber = '{LEDGERNUMBER.get()}' and Section = '{SECTION.get()}'""")
        fetch = cursor.fetchall()
        ledgerpagenumbers = ["{}".format(data[0]) for data in fetch]
        ledgerpagenumber['values'] = ledgerpagenumbers
        cursor.close()
        conn.close()

def LedgerPageNumberSelection(event = None):
    if(LEDGERNUMBER.get()!="" and LEDGERPAGENUMBER.get()!=""):
        PAGENUMBER.set(0)
        Database(SECTION.get())
        cursor.execute(f"""SELECT DISTINCT PageNumber FROM InventTable 
                           WHERE Section = '{SECTION.get()}' and LedgerNumber = '{LEDGERNUMBER.get()}'
                           and LedgerPageNumber = '{LEDGERPAGENUMBER.get()}'""")
        fetch = cursor.fetchall()
        pagenumbers = ["{}".format(data[0]) for data in fetch]
        pagenumber['values'] = pagenumbers
        cursor.close()
        conn.close()

def PrintData():
    Database(SECTION.get())
    if(LEDGERNUMBER.get()!=""):
        if(LEDGERPAGENUMBER.get()!=""):
            if(PAGENUMBER.get()!=None and PAGENUMBER.get() > 0):    PrintPageNumber()
            else:   PrintLedgerPageNumber()
        else:   PrintLedgerNumber()
        ResetAllEntries()
        RESULT.set("Successful")
    else:   RESULT.set("Please select ledger number")
    cursor.close()
    conn.close()


#Print data for one page number
def PrintPageNumber():
    cursor.execute(f"""SELECT * FROM LogTableInfo 
                       WHERE Section = '{SECTION.get()}' and LedgerNumber = '{LEDGERNUMBER.get()}' 
                       and LedgerPageNumber = '{LEDGERPAGENUMBER.get()}' and PageNumber = {PAGENUMBER.get()} ORDER BY Date""")
    columns = [col[0] for col in cursor.description]
    rows = [dict(zip(columns, row)) for row in cursor.fetchall()]
    if(len(rows) == 0): rows = [{"Name":"-","Date":"-","Quantity":"-","Type":"-","Balance":"-"}]
    cursor.execute(f"""SELECT * FROM InventTable 
                       WHERE Section = '{SECTION.get()}' and LedgerNumber = '{LEDGERNUMBER.get()}' 
                       and LedgerPageNumber = '{LEDGERPAGENUMBER.get()}' and PageNumber = {PAGENUMBER.get()}""")
    fetch = cursor.fetchone()
    rpt = Report(datasource = rows, detailband = Band([
    Element((0, 10), ("Helvetica", 8), key = "Name"),
    Element((200, 10), ("Helvetica", 8), key = "Date"),
    Element((280, 10), ("Helvetica", 8), key = "Quantity"),
    Element((360, 10), ("Helvetica", 8), key = "Type"),
    Element((440, 10), ("Helvetica", 8), key = "Balance")]))
    #cursor.execute("""CREATE TABLE IF NOT EXISTS InventTable (Section TEXT, LedgerNumber TEXT,
    #                  LedgerPageNumber TEXT, PageNumber INTEGER, ItemName TEXT, AttachedFiles TEXT,
    #                  Quantity INTEGER, Balance INTEGER, ItemCost FLOAT, CRVNumber TEXT, RIVNumber TEXT,
    #                  ItemType TEXT, DateOfPurchase DATE, DateOfInstallation DATE, IsInstalled INTEGER,
    #                  CondemnedNumber TEXT,PRIMARY KEY (LedgerNumber, LedgerPageNumber, PageNumber))""")
    rpt.pageheader = Band([
    Element((0, 0), ("Times-Bold", 10), text = "Ledger Number:"), 
    Element((90, 0), ("Helvetica", 8), text = "{}".format(LEDGERNUMBER.get())),
    Element((190, 0), ("Times-Bold", 10), text = "Ledger Page Number:"),
    Element((290, 0), ("Helvetica", 8), text = "{}".format(LEDGERPAGENUMBER.get())),
    Element((385, 0), ("Times-Bold", 10), text = "Page Number:"),
    Element((470, 0), ("Helvetica", 8), text = "{}".format(PAGENUMBER.get())),
    Element((0, 16), ("Times-Bold", 10), text = "Item name:"),
    Element((90, 16), ("Helvetica", 8), text = "{}".format(fetch[4])),
    Element((0, 32), ("Times-Bold", 10), text = "File attached:"),
    Element((90, 32), ("Helvetica", 8), text = "{}".format(fetch[5])) if fetch[15] != "" else Element((90, 32), ("Helvetica", 8), text = "None"),
    Element((0, 48), ("Times-Bold", 10), text = "Quantity:"),
    Element((90, 48), ("Helvetica", 8), text = "{}".format(fetch[6])),
    Element((190, 48), ("Times-Bold", 10), text = "Item cost:"),
    Element((290, 48), ("Helvetica", 8), text = "Rs. {}".format(round(fetch[8],2))),
    Element((385, 48), ("Times-Bold", 10), text = "Item type:"),
    Element((470, 48), ("Helvetica", 8), text = "{}".format(fetch[11])),
    Element((0, 80), ("Times-Bold", 10), text = "CRV number:") if fetch[9] != "" else Element((0, 80), ("Times-Bold", 10), text = ""),
    Element((90, 80), ("Helvetica", 8), text = "{}".format(fetch[9])) if fetch[9] != "" else Element((90, 80), ("Helvetica", 8), text = ""),
    Element((0, 96), ("Times-Bold", 10), text = "R/IV number:") if fetch[10] != "" else Element((0, 96), ("Times-Bold", 10), text = ""),
    Element((90, 96), ("Helvetica", 8), text = "{}".format(fetch[10])) if fetch[10] != "" else Element((90, 96), ("Helvetica", 8), text = ""),
    Element((0, 112), ("Times-Bold", 10), text = "Condemned number:") if fetch[15] != "" else Element((0, 112), ("Times-Bold", 10), text = ""),
    Element((100, 112), ("Helvetica", 8), text = "{}".format(fetch[15])) if fetch[15] != "" else Element((90, 112), ("Helvetica", 8), text = ""),
    Element((0, 128), ("Helvetica", 8), text = "Name"),
    Element((200, 128), ("Helvetica", 8), text = "Date"),
    Element((280, 128), ("Helvetica", 8), text = "Quantity"),
    Element((360, 128), ("Helvetica", 8), text = "Type"),
    Element((440, 128), ("Helvetica", 8), text = "Balance"),
    Rule((0, 141), 7.5*72, thickness = 1)])
    desktop_path = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop')
    canvas = Canvas("{}\\{}_{}_{}.pdf".format(desktop_path.replace('\\','\\\\'),LEDGERNUMBER.get(),LEDGERPAGENUMBER.get(),PAGENUMBER.get()))
    rpt.generate(canvas)
    canvas.save()

def PrintLedgerPageNumber():
    cursor.execute(f"SELECT * FROM InventTable WHERE Section = '{SECTION.get()}' and LedgerNumber = '{LEDGERNUMBER.get()}' and LedgerPageNumber = '{LEDGERPAGENUMBER.get()}'")
    columns = [col[0] for col in cursor.description]
    rows = [dict(zip(columns, row)) for row in cursor.fetchall()]
    for i in range(0,len(rows)):
        if(len(rows[i]['ItemName'])>40): rows[i]['ItemName'] = rows[i]['ItemName'][:40]
    rpt = Report(datasource = rows, detailband = Band([
    Element((0, 10), ("Helvetica", 8), key = "ItemName"),
    Element((200, 10), ("Helvetica", 8), key = "PageNumber"),
    Element((280, 10), ("Helvetica", 8), key = "Quantity"),
    Element((360, 10), ("Helvetica", 8), key = "Balance")]))
    rpt.pageheader = Band([
    Element((0, 0), ("Times-Bold", 10), text = "Ledger Number:"),
    Element((100, 0), ("Helvetica", 8), text = "{}".format(LEDGERNUMBER.get())),
    Element((300, 0), ("Times-Bold", 10), text = "Ledger Page Number:"),
    Element((400, 0), ("Helvetica", 8), text = "{}".format(LEDGERPAGENUMBER.get())),
    Element((0, 20), ("Helvetica", 8), text = "Item name"),
    Element((200, 20), ("Helvetica", 8), text = "Page number"),
    Element((280, 20), ("Helvetica", 8), text = "Quantity"),
    Element((360, 20), ("Helvetica", 8), text = "Balance"),
    Rule((0, 32), 7.5*72, thickness = 1)])
    desktop_path = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop')
    canvas = Canvas("{}\\{}_{}.pdf".format(desktop_path.replace('\\','\\\\'),LEDGERNUMBER.get(),LEDGERPAGENUMBER.get()))
    rpt.generate(canvas)
    canvas.save()

def PrintLedgerNumber():
    cursor.execute(f"SELECT * FROM InventTable WHERE Section = '{SECTION.get()}' and LedgerNumber = '{LEDGERNUMBER.get()}' ORDER BY LedgerPageNumber, PageNumber")
    columns = [col[0] for col in cursor.description]
    rows = [dict(zip(columns, row)) for row in cursor.fetchall()]
    for i in range(0,len(rows)):
        if(len(rows[i]['ItemName'])>40): rows[i]['ItemName'] = rows[i]['ItemName'][:40]
    rpt = Report(datasource = rows, detailband = Band([
    Element((0, 10), ("Helvetica", 8), key = "ItemName"),
    Element((200, 10), ("Helvetica", 8), key = "LedgerPageNumber"),
    Element((300, 10), ("Helvetica", 8), key = "PageNumber"),
    Element((360, 10), ("Helvetica", 8), key = "Quantity")]))
    rpt.pageheader = Band([
    Element((0, 0), ("Times-Bold", 12), text = "Ledger Number:"),
    Element((100, 0), ("Helvetica", 10), text = f"{LEDGERNUMBER.get()}"),
    Element((0, 20), ("Helvetica", 8), text = "Item name"),
    Element((200, 20), ("Helvetica", 8), text = "Ledger page no."),
    Element((300, 20), ("Helvetica", 8), text = "Page number"),
    Element((360, 20), ("Helvetica", 8), text = "Quantity"),
    Rule((0, 32), 7.5*72, thickness = 1)])
    desktop_path = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop')
    canvas = Canvas("{}\\{}.pdf".format(desktop_path.replace('\\','\\\\'),LEDGERNUMBER.get()))
    rpt.generate(canvas)
    canvas.save()
#========================================INVENTORY FORM===================================

def ShowItemNew():
    global itemnewform
    itemnewform = Toplevel()
    itemnewform.title("Inventory Management System / New item")
    width =Home.winfo_screenwidth()*0.4
    height = Home.winfo_screenheight()*0.95
    screen_width = Home.winfo_screenwidth()
    screen_height = Home.winfo_screenheight()
    x = (screen_width/2) - (width/2)
    y = (screen_height/2) - (height/2)
    itemnewform.geometry("%dx%d+%d+%d" % (width, height, x, y))
    itemnewform.resizable(0, 0)
    ItemNewForm()

def ItemNewForm():
    ResetAllEntries()
    TopItemNew = Frame(itemnewform, width=600, height=100, bd=1, relief=SOLID)
    TopItemNew.pack(side=TOP, pady=10)
    MidItemNew = Frame(itemnewform, width=600)
    MidItemNew.pack(side=TOP, pady=10)
    lbl_text = Label(TopItemNew, text="New item", font=('arial', 14), width=600)
    lbl_text.pack(fill=X)
    lbl_ledgernumber = Label(MidItemNew, text="Ledger:", font=('arial', 12), bd=10)
    lbl_ledgernumber.grid(row=2, sticky=W)
    lbl_ledgerpagenumber = Label(MidItemNew, text="Ledger page number:", font=('arial', 12), bd=10)
    lbl_ledgerpagenumber.grid(row=0, sticky=W)
    lbl_pagenumber = Label(MidItemNew, text="Inventory page number:", font=('arial', 12), bd=10)
    lbl_pagenumber.grid(row=1, sticky=W)
    lbl_itemname = Label(MidItemNew, text="Item name:", font=('arial', 12), bd=10)
    lbl_itemname.grid(row=4, sticky=W)
    lbl_attachfile = Label(MidItemNew, text="Attach file:", font=('arial', 12), bd=10)
    lbl_attachfile.grid(row=5, sticky=W)
    lbl_quantity = Label(MidItemNew, text="Quantity:", font=('arial', 12), bd=10)
    lbl_quantity.grid(row=6, sticky=W)
    lbl_itemcost = Label(MidItemNew, text="Item cost:", font=('arial', 12), bd=10)
    lbl_itemcost.grid(row=3, sticky=W)
    lbl_rivnumber = Label(MidItemNew, text="R / IV number:", font=('arial', 12), bd=10)
    lbl_rivnumber.grid(row=7, sticky=W)
    lbl_crvnumber = Label(MidItemNew, text="CRV number:", font=('arial', 12), bd=10)
    lbl_crvnumber.grid(row=8, sticky=W)
    lbl_itemtype = Label(MidItemNew, text="Item Type:", font=('arial', 12), bd=10)
    lbl_itemtype.grid(row=9, sticky=W)
    lbl_condemnednumber = Label(MidItemNew, text="Condemned number:", font=('arial', 12), bd=10)
    lbl_condemnednumber.grid(row=12, sticky=W)
    lbl_result = Label(MidItemNew, textvariable=RESULT, font=('arial', 8), bd=10, fg="red")
    lbl_result.grid(row=14, columnspan = 2)

    ledgerpagenumber = Entry(MidItemNew, textvariable = LEDGERPAGENUMBER, font=('arial', 12), width=15)
    ledgerpagenumber.grid(row=0, column=1)
    pagenumber = Entry(MidItemNew, textvariable = PAGENUMBER, font=('arial', 12), width=15)
    pagenumber.grid(row=1, column=1)
    ledgernumber = Entry(MidItemNew, textvariable = LEDGERNUMBER, font=('arial', 12), width=15)
    ledgernumber.grid(row=2, column=1)
    itemcost = Entry(MidItemNew, textvariable = ITEMCOST, font=('arial', 12), width=15)
    itemcost.grid(row=3, column=1)
    itemname = Entry(MidItemNew, textvariable = ITEMNAME, font=('arial', 12), width=15)
    itemname.grid(row=4, column=1)
    btn_attachfile = Button(MidItemNew, text="Attach", font=('arial', 8), width=10, bg="#009ACD", command=AttachFile)
    btn_attachfile.grid(row=5, column=1)
    quantity = Entry(MidItemNew, textvariable = QUANTITY, font=('arial', 12), width=15)
    quantity.grid(row=6, column=1)
    rivnumber = Entry(MidItemNew, textvariable = RIVNUMBER, font=('arial', 12), width=15)
    rivnumber.grid(row=7, column=1)
    crvnumber = Entry(MidItemNew, textvariable = CRVNUMBER, font=('arial', 12), width=15)
    crvnumber.grid(row=8, column=1)
    itemtype = ttk.Combobox(MidItemNew, textvariable = ITEMTYPE, values = ["Consumable", "Non-Consumable", "NCF"], font=('arial', 12), width=15)
    itemtype.grid(row=9, column=1)
    condemnednumber = Entry(MidItemNew, textvariable = CONDEMNEDNUMBER, font=('arial', 12), width=15)
    condemnednumber.grid(row=12, column=1)
    btn_add = Button(MidItemNew, text="Save", font=('arial', 10), width=30, bg="#009ACD", command=ItemNew)
    btn_add.grid(row=13, columnspan=2, pady=10)

def ItemNew():
    Database(SECTION.get())
    LEDGERNUMBER.set(LEDGERNUMBER.get().strip())
    LEDGERPAGENUMBER.set(LEDGERPAGENUMBER.get().strip())
    if(LEDGERNUMBER.get()!="" and LEDGERPAGENUMBER.get()!="" and PAGENUMBER.get()!=None and PAGENUMBER.get()>0 and ITEMNAME.get()!="" 
      and QUANTITY.get()!=None and QUANTITY.get()>0 and ITEMTYPE.get()!=""):
        cursor.execute(f"""SELECT * FROM InventTable
        WHERE Section = '{SECTION.get()}' and LedgerNumber = '{LEDGERNUMBER.get()}' 
        and LedgerPageNumber = '{LEDGERPAGENUMBER.get()}' and PageNumber = {PAGENUMBER.get()}""")
        if(cursor.fetchone() is None):
            cursor.execute("""INSERT INTO InventTable 
            (Section, LedgerNumber, LedgerPageNumber, PageNumber, ItemName, Quantity, Balance, ItemCost, ItemType,
            AttachedFiles, RIVNumber, CRVNumber, IsInstalled, CondemnedNumber) 
            VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
            (SECTION.get(), LEDGERNUMBER.get(), LEDGERPAGENUMBER.get(), PAGENUMBER.get(), ITEMNAME.get(), QUANTITY.get(), QUANTITY.get(),
            ITEMCOST.get(), ITEMTYPE.get(), ATTACHEDFILE.get(), RIVNUMBER.get(), CRVNUMBER.get(), CONDEMNEDNUMBER.get()))
            conn.commit()
            ResetAllEntries()
            RESULT.set("Success")
        else: 
            RESULT.set("Item already exists")
    else: 
        RESULT.set("Please enter all details")
    cursor.close()
    conn.close()

def AttachFile():
    file = askopenfile(mode ='r', filetypes = [('Attach a file','.pdf')]) 
    if file is not None:
        ATTACHEDFILE.set(file.name)
    else:
        ATTACHEDFILE.set("")

#========================================USER FORM===================================

def ShowUserNew():
    global usernewform
    usernewform = Toplevel()
    usernewform.title("Inventory Management System / Create new user")
    width = 500
    height = 400
    screen_width = Home.winfo_screenwidth()
    screen_height = Home.winfo_screenheight()
    x = (screen_width/2) - (width/2)
    y = (screen_height/2) - (height/2)
    usernewform.geometry("%dx%d+%d+%d" % (width, height, x, y))
    usernewform.resizable(0, 0)
    UserNewForm()

def UserNewForm():
    ResetAllEntries()
    TopUserNew = Frame(usernewform, width=600, height=100, bd=1, relief=SOLID)
    TopUserNew.pack(side=TOP, pady=20)
    MidUserNew = Frame(usernewform, width=600)
    MidUserNew.pack(side=TOP, pady=20)
    lbl_text = Label(TopUserNew, text="New user", font=('arial', 18), width=600)
    lbl_text.pack(fill=X)
    lbl_firstname = Label(MidUserNew, text="First Name:", font=('arial', 16), bd=10)
    lbl_firstname.grid(row=0, sticky=W)
    lbl_lastname = Label(MidUserNew, text="Last Name:", font=('arial', 16), bd=10)
    lbl_lastname.grid(row=1, sticky=W)
    lbl_designation = Label(MidUserNew, text="Designation:", font=('arial', 16), bd=10)
    lbl_designation.grid(row=2, sticky=W)
    lbl_result = Label(MidUserNew, textvariable=RESULT, font=('arial', 10), bd=10,fg="red")
    lbl_result.grid(row=4, columnspan=2)
    firstname = Entry(MidUserNew, textvariable = FIRSTNAME, font=('arial', 16), width=15)
    firstname.grid(row=0, column=1)
    lastname = Entry(MidUserNew, textvariable = LASTNAME, font=('arial', 16), width=15)
    lastname.grid(row=1, column=1)
    designation = Entry(MidUserNew, textvariable = DESIGNATION, font=('arial', 16), width=15)
    designation.grid(row=2, column=1)
    btn_add = Button(MidUserNew, text="Save", font=('arial', 16), width=30, bg="#009ACD", command=UserNew)
    btn_add.grid(row=3, columnspan=2, pady=20)

def UserNew():
    Database(SECTION.get())
    FIRSTNAME.set(FIRSTNAME.get().strip())
    LASTNAME.set(LASTNAME.get().strip())
    DESIGNATION.set(DESIGNATION.get().strip())
    if(FIRSTNAME.get()!="" and LASTNAME.get()!="" and DESIGNATION.get()!=""):
        cursor.execute("INSERT INTO UserInfo (Section, FirstName, LastName, Designation) VALUES(?, ?, ?, ?)", (SECTION.get(), FIRSTNAME.get(), LASTNAME.get(), DESIGNATION.get()))
        conn.commit()
        ResetAllEntries()
    else:
       RESULT.set("Please enter all details")
    cursor.close()
    conn.close()

#========================================ISSUE FORM===================================

def ShowIssueItem():
    global issuenewform
    issuenewform = Toplevel()
    issuenewform.title("Inventory Management System / Issue item")
    width = 500
    height = 500
    screen_width = Home.winfo_screenwidth()
    screen_height = Home.winfo_screenheight()
    x = (screen_width/2) - (width/2)
    y = (screen_height/2) - (height/2)
    issuenewform.geometry("%dx%d+%d+%d" % (width, height, x, y))
    issuenewform.resizable(0, 0)
    IssueNewForm()

def IssueNewForm():
    global name, itemname 
    ResetAllEntries()
    TopIssueNew = Frame(issuenewform, width=600, height=100, bd=1, relief=SOLID)
    TopIssueNew.pack(side=TOP, pady=20)
    lbl_text = Label(TopIssueNew, text="Issue item", font=('arial', 18), width=600)
    lbl_text.pack(fill=X)
    MidIssueNew = Frame(issuenewform, width=600)
    MidIssueNew.pack(side=TOP, pady=20)
    lbl_name = Label(MidIssueNew, text="Name:", font=('arial', 16), bd=10)
    lbl_name.grid(row=0, sticky=W)
    lbl_date = Label(MidIssueNew, text="Issue date:", font=('arial', 16), bd=10)
    lbl_date.grid(row=1, sticky=W)
    lbl_itemname = Label(MidIssueNew, text="Item name:", font=('arial', 16), bd=10)
    lbl_itemname.grid(row=2, sticky=W)
    lbl_balance = Label(MidIssueNew, text="Balance:", font=('arial', 16), bd=10)
    lbl_balance.grid(row=3, sticky=W)
    lbl_quantity = Label(MidIssueNew, text="Quantity:", font=('arial', 16), bd=10)
    lbl_quantity.grid(row=4, sticky=W)
    lbl_result = Label(MidIssueNew, textvariable = RESULT, font=('arial', 10), bd=10, fg="red")
    lbl_result.grid(row=6, columnspan = 2)
    name = ttk.Combobox(MidIssueNew, values = Names(), textvariable = NAME, font=('arial', 16), width=15)
    name.grid(row=0, column=1)
    namefilter = Entry(MidIssueNew, textvariable=NAMEFILTER, font=('arial', 8), width=8)
    namefilter.grid(row=0, column=2)
    btn_namefilter = Button(MidIssueNew, text="Search", font=('arial', 8), width=5, bg="#009ACD", command = FilterName)
    btn_namefilter.grid(row=0, column=3)
    issueDate = Entry(MidIssueNew, textvariable=DATE, font=('arial', 16), width=15)
    issueDate.grid(row=1, column=1)
    itemname = ttk.Combobox(MidIssueNew, values = Items(), textvariable=ITEMNAME, font=('arial', 16), width=15)
    itemname.bind("<<ComboboxSelected>>", SetBalance)
    itemname.grid(row=2, column=1)
    itemfilter = Entry(MidIssueNew, textvariable=ITEMFILTER, font=('arial', 8), width=8)
    itemfilter.grid(row=2, column=2)
    btn_itemfilter = Button(MidIssueNew, text="Search", font=('arial', 8), width=5, bg="#009ACD", command = FilterItemName)
    btn_itemfilter.grid(row=2, column=3)
    balance = Label(MidIssueNew, textvariable=BALANCE, font=('arial', 16), bd=10)
    balance.grid(row=3, column=1)
    quantity = Entry(MidIssueNew, textvariable=QUANTITY, font=('arial', 16), width=15)
    quantity.grid(row=4, column=1)
    btn_add = Button(MidIssueNew, text="Save", font=('arial', 16), width=30, bg="#009ACD", command=IssueNew)
    btn_add.grid(row=5, columnspan=2, pady=20)

def FilterItemName():
    itemname['values'] = Items()

def FilterName():
    name['values'] = Names()

def SetBalance(event = None):
    if(ITEMNAME.get()!=""):
        BALANCE.set(int(ITEMNAME.get().split('/Balance:')[1]))
        ITEMNAME.set(ITEMNAME.get().split('/Balance:')[0])

def IssueNew():
    Database(SECTION.get())
    format = "%d/%m/%Y"
    Delta = datetime.strptime(DATE.get(),format) - datetime.strptime(date.today().strftime(format),format)
    if(ITEMNAME.get()!="" and NAME.get()!="" and QUANTITY.get()!=None and QUANTITY.get()>0):
        if(Delta.days <= 0):
            newbalance = BALANCE.get() - QUANTITY.get()
            if(newbalance >= 0):
                cursor.execute(f"SELECT LedgerNumber, LedgerPageNumber, PageNumber FROM InventTable WHERE Section = '{SECTION.get()}' and ItemName = '{ITEMNAME.get()}' and Balance = {BALANCE.get()}")
                data = cursor.fetchone()
                cursor.execute("UPDATE InventTable SET Balance = {} WHERE LedgerNumber = '{}' and LedgerPageNumber = '{}' and PageNumber = {} and Section = '{}'".format(newbalance, data[0], data[1], data[2], SECTION.get()))
                cursor.execute("INSERT INTO LogTableInfo (Name, Date, ItemName, LedgerNumber, LedgerPageNumber, PageNumber, Quantity, Type, Balance, Section) VALUES(?, ?, ?, ?, ?, ?, ?, 'Issued', ?,?)",
                          (NAME.get(), DATE.get(), ITEMNAME.get(), data[0], data[1], data[2], QUANTITY.get(), newbalance, SECTION.get()))
                conn.commit()
                ResetAllEntries()
            else: 
                RESULT.set("Insufficient balance")
        else: 
            RESULT.set("Cannot be issued for future dates")
    else: 
        RESULT.set("Please enter all details")
    cursor.close()
    conn.close()


#========================================RETURN FORM===================================

def ShowReturnItem():
    global returnnewform
    returnnewform = Toplevel()
    returnnewform.title("Inventory Management System / Return item")
    width = 500
    height = 500
    screen_width = Home.winfo_screenwidth()
    screen_height = Home.winfo_screenheight()
    x = (screen_width/2) - (width/2)
    y = (screen_height/2) - (height/2)
    returnnewform.geometry("%dx%d+%d+%d" % (width, height, x, y))
    returnnewform.resizable(0, 0)
    ReturnNewForm()

def ReturnNewForm():
    global name, itemname
    ResetAllEntries()
    TopReturnNew = Frame(returnnewform, width=600, height=100, bd=1, relief=SOLID)
    TopReturnNew.pack(side=TOP, pady=20)
    lbl_text = Label(TopReturnNew, text="Return item", font=('arial', 18), width=600)
    lbl_text.pack(fill=X)
    MidReturnNew = Frame(returnnewform, width=600)
    MidReturnNew.pack(side=TOP, pady=20)
    lbl_name = Label(MidReturnNew, text="Name:", font=('arial', 16), bd=10)
    lbl_name.grid(row=0, sticky=W)
    lbl_date = Label(MidReturnNew, text="Return date:", font=('arial', 16), bd=10)
    lbl_date.grid(row=1, sticky=W)
    lbl_itemname = Label(MidReturnNew, text="Item name:", font=('arial', 16), bd=10)
    lbl_itemname.grid(row=2, sticky=W)
    lbl_quantity = Label(MidReturnNew, text="Quantity:", font=('arial', 16), bd=10)
    lbl_quantity.grid(row=3, sticky=W)
    name = ttk.Combobox(MidReturnNew, values = Names(), textvariable = NAME, font=('arial', 16), width=15)
    name.grid(row=0, column=1)
    namefilter = Entry(MidReturnNew, textvariable=NAMEFILTER, font=('arial', 8), width=8)
    namefilter.grid(row=0, column=2)
    btn_namefilter = Button(MidReturnNew, text="Search", font=('arial', 8), width=5, bg="#009ACD", command = FilterName)
    btn_namefilter.grid(row=0, column=3)
    returnDate = Entry(MidReturnNew, textvariable=DATE, font=('arial', 16), width=15)
    returnDate.grid(row=1, column=1)
    itemname = ttk.Combobox(MidReturnNew, values = Items(), textvariable=ITEMNAME, font=('arial', 16), width=15)
    itemname.grid(row=2, column=1)
    itemfilter = Entry(MidReturnNew, textvariable=ITEMFILTER, font=('arial', 8), width=8)
    itemfilter.grid(row=2, column=2)
    btn_itemfilter = Button(MidReturnNew, text="Search", font=('arial', 8), width=5, bg="#009ACD", command = FilterItemName)
    btn_itemfilter.grid(row=2, column=3)
    quantity = Entry(MidReturnNew, textvariable=QUANTITY, font=('arial', 16), width=15)
    quantity.grid(row=3, column=1)
    btn_add = Button(MidReturnNew, text="Save", font=('arial', 16), width=30, bg="#009ACD", command=ReturnNew)
    btn_add.grid(row=4, columnspan=2, pady=20)
    lbl_result = Label(MidReturnNew, textvariable = RESULT, font=('arial', 10), bd=10, fg="red")
    lbl_result.grid(row=5, columnspan = 2)

def ReturnNew():
    Database(SECTION.get())
    format = "%d/%m/%Y"
    Delta = datetime.strptime(DATE.get(),format)-datetime.strptime(date.today().strftime(format),format)
    if(ITEMNAME.get()!= "" and NAME.get()!="" and QUANTITY.get() != None and QUANTITY.get()>0):
        if(Delta.days <= 0):
            newbalance = BALANCE.get() + QUANTITY.get()
            cursor.execute(f"SELECT LedgerNumber, LedgerPageNumber, PageNumber FROM InventTable WHERE ItemName = '{ITEMNAME.get()}' and Balance = {BALANCE.get()}")
            data = cursor.fetchone()
            cursor.execute("UPDATE InventTable SET Balance = {} WHERE LedgerNumber = '{}' and LedgerPageNumber = '{}' and PageNumber = {} and Section = '{}'".format(newbalance, data[0], data[1], data[2], SECTION.get()))
            cursor.execute("INSERT INTO LogTableInfo (Name, Date, LedgerNumber, LedgerPageNumber, PageNumber, ItemName, Quantity, Type, Balance, Section) VALUES(?, ?, ?, ?, ?, ?, ?, 'Returned', ?, ?)",
                      (NAME.get(), DATE.get(), data[0], data[1], data[2], ITEMNAME.get(), QUANTITY.get(), newbalance, SECTION.get()))
            conn.commit()
            ResetAllEntries()
        else: ERROR.set("Cannot be returned for future dates")
    else: ERROR.set("Please enter all details")
    cursor.close()
    conn.close()

def Names():
    Database(SECTION.get())
    cursor.execute(f"SELECT FirstName, LastName, Designation FROM userInfo WHERE FirstName LIKE '{NAMEFILTER.get()}%' and Section = '{SECTION.get()}'")
    fetch = cursor.fetchall()
    list = ["{} {}/{}".format(data[0], data[1], data[2]) for data in fetch]
    cursor.close()
    conn.close()
    return list

def Items():
    Database(SECTION.get())
    cursor.execute(f"SELECT ItemName, Balance FROM InventTable WHERE ItemName LIKE '{ITEMFILTER.get()}%' and Section = '{SECTION.get()}'")
    fetch = cursor.fetchall()
    list = ["{}/Balance:{}".format(data[0], data[1]) for data in fetch]
    cursor.close()
    conn.close()
    return list

def LedgerNumber():
    Database(SECTION.get())
    cursor.execute(f"SELECT DISTINCT LedgerNumber FROM InventTable WHERE Section = '{SECTION.get()}'")
    fetch = cursor.fetchall()
    list = ["{}".format(data[0]) for data in fetch]
    cursor.close()
    conn.close()
    return list
#========================================LOG VIEW FORM===================================

def LogForm():
    global tree, combobox_type
    ResetAllEntries()
    TopLogForm = Frame(logform, width=600, bd=1, relief=SOLID)
    TopLogForm.pack(side=TOP, fill=X)
    LeftLogForm = Frame(logform, width=100)
    LeftLogForm.pack(side=LEFT, fill=Y)
    MidLogForm = Frame(logform, width=1100)
    MidLogForm.pack(side=RIGHT)
    lbl_text = Label(TopLogForm, text="Logs", font=('arial', 18), width=600)
    lbl_text.pack(fill=X)
    lbl_txtsearch = Label(LeftLogForm, text="Search by name", font=('arial', 16))
    lbl_txtsearch.pack(side=TOP, anchor=W)
    search = Entry(LeftLogForm, textvariable=SEARCH, font=('arial', 16), width=10)
    search.pack(side=TOP,  padx=10, fill=X)
    btn_search = Button(LeftLogForm, text="Search", command=Search)
    btn_search.pack(side=TOP, padx=10, pady=10, fill=X)
    btn_reset = Button(LeftLogForm, text="Reset", command=Reset)
    btn_reset.pack(side=TOP, padx=10, pady=10, fill=X)
    combobox_type = ttk.Combobox(LeftLogForm,values = ['All', 'Issued', 'Returned'] ,textvariable=COMBOBOX)
    combobox_type.bind("<<ComboboxSelected>>", DisplayData)
    combobox_type.pack(side=TOP, padx=10, pady=10, fill=X)
    scrollbarx = Scrollbar(MidLogForm, orient=HORIZONTAL)
    scrollbary = Scrollbar(MidLogForm, orient=VERTICAL)
    tree = ttk.Treeview(MidLogForm, columns=("Name", "Date of Issue/Return", "Item name", "Quantity", "Type", "Balance"), selectmode="extended", height=100, yscrollcommand=scrollbary.set, xscrollcommand=scrollbarx.set)
    scrollbary.config(command=tree.yview)
    scrollbary.pack(side=RIGHT, fill=Y)
    scrollbarx.config(command=tree.xview)
    scrollbarx.pack(side=BOTTOM, fill=X)
    tree.heading('Name', text="Name",anchor=W)
    tree.heading('Date of Issue/Return', text="Date of Issue/Return",anchor=W)
    tree.heading('Item name', text="Item name",anchor=W)
    tree.heading('Quantity', text="Quantity",anchor=W)
    tree.heading('Type', text="Type",anchor=W)
    tree.heading('Balance', text="Balance",anchor=W)
    tree.column('#0', stretch=NO, minwidth=0, width=0)
    tree.column('#1', stretch=NO, minwidth=0, width=120)
    tree.column('#2', stretch=NO, minwidth=0, width=120)
    tree.column('#3', stretch=NO, minwidth=0, width=120)
    tree.column('#4', stretch=NO, minwidth=0, width=120)
    tree.column('#5', stretch=NO, minwidth=0, width=120)
    tree.column('#6', stretch=NO, minwidth=0, width=120)
    tree.pack()
    DisplayData()

def DisplayData(event = None):
    Database(SECTION.get())
    tree.delete(*tree.get_children())
    if(COMBOBOX.get()!="All" or COMBOBOX.get()!=""): cursor.execute(f"SELECT Name, Date, ItemName, Quantity, Type, Balance FROM LogTableInfo WHERE Type = '{COMBOBOX.get()}' and Section = '{SECTION.get()}'")
    else: cursor.execute(f"SELECT Name, Date, ItemName, Quantity, Type, Balance FROM LogTableInfo WHERE Section = '{SECTION.get()}'")
    fetch = cursor.fetchall()
    for data in fetch:
        tree.insert('', 'end', values=(data))
    cursor.close()
    conn.close()

#========================================USER VIEW FORM===================================

def UserForm():
    global usertree
    ResetAllEntries()
    TopUserForm = Frame(userform, width=600, bd=1, relief=SOLID)
    TopUserForm.pack(side=TOP, fill=X)
    LeftUserForm = Frame(userform, width=600)
    LeftUserForm.pack(side=LEFT, fill=Y)
    MidUserForm = Frame(userform, width=600)
    MidUserForm.pack(side=RIGHT)
    lbl_text = Label(TopUserForm, text="Users", font=('arial', 18), width=600)
    lbl_text.pack(fill=X)
    lbl_txtsearch = Label(LeftUserForm, text="Search by first name", font=('arial', 16))
    lbl_txtsearch.pack(side=TOP, anchor=W)
    search = Entry(LeftUserForm, textvariable=SEARCH, font=('arial', 16), width=10)
    search.pack(side=TOP,  padx=10, fill=X)
    btn_search = Button(LeftUserForm, text="Search", command=UserSearch)
    btn_search.pack(side=TOP, padx=10, pady=10, fill=X)
    btn_reset = Button(LeftUserForm, text="Reset", command=UserReset)
    btn_reset.pack(side=TOP, padx=10, pady=10, fill=X)
    btn_delete = Button(LeftUserForm, text="Delete", command=UserDelete)
    btn_delete.pack(side=TOP, padx=10, pady=10, fill=X)
    scrollbarx = Scrollbar(MidUserForm, orient=HORIZONTAL)
    scrollbary = Scrollbar(MidUserForm, orient=VERTICAL)
    usertree = ttk.Treeview(MidUserForm, columns=("Index", "First name", "Last name", "Designation"), selectmode="extended", height=100, yscrollcommand=scrollbary.set, xscrollcommand=scrollbarx.set)
    scrollbary.config(command=usertree.yview)
    scrollbary.pack(side=RIGHT, fill=Y)
    scrollbarx.config(command=usertree.xview)
    scrollbarx.pack(side=BOTTOM, fill=X)
    usertree.heading('Index', text="Index",anchor=W)
    usertree.heading('First name', text="First name",anchor=W)
    usertree.heading('Last name', text="Last name",anchor=W)
    usertree.heading('Designation', text="Designation",anchor=W)
    usertree.column('#0', stretch=NO, minwidth=0, width=0)
    usertree.column('#1', stretch=NO, minwidth=0, width=0)
    usertree.column('#2', stretch=NO, minwidth=0, width=100)
    usertree.column('#3', stretch=NO, minwidth=0, width=100)
    usertree.pack()
    UserDisplayData()

def UserDisplayData(event = None):
    Database(SECTION.get())
    usertree.delete(*usertree.get_children())
    cursor.execute(f"SELECT * FROM UserInfo WHERE Section = '{SECTION.get()}'")
    fetch = cursor.fetchall()
    for data in fetch:
        usertree.insert('', 'end', values=(data))
    cursor.close()
    conn.close()


#========================================INVENTORY VIEW FORM===================================

def InventoryForm():
    global inventorytree
    ResetAllEntries()
    TopInventoryForm = Frame(inventoryform, width=600, bd=1, relief=SOLID)
    TopInventoryForm.pack(side=TOP, fill=X)
    LeftInventoryForm = Frame(inventoryform, width=100)
    LeftInventoryForm.pack(side=LEFT, fill=Y)
    MidInventoryForm = Frame(inventoryform, width=1100)
    MidInventoryForm.pack(side=RIGHT)
    lbl_text = Label(TopInventoryForm, text="Inventory", font=('arial', 18), width=600)
    lbl_text.pack(fill=X)
    lbl_txtsearch = Label(LeftInventoryForm, text="Search by item name", font=('arial', 16))
    lbl_txtsearch.pack(side=TOP, anchor=W)
    search = Entry(LeftInventoryForm, textvariable=SEARCH, font=('arial', 16), width=10)
    search.pack(side=TOP,  padx=10, fill=X)
    btn_search = Button(LeftInventoryForm, text="Search", command=InventorySearch)
    btn_search.pack(side=TOP, padx=10, pady=10, fill=X)
    btn_reset = Button(LeftInventoryForm, text="Reset", command=InventoryReset)
    btn_reset.pack(side=TOP, padx=10, pady=10, fill=X)
    btn_delete = Button(LeftInventoryForm, text="Delete", command=InventoryDelete)
    btn_delete.pack(side=TOP, padx=10, pady=10, fill=X)
    btn_edit = Button(LeftInventoryForm, text="Edit", command=InventoryEdit)
    btn_edit.pack(side=TOP, padx=10, pady=10, fill=X)
    scrollbarx = Scrollbar(MidInventoryForm, orient=HORIZONTAL)
    scrollbary = Scrollbar(MidInventoryForm, orient=VERTICAL)
    inventorytree = ttk.Treeview(MidInventoryForm, columns=("Ledger number", "Ledger page number", "Page number", "Item name", "Quantity", "Balance", 
                    "Item cost", "RIV number", "CRV number", "Item type", "Attached files", "Condemned number"), selectmode="extended", height=100, yscrollcommand=scrollbary.set, xscrollcommand=scrollbarx.set)
    scrollbary.config(command=inventorytree.yview)
    scrollbary.pack(side=RIGHT, fill=Y)
    scrollbarx.config(command=inventorytree.xview)
    scrollbarx.pack(side=BOTTOM, fill=X)
    inventorytree.heading('Ledger number', text="Ledger number",anchor=W)
    inventorytree.heading('Ledger page number', text="Ledger page number",anchor=W)
    inventorytree.heading('Page number', text="Page number",anchor=W)
    inventorytree.heading('Item name', text="Item name",anchor=W)
    inventorytree.heading('Quantity', text="Quantity",anchor=W)
    inventorytree.heading('Balance', text="Balance",anchor=W)
    inventorytree.heading('Item cost', text="Item cost",anchor=W)
    inventorytree.heading('RIV number', text="RIV number",anchor=W)
    inventorytree.heading('CRV number', text="CRV number",anchor=W)
    inventorytree.heading('Item type', text="Item type",anchor=W)
    inventorytree.heading('Attached files', text="Attached files",anchor=W)
    inventorytree.heading('Condemned number', text="Condemned number",anchor=W)
    inventorytree.column('#0', stretch=NO, minwidth=0, width=0)
    inventorytree.column('#1', stretch=NO, minwidth=0, width=100)
    inventorytree.column('#2', stretch=NO, minwidth=0, width=100)
    inventorytree.column('#3', stretch=NO, minwidth=0, width=100)
    inventorytree.column('#4', stretch=NO, minwidth=0, width=200)
    inventorytree.column('#5', stretch=NO, minwidth=0, width=100)
    inventorytree.column('#6', stretch=NO, minwidth=0, width=100)
    inventorytree.column('#7', stretch=NO, minwidth=0, width=100)
    inventorytree.column('#8', stretch=NO, minwidth=0, width=100)
    inventorytree.column('#9', stretch=NO, minwidth=0, width=100)
    inventorytree.column('#10', stretch=NO, minwidth=0, width=100)
    inventorytree.column('#11', stretch=NO, minwidth=0, width=100)
    inventorytree.column('#12', stretch=NO, minwidth=0, width=100)
    inventorytree.pack()
    InventoryDisplayData()

def InventoryDisplayData(event = None):
    Database(SECTION.get())
    inventorytree.delete(*inventorytree.get_children())
    cursor.execute(f"SELECT LedgerNumber, LedgerPageNumber, PageNumber, ItemName, Quantity, Balance, ItemCost, RIVNumber, CRVNumber, ItemType, AttachedFiles, CondemnedNumber FROM InventTable WHERE Section = '{SECTION.get()}'")
    fetch = cursor.fetchall()
    for data in fetch:
        inventorytree.insert('', 'end', values=(data))
    cursor.close()
    conn.close()

def SectionForm():
    global sectiontree
    TopSectionForm = Frame(sectionform, width=600, bd=1, relief=SOLID)
    TopSectionForm.pack(side=TOP, fill=X)
    MidSectionForm = Frame(sectionform, width=1100)
    MidSectionForm.pack(fill=X)
    lbl_text = Label(TopSectionForm, text="Sections", font=('arial', 18), width=600)
    lbl_text.pack(fill=X)
    scrollbarx = Scrollbar(MidSectionForm, orient=HORIZONTAL)
    scrollbary = Scrollbar(MidSectionForm, orient=VERTICAL)
    sectiontree = ttk.Treeview(MidSectionForm, columns=("Index","Section"), selectmode="extended", height=100, yscrollcommand=scrollbary.set, xscrollcommand=scrollbarx.set)
    scrollbary.config(command=sectiontree.yview)
    scrollbary.pack(side=RIGHT, fill=Y)
    scrollbarx.config(command=sectiontree.xview)
    scrollbarx.pack(side=BOTTOM, fill=X)
    sectiontree.heading('Index', text="Index",anchor=W)
    sectiontree.heading('Section', text="Section",anchor=W)
    sectiontree.column('#0', stretch=NO, minwidth=0, width=0)
    sectiontree.column('#1', stretch=NO, minwidth=0, width=100)
    sectiontree.column('#2', stretch=NO, minwidth=0, width=100)
    sectiontree.pack()
    SectionData()

def SectionData(event = None):
    SectionSelectDatabase()
    sectiontree.delete(*sectiontree.get_children())
    cursor.execute("SELECT * FROM SectionInfo")
    fetch = cursor.fetchall()
    for data in fetch:
        sectiontree.insert('', 'end', values=(data))
    cursor.close()
    conn.close()


#========================================BUTTONS FOR INVENTORY VIEW===================================

def InventorySearch():
    if SEARCH.get() != "":
        inventorytree.delete(*inventorytree.get_children())
        Database(SECTION.get())
        cursor.execute(f"SELECT LedgerNumber, LedgerPageNumber, PageNumber, ItemName, Quantity, Balance, ItemCost, RIVNumber, CRVNumber, ItemType, AttachedFiles, CondemnedNumber FROM InventTable WHERE ItemName LIKE '%{SEARCH.get()}% and Section = '{SECTION.get()}'")
        fetch = cursor.fetchall()
        for data in fetch:
            inventorytree.insert('', 'end', values=(data))
        cursor.close()
        conn.close()

def InventoryReset():
    inventorytree.delete(*inventorytree.get_children())
    InventoryDisplayData()
    SEARCH.set("")

def InventoryDelete():
    if not inventorytree.selection():
       print("ERROR")
    else:
        result = tkMessageBox.askquestion('Inventory Management System', 'Are you sure you want to delete this record?', icon="warning")
        if result == 'yes':
            curItem = inventorytree.focus()
            contents =(inventorytree.item(curItem))
            selecteditem = contents['values']
            inventorytree.delete(curItem)
            Database(SECTION.get())
            cursor.execute(f"DELETE FROM InventTable WHERE LedgerNumber = '{selecteditem[0]}' and LedgerPageNumber = '{selecteditem[1]}' and PageNumber = {selecteditem[2]} and Section = '{SECTION.get()}'")
            conn.commit()
            cursor.close()
            conn.close()

def setValues(selecteditem):
    LEDGERNUMBER.set(selecteditem[0])
    LEDGERPAGENUMBER.set(selecteditem[1])
    PAGENUMBER.set(selecteditem[2])
    ITEMNAME.set(selecteditem[3])
    ITEMCOST.set(selecteditem[6])
    RIVNUMBER.set(selecteditem[7])
    CRVNUMBER.set(selecteditem[8])
    ITEMTYPE.set(selecteditem[9])
    CONDEMNEDNUMBER.set(selecteditem[13])

def InventoryEdit():
    if not inventorytree.selection():
       print("ERROR")
    else:
        global itemnewform
        ResetAllEntries()
        curItem = inventorytree.focus()
        contents =(inventorytree.item(curItem))
        selecteditem = contents['values']
        setValues(selecteditem)
        itemnewform = Toplevel()
        itemnewform.title("Inventory Management System / Edit item")
        width =Home.winfo_screenwidth()*0.4
        height = Home.winfo_screenheight()*0.8
        screen_width = Home.winfo_screenwidth()
        screen_height = Home.winfo_screenheight()
        x = (screen_width/2) - (width/2)
        y = (screen_height/2) - (height/2)
        itemnewform.geometry("%dx%d+%d+%d" % (width, height, x, y))
        itemnewform.resizable(0, 0)
        TopItemNew = Frame(itemnewform, width=600, height=100, bd=1, relief=SOLID)
        TopItemNew.pack(side=TOP, pady=10)
        MidItemNew = Frame(itemnewform, width=600)
        MidItemNew.pack(side=TOP, pady=10)
        lbl_text = Label(TopItemNew, text="Edit item", font=('arial', 14), width=600)
        lbl_text.pack(fill=X)
        lbl_ledgernumber = Label(MidItemNew, text="Ledger:", font=('arial', 12), bd=10)
        lbl_ledgernumber.grid(row=2, sticky=W)
        lbl_ledgerpagenumber = Label(MidItemNew, text="Ledger page number:", font=('arial', 12), bd=10)
        lbl_ledgerpagenumber.grid(row=0, sticky=W)
        lbl_pagenumber = Label(MidItemNew, text="Inventory page number:", font=('arial', 12), bd=10)
        lbl_pagenumber.grid(row=1, sticky=W)
        lbl_itemname = Label(MidItemNew, text="Item name:", font=('arial', 12), bd=10)
        lbl_itemname.grid(row=4, sticky=W)
        lbl_attachfile = Label(MidItemNew, text="Attach file:", font=('arial', 12), bd=10)
        lbl_attachfile.grid(row=5, sticky=W)
        lbl_itemcost = Label(MidItemNew, text="Item cost:", font=('arial', 12), bd=10)
        lbl_itemcost.grid(row=3, sticky=W)
        lbl_rivnumber = Label(MidItemNew, text="R / IV number:", font=('arial', 12), bd=10)
        lbl_rivnumber.grid(row=7, sticky=W)
        lbl_crvnumber = Label(MidItemNew, text="CRV number:", font=('arial', 12), bd=10)
        lbl_crvnumber.grid(row=8, sticky=W)
        lbl_itemtype = Label(MidItemNew, text="Item Type:", font=('arial', 12), bd=10)
        lbl_itemtype.grid(row=9, sticky=W)
        lbl_condemnednumber = Label(MidItemNew, text="Condemned number:", font=('arial', 12), bd=10)
        lbl_condemnednumber.grid(row=10, sticky=W)
        lbl_result = Label(MidItemNew, textvariable=RESULT, font=('arial', 8), bd=10, fg="red")
        lbl_result.grid(row=12, columnspan = 2)
        ledgerpagenumber = Label(MidItemNew, textvariable = LEDGERPAGENUMBER, font=('arial', 12))
        ledgerpagenumber.grid(row=0, column=1)
        pagenumber = Label(MidItemNew, textvariable = PAGENUMBER, font=('arial', 12))
        pagenumber.grid(row=1, column=1)
        ledgernumber = Label(MidItemNew, textvariable = LEDGERNUMBER, font=('arial', 12))
        ledgernumber.grid(row=2, column=1)
        itemcost = Entry(MidItemNew, textvariable = ITEMCOST, font=('arial', 12), width=15)
        itemcost.grid(row=3, column=1)
        itemname = Entry(MidItemNew, textvariable = ITEMNAME, font=('arial', 12), width=15)
        itemname.grid(row=4, column=1)
        btn_attachfile = Button(MidItemNew, text="Attach", font=('arial', 8), width=10, bg="#009ACD", command=AttachFile)
        btn_attachfile.grid(row=5, column=1)
        rivnumber = Entry(MidItemNew, textvariable = RIVNUMBER, font=('arial', 12), width=15)
        rivnumber.grid(row=7, column=1)
        crvnumber = Entry(MidItemNew, textvariable = CRVNUMBER, font=('arial', 12), width=15)
        crvnumber.grid(row=8, column=1)
        itemtype = ttk.Combobox(MidItemNew, textvariable = ITEMTYPE, values = ["Consumable", "Non-Consumable", "NCF"], font=('arial', 12), width=15)
        itemtype.grid(row=9, column=1)
        condemnednumber = Entry(MidItemNew, textvariable = CONDEMNEDNUMBER, font=('arial', 12), width=15)
        condemnednumber.grid(row=10, column=1)
        btn_add = Button(MidItemNew, text="Update", font=('arial', 10), width=30, bg="#009ACD", command=ItemEdit)
        btn_add.grid(row=11, columnspan=2, pady=10)


def ItemEdit():
    ITEMNAME.set(ITEMNAME.get().strip())
    if ITEMNAME.get()!="" and ITEMTYPE.get()!="":
        Database(SECTION.get())
        cursor.execute("UPDATE InventTable SET ItemName = '{}', ItemCost = {}, ItemType = '{}', AttachedFiles = '{}', RIVNumber = '{}', CRVNumber = '{}', CondemnedNumber = '{}' WHERE LedgerNumber = '{}' and LedgerPageNumber = '{}'and PageNumber = {} and Section = '{}'"
                       .format(ITEMNAME.get(), ITEMCOST.get(), ITEMTYPE.get(), ATTACHEDFILE.get(), RIVNUMBER.get(), CRVNUMBER.get(), CONDEMNEDNUMBER.get(), LEDGERNUMBER.get(), LEDGERPAGENUMBER.get(), PAGENUMBER.get(), SECTION.get()))
        conn.commit()
        cursor.close()
        conn.close()
        itemnewform.destroy()
        ResetAllEntries()
        InventoryReset()
    else:
        RESULT.set("Enter details")
    
    

#========================================BUTTONS FOR USER VIEW===================================

def UserSearch():
    if SEARCH.get() != "":
        usertree.delete(*usertree.get_children())
        Database(SECTION.get())
        cursor.execute(f"SELECT * FROM UserInfo WHERE FirstName LIKE '%{SEARCH.get()}% and Section = '{SECTION.get()}''")
        fetch = cursor.fetchall()
        for data in fetch:
            usertree.insert('', 'end', values=(data))
        cursor.close()
        conn.close()

def UserReset():
    usertree.delete(*usertree.get_children())
    UserDisplayData()
    SEARCH.set("")

def UserDelete():
    if not usertree.selection():
       print("ERROR")
    else:
        result = tkMessageBox.askquestion('Inventory Management System', 'Are you sure you want to delete this record?', icon="warning")
        if result == 'yes':
            curItem = usertree.focus()
            contents =(usertree.item(curItem))
            selecteditem = contents['values']
            usertree.delete(curItem)
            Database(SECTION.get())
            cursor.execute(f"DELETE FROM UserInfo WHERE IndexId = {selecteditem[0]} and Section = '{SECTION.get()}'")
            conn.commit()
            cursor.close()
            conn.close()


#========================================BUTTONS FOR LOG VIEW===================================

def Search():
    if SEARCH.get() != "":
        tree.delete(*tree.get_children())
        Database(SECTION.get())
        cursor.execute(f"SELECT * FROM LogTableInfo WHERE Name LIKE '%{SEARCH.get()}%' and Section = '{SECTION.get()}'")
        fetch = cursor.fetchall()
        for data in fetch:
            tree.insert('', 'end', values=(data))
        cursor.close()
        conn.close()

def Reset():
    tree.delete(*tree.get_children())
    COMBOBOX.set("All")
    DisplayData()
    SEARCH.set("")


def ShowLogView():
    global logform
    logform = Toplevel()
    logform.title("Inventory Management System / View Logs")
    width = 1024
    height = 520
    screen_width = Home.winfo_screenwidth()
    screen_height = Home.winfo_screenheight()
    x = (screen_width/2) - (width/2)
    y = (screen_height/2) - (height/2)
    logform.geometry("%dx%d+%d+%d" % (width, height, x, y))
    logform.resizable(True, True)
    LogForm()


def ShowUserView():
    global userform
    userform = Toplevel()
    userform.title("Inventory Management System / View users")
    width = 600
    height = 500
    screen_width = Home.winfo_screenwidth()
    screen_height = Home.winfo_screenheight()
    x = (screen_width/2) - (width/2)
    y = (screen_height/2) - (height/2)
    userform.geometry("%dx%d+%d+%d" % (width, height, x, y))
    userform.resizable(True, True)
    UserForm()


def ShowInventoryView():
    global inventoryform
    inventoryform = Toplevel()
    inventoryform.title("Inventory Management System / View items")
    width = 1024
    height = 520
    screen_width = Home.winfo_screenwidth()
    screen_height = Home.winfo_screenheight()
    x = (screen_width/2) - (width/2)
    y = (screen_height/2) - (height/2)
    inventoryform.geometry("%dx%d+%d+%d" % (width, height, x, y))
    inventoryform.resizable(True, True)
    InventoryForm()

def ViewSection():
    global sectionform
    sectionform = Toplevel()
    sectionform.title("Inventory Management System / View sections")
    width = 520
    height = 300
    screen_width = Home.winfo_screenwidth()
    screen_height = Home.winfo_screenheight()
    x = (screen_width/2) - (width/2)
    y = (screen_height/2) - (height/2)
    sectionform.geometry("%dx%d+%d+%d" % (width, height, x, y))
    sectionform.resizable(True, True)
    SectionForm()

def SectionSelectDatabase():
    global conn, cursor
    conn = sqlite3.connect("Sections.db")
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS SectionInfo (IndexId INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, Section TEXT)")
    conn.commit()
    
def CreateNewSection():
    global newsection, New_section
    newsection = Toplevel()
    newsection.title("Inventory Management System / Create new section")
    width =Home.winfo_screenwidth()/2
    height = Home.winfo_screenheight()/2
    screen_width = Home.winfo_screenwidth()
    screen_height = Home.winfo_screenheight()
    x = (screen_width/2) - (width/2)
    y = (screen_height/2) - (height/2)
    newsection.geometry("%dx%d+%d+%d" % (width, height, x, y))
    newsection.resizable(0, 0)
    TopNewSection = Frame(newsection, width=600, height=100, bd=1, relief=SOLID)
    TopNewSection.pack(side=TOP, pady=10)
    MidNewSection = Frame(newsection, width=600)
    MidNewSection.pack(side=TOP, pady=10)
    lbl_text = Label(TopNewSection, text="New section", font=('arial', 14), width=600)
    lbl_text.pack(fill=X)
    lbl_sectionname = Label(MidNewSection, text="Section name:", font=('arial', 12), bd=10)
    lbl_sectionname.grid(row=0, sticky=W)
    lbl_result = Label(MidNewSection, textvariable=RESULT, font=('arial', 8), bd=10, fg="red")
    lbl_result.grid(row=2, columnspan = 2)
    New_section = StringVar()
    sectionname = Entry(MidNewSection, textvariable = New_section, font=('arial', 12), width=15)
    sectionname.grid(row=0, column=1)
    btn_add = Button(MidNewSection, text="Save", font=('arial', 10), width=30, bg="#009ACD", command=SectionNew)
    btn_add.grid(row=13, columnspan=2, pady=10)

def SectionNew():
    SectionSelectDatabase()
    if New_section.get() is None:
        RESULT.set("Section name not entered.")
        return
    cursor.execute(f"INSERT INTO SectionInfo (Section) VALUES('{New_section.get()}')")
    conn.commit()
    cursor.close()
    conn.close()
    New_section.set("")
    RESULT.set("Created successfully")

#Home page details
Title = Frame(Home, bd=1, relief=SOLID)
Title.pack(pady=10)
lbl_display = Label(Title, text="Inventory Management System", font=('arial', 20))
lbl_display.pack()
menubar = Menu(Home)
filemenu1 = Menu(menubar, tearoff=0)
filemenu2 = Menu(menubar, tearoff=0)
filemenu3 = Menu(menubar, tearoff=0)
filemenu4 = Menu(menubar, tearoff=0)
filemenu5 = Menu(menubar, tearoff=0)
filemenu6 = Menu(menubar, tearoff=0)
filemenu1.add_command(label="Issue", command=ShowIssueItem)
filemenu1.add_command(label="Return", command=ShowReturnItem)
filemenu1.add_command(label="Log", command=ShowLogView)
filemenu2.add_command(label="New user", command=ShowUserNew)
filemenu2.add_command(label="Users", command=ShowUserView)
filemenu3.add_command(label="New item", command=ShowItemNew)
filemenu3.add_command(label="Item", command=ShowInventoryView)
filemenu4.add_command(label="Print item details", command=PrintInventoryDetails)
filemenu5.add_command(label="New section", command=CreateNewSection)
filemenu5.add_command(label="Sections", command=ViewSection)

#Call section database 
SectionSelectDatabase()
cursor.execute("SELECT Section FROM SectionInfo")
fetch = cursor.fetchall()

#Create a list and attach it to the radio button
SectionList = ["{}".format(data[0]) for data in fetch]
cursor.close()
conn.close()

#adding dropdown option for buttons
menubar.add_cascade(label="Log", menu=filemenu1)
menubar.add_cascade(label="Users", menu=filemenu2)
menubar.add_cascade(label="Items", menu=filemenu3)
menubar.add_cascade(label="Print", menu=filemenu4)
menubar.add_cascade(label="Section", menu=filemenu5)

#Section list options
label_listofsections = Label(Home, text="Select section: ")
label_listofsections.pack()
listofsections = ttk.Combobox(Home, values=SectionList, textvariable=SECTION)
listofsections.pack()

Home.config(menu=menubar)
Home.config(bg="#6666ff")


#========================================INITIALIZATION===================================
if __name__ == '__main__':
    Home.mainloop()