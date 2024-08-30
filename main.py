import os
import subprocess
from time import sleep
from colorama import Fore

def check_adb():
    try:
        subprocess.run(['.\\platform-tools\\adb.exe', 'disconnect'], creationflags=subprocess.CREATE_NO_WINDOW)
        devices = ((subprocess.run(['.\\platform-tools\\adb.exe', 'devices'], stdout=subprocess.PIPE, text=True)).stdout.strip()).split("\n")
        if len(devices) < 2:
            return False
        else:
            return True
    except FileNotFoundError:
        return False

def get_device(str):
    subprocess.run(['.\\platform-tools\\adb.exe', 'disconnect'], creationflags=subprocess.CREATE_NO_WINDOW)
    if str == "ip":
        sleep(2)
        wlan0 = ((subprocess.run(['.\\platform-tools\\adb.exe', 'shell', 'ip', '-f', 'inet', 'addr', 'show', 'wlan0'], creationflags=subprocess.CREATE_NO_WINDOW, stdout=subprocess.PIPE, text=True)).stdout).split("\n")
        for line in wlan0:
            if 'inet' in line:
                return f"{(line.split()[1]).split("/")[0]}"
    elif str == "info":
        try:
            brand = (subprocess.run(['.\\platform-tools\\adb.exe', 'shell', 'getprop', 'ro.product.brand'], creationflags=subprocess.CREATE_NO_WINDOW, stdout=subprocess.PIPE, text=True)).stdout.strip()
            model = (subprocess.run(['.\\platform-tools\\adb.exe', 'shell', 'getprop', 'ro.product.model'], creationflags=subprocess.CREATE_NO_WINDOW, stdout=subprocess.PIPE, text=True)).stdout.strip()
            return (brand if brand else False), (model if model else False)
        except FileNotFoundError:
            return "Unknown (ADB is not installed)", "Unknown (ADB is not installed)"

def adb_connect(ip):
    sleep(1)
    subprocess.run(['.\\platform-tools\\adb.exe', 'connect', f'{ip}'], creationflags=subprocess.CREATE_NO_WINDOW)
    subprocess.run(['.\\platform-tools\\adb.exe', 'tcpip', f'5555'], creationflags=subprocess.CREATE_NO_WINDOW)
    devices = (subprocess.run(['.\\platform-tools\\adb.exe', 'devices'], stdout=subprocess.PIPE, text=True)).stdout.strip()
    if f'{ip}:5555' in devices:
        return True
    else:
        return False
    
def device_status():
    subprocess.run(['.\\platform-tools\\adb.exe', 'disconnect'], creationflags=subprocess.CREATE_NO_WINDOW)
    devices = ((subprocess.run(['.\\platform-tools\\adb.exe', 'devices'], creationflags=subprocess.CREATE_NO_WINDOW, stdout=subprocess.PIPE, text=True)).stdout.strip()).split("\n")
    if len(devices) < 2:
        return False
    elif "device" in devices[1]:
        return True
    elif "unauthorized" in devices[1]:
        return "Unauthorized"

def main():
    while True:
        os.system("cls")
        print("""{}
                                    ______  _       _
                                    |  ___|(_)     | |
                                    | |_    _  ___ | |_  ___
                                    |  _|  | |/ __|| __|/ __|
                                    | |    | |\\__ \\| |_ \\__ \\
                                    \\_|    |_||___/ \\__||___/
{}
  ___              _               _      _  ___  ___                             _  _         _                
 / _ \\            | |             (_)    | | |  \\/  |                            (_)| |       | |               
/ /_\\ \\ _ __    __| | _ __   ___   _   __| | | .  . |  __ _  _ __   _   _  _ __   _ | |  __ _ | |_   ___   _ __ 
|  _  || '_ \\  / _` || '__| / _ \\ | | / _` | | |\\/| | / _` || '_ \\ | | | || '_ \\ | || | / _` || __| / _ \\ | '__|
| | | || | | || (_| || |   | (_) || || (_| | | |  | || (_| || | | || |_| || |_) || || || (_| || |_ | (_) || |   
\\_| |_/|_| |_| \\__,_||_|    \\___/ |_| \\__,_| \\_|  |_/ \\__,_||_| |_| \\__,_|| .__/ |_||_| \\__,_| \\__| \\___/ |_|   
                                                                          | |                                   
                                                                          |_|                                   

    """.format(Fore.WHITE, Fore.LIGHTCYAN_EX))
        try:
            brand, model = get_device("info")
            if brand == False or model == False:
                os.system("cls")
                print(Fore.LIGHTRED_EX + "The USB device is disconnected. Check your USB connection and try again." + Fore.RESET)
                break
            menu = int(input(Fore.WHITE + "   Brand: " + Fore.LIGHTYELLOW_EX + f"{brand}" + Fore.WHITE + "\n   Model: " + Fore.LIGHTYELLOW_EX + f"{model}" + Fore.GREEN + "\n\n   1) Android Screen Sharing (USB)\n   2) Android Screen Sharing (Wireless)\n   3) Run ADB Commands\n\n   9) Exit the program." + Fore.WHITE + "\n\n   => "))
        except ValueError:
            os.system("cls")
            print(Fore.LIGHTRED_EX + "Unexpected input. Please respond using only numbers.\nYou're being redirected...")
            sleep(3)
            continue
        except KeyboardInterrupt:
            os.system("taskkill -f -im adb.exe")
            os.system("cls")
            print(Fore.LIGHTGREEN_EX + "'CTRL + C' combination detected. Program will be closed..." + Fore.RESET)
            sleep(3)
            break
        if menu == 1:
            os.system("cls")
            print(Fore.LIGHTBLUE_EX + "Trying to communicate with the android device...")
            sleep(2)
            status = device_status()
            if status == True:
                print(Fore.LIGHTGREEN_EX + "Device found! Connecting...")
                subprocess.run(".\\platform-tools\\scrcpy.exe", creationflags=subprocess.CREATE_NO_WINDOW)
                continue
            elif status == "Unauthorized":
                print(Fore.LIGHTYELLOW_EX + "Try again after confirming the checkbox on the screen of the android device.\nYou're being redirected...")
                sleep(5)
                continue
            else:
                print(Fore.LIGHTRED_EX + "Device not found. Check your USB connection and try again." + Fore.RESET)
                break
        if menu == 2:
            os.system("cls")
            print(Fore.LIGHTBLUE_EX + "Trying to communicate with the android device's in the cache...")
            sleep(2)
            with open("last_wireless_device.txt", "r") as file:
                last_ip = file.read()
                if last_ip:
                    if adb_connect(last_ip) == True:
                        print(Fore.LIGHTGREEN_EX + "Connected to the device! Establishing communication...")
                        subprocess.run(['.\\platform-tools\\scrcpy.exe', '-e'], creationflags=subprocess.CREATE_NO_WINDOW)
                        continue
                    else:
                        if device_status() == True:
                            new_ip = get_device("ip")
                            if last_ip != new_ip:
                                with open("last_wireless_device.txt", "w") as new_save:
                                    new_save.write(new_ip)
                                if adb_connect(new_ip) == True:
                                    print(Fore.LIGHTGREEN_EX + "Connected to the device! Establishing communication...")
                                    subprocess.run(['.\\platform-tools\\scrcpy.exe', '-e'], creationflags=subprocess.CREATE_NO_WINDOW)
                                    continue
                                else:
                                    print(Fore.LIGHTRED_EX + "Something went wrong, your device cannot connect wirelessly. Please notify the developer. You're being redirected...")
                                    sleep(5)
                                    continue
                        elif device_status() == "Unauthorized":
                            print(Fore.LIGHTYELLOW_EX + "Try again after confirming the checkbox on the screen of the android device.\nYou're being redirected...")
                            sleep(5)
                            continue
                        else:
                            print(Fore.LIGHTYELLOW_EX + "Unable to establish a connection with your phone's IP address stored in cache. Please reconnect your phone via USB and try again.\nYou're being redirected...")
                            sleep(5)
                            continue
                else:
                    print(Fore.LIGHTYELLOW_EX + "Device found! Trying to establish communication...")
                    ip = get_device("ip")
                    with open("last_wireless_device.txt", "w") as new:
                        new.write(ip)
                    if adb_connect(ip) == True:
                        print(Fore.LIGHTGREEN_EX + "Connected to the device! Establishing communication...")
                        subprocess.run(['.\\platform-tools\\scrcpy.exe', '-e'], creationflags=subprocess.CREATE_NO_WINDOW)
                        continue
                    else:
                        print(Fore.LIGHTRED_EX + "Something went wrong, your device cannot connect wirelessly. Please notify the developer. You're being redirected...")
                        sleep(5)
                        continue
        if menu == 3:
            os.system("cls")
            print(Fore.LIGHTBLUE_EX + "Trying to communicate with the android device...")
            sleep(2)
            status = device_status()
            if status == True:
                print(Fore.LIGHTGREEN_EX + "Device found! Connecting...")
                sleep(3)
                os.system("cls")
                brand, model = get_device("info")
                print(Fore.LIGHTGREEN_EX + "\n\t\t\t\t\t  Android Debugging Bridge [ADB]\n" + Fore.LIGHTRED_EX + "\t  (REMEMBER, the developer (F1sts) is not responsible for any damage you do to your device from here!)\n\t\t\t\t\t     (USE AT YOUR OWN RISK!)\n" + Fore.LIGHTYELLOW_EX + "\n\t\t\t\t\t     (Type “!exit” to quit.)")
                adb_mode = True
                while adb_mode:
                    command = input(f"{Fore.WHITE}[{Fore.GREEN}{brand}{Fore.WHITE}] ({Fore.GREEN}{model}{Fore.WHITE}) | {os.getcwd()} => ")
                    if command == "cls" or command == "clear":
                        os.system("cls")
                        print(Fore.LIGHTGREEN_EX + "\n\t\t\t\t\t  Android Debugging Bridge [ADB]\n" + Fore.LIGHTRED_EX + "\t  (REMEMBER, the developer (F1sts) is not responsible for any damage you do to your device from here!)\n\t\t\t\t\t     (USE AT YOUR OWN RISK!)\n" + Fore.LIGHTYELLOW_EX + "\n\t\t\t\t\t     (Type “!exit” to quit.)")
                        continue
                    if command == "!exit":
                        adb_mode = False
                        continue
                    elif command.startswith("cd"):
                        try:
                            os.chdir(command[3:])
                        except FileNotFoundError:
                            print(f"{Fore.LIGHTRED_EX}Cannot find path {Fore.WHITE}'{command[3:]}'{Fore.LIGHTRED_EX} because it does not exist.")
                    os.system(f"{command.replace("adb", ".\\platform-tools\\adb.exe")}")
            elif status == "Unauthorized":
                print(Fore.LIGHTYELLOW_EX + "Try again after confirming the checkbox on the screen of the android device.\nYou're being redirected...")
                sleep(5)
                continue
            else:
                print(Fore.LIGHTRED_EX + "Device not found. Check your USB connection and try again." + Fore.RESET)
                break
        if menu == 9:
            os.system("taskkill -f -im adb.exe & cls")
            break

if __name__ == "__main__":
    if check_adb() == True:
        main()
    else:
        print(Fore.LIGHTRED_EX + "ADB is not installed or your device isn't connected properly. Please check your USB connection and make sure 'USB debugging' is turned on." + Fore.RESET)
