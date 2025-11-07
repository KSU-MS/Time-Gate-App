import customtkinter
import serial
import serial.tools.list_ports
import time
global cancel
cancel = False
#checking what ports are available
ports = serial.tools.list_ports.comports()
for port in ports:
    print(f"Port: {port.device} \nDescription: {port.description}")

#---------------------------------Command Definitions---------------------------------

#Read COM Port Button logic
def button1_callback():
    print("button 1 was pressed")
    COMLable.configure(text="")
    comPorts = ["Select Your Port"]
    for port in ports:
        currentText = COMLable.cget("text")
        newText = currentText + f"Port: {port.device}\nDescription: {port.description}\n\n"
        COMLable.configure(text=newText)
        comPorts.append(str(port.device))
        #print(comPorts) #Debug
    comSelectionBox.configure(values = comPorts)

def selectPort(choice):
    global selectedPort
    selectedPort = choice
    #print(selectedPort) #Debug
    return

#Button 1 (IM PRETTY SURE THIS DEF CAN BE DELEATED BUT I WILL LEAVE UNTIL AFTER FURTHER TESTING)
def loop_1():
    mainApp.counter += 1
    print("Hello World")
    mainApp.serial_data = ser.read(size=8)#.decode('utf-8').strip()    
    if mainApp.serial_data:  # Only process if data is received
        print(f"Received: {mainApp.serial_data}")
    COMLable2.configure(text=mainApp.serial_data)
    #COMLable2.configure(text=mainApp.counter)
    #insert code for loop here
    mainApp.after_id = mainApp.after(1, loop_1)

#Loops
def loopy1(): 
    ser = serial.Serial(
    port=selectedPort,
    baudrate=9600,  
    bytesize=serial.SEVENBITS,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    timeout=1)  # Timeout in seconds. None means wait forever.
    try:
        if ser.is_open:
            global serial_data
            print("Serial port opened successfully.")
            serial_data = ser.read(size=8)#.decode('utf-8').strip()

            if serial_data:  # Only process if data is received
                print(f"Received: {serial_data}")
                COMLable2.configure(text=serial_data)
        else:
            print("Failed to open serial port.")

    except serial.SerialException as e:
        print(f"Serial port error: {e}")
    except KeyboardInterrupt:
        print("Program terminated by user.")
    finally:
        if ser.is_open:
            ser.close()
            #print("Serial port closed.")
    if cancel != True:
        mainApp.after(3, loopy2)
    
def loopy2():
    global ser
    global cancel
    mainApp.after(3, loopy1)

#Button 2
def start_button():
    global cancel
    cancel = False
    mainApp.after(3, loopy1)

#Button 3
def cancel_button():
    global cancel
    cancel = True

#Button 4
def clipboard_button_callback():
    mainApp.clipboard_clear()
    mainApp.clipboard_append(serial_data)
    mainApp.update()

#App Start
mainApp = customtkinter.CTk()
mainApp.title("Timing Gates App V1")
mainApp.geometry("1200x600")
customtkinter.set_default_color_theme("green")

#Global Variables
mainApp.after_id = None
mainApp.counter = 0
mainApp.serial_data = 0

#---------------------------------Tab Creation---------------------------------

#Setting Tabs 
my_tab = customtkinter.CTkTabview(mainApp,
    width=1200,
    height=600
)
my_tab.pack(pady = 10)

#Calling Tabs
tab_1 = my_tab.add("Select Port")
tab_2 = my_tab.add("Data Read")

#---------------------------------Button Creation---------------------------------

#Read COM Port Button Creation
button1 = customtkinter.CTkButton(tab_1, text="Read COM Ports", command=button1_callback)
button1.pack(pady=10)

#Com Port Drop Box Creation
comPorts = ["Select Your Port"]
comSelectionBox = customtkinter.CTkComboBox(tab_1, values=comPorts, command= selectPort)
comSelectionBox.pack(pady=10)

#COM Port Selector Creation
COMLable = customtkinter.CTkLabel(tab_1, text="").pack(pady=10)

#Readout Buttons
button2 = customtkinter.CTkButton(tab_2, text="Start", command=start_button).pack(pady=10)

button3 = customtkinter.CTkButton(tab_2, text="Stop", command=cancel_button).pack(pady=10)

#Tab 2 readout
COMLable1 = customtkinter.CTkLabel(tab_2, font=("arial", 30, "bold"), text="Readout")
COMLable1.pack(pady=1)

COMLable2 = customtkinter.CTkLabel(tab_2, font=("arial", 30, "bold"), text="")
COMLable2.pack(pady = 10)

button4 = customtkinter.CTkButton(tab_2, text="Copy to clipboard", command=clipboard_button_callback).pack(pady=10)

#COMLable2 = customtkinter.CTkLabel(tab_2, text="")
#COMLable2.pack(pady = 10)

#Loop Start
mainApp.mainloop() 