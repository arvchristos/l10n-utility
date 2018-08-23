#!/usr/bin/env python
# -*- coding: utf-8 -*-
#title           :menu.py
#description     :This program displays an interactive menu on CLI
#author          :
#date            :
#version         :0.1
#usage           :python menu.py
#notes           :
#python_version  :2.7.6  
#=======================================================================
 
# Import the modules needed to run the script.
import sys, os
import argparse
import zipfile
import subprocess

# Argument parsing

parser = argparse.ArgumentParser(description='Localize LibreOffice extension')
parser.add_argument('extension', metavar='E', type=argparse.FileType('r'),
                   help='an .oxt extension for l10n')

parser.add_argument('locale', metavar='L', type=str,
                   help='Locale code')

args = parser.parse_args()

# Unzip our extension in current directory
zip_ref = zipfile.ZipFile(args.extension, 'r')
zip_ref.extractall("./"+ os.path.basename(args.extension.name) + "_extracted/")

new_locale = args.locale

# Main definition - constants
menu_actions  = {}  
 
# =======================
#     MENUS FUNCTIONS
# =======================
 
# Main menu
def main_menu():
    os.system('clear')
    
    print "Welcome to LO extension l10n utility,\n"
    print "Choose extension part to localize:"
    print "1. User Interface (UI)"
    print "2. Help pages"
    print "3. Legal"
    print "4. Extension Description"
    print "5. Compile localized extension"
    print "\n0. Quit"
    choice = raw_input(" >>  ")
    exec_menu(choice)
 
    return
 
# Execute menu
def exec_menu(choice):
    os.system('clear')
    ch = choice.lower()
    if ch == '':
        menu_actions['main_menu']()
    else:
        try:
            menu_actions[ch]()
        except KeyError:
            print "Invalid selection, please try again.\n"
            menu_actions['main_menu']()
    return
 
# UI l10n
def menu1():
    print "User interface l10n\n"
    wd = os.getcwd()
    os.chdir("./"+ os.path.basename(args.extension.name) + "_extracted/python/")
    subprocess.call("$(locate pygettext.py 2>&1 | head -n 1) -d base -o ./locales/base.pot ./main.py", shell=True)

    # There should be the edit from Poedit

    subprocess.call("mkdir -p locales/"+new_locale+"/LC_MESSAGES",shell=True)

    print "Save file as locales/"+new_locale+"/LC_MESSAGES/base.po using poedit:"

    subprocess.call("cp ./locales/base.pot ./locales/"+new_locale+"/LC_MESSAGES/base.po",shell=True)
    subprocess.call("poedit ./locales/"+new_locale+"/LC_MESSAGES/base.po >/dev/null 2>&1",shell=True)
    os.chdir(wd)

    print "9. Back"
    print "0. Quit"
    choice = raw_input(" >>  ")
    exec_menu(choice)
    return
 
 
# Help pages
def menu2():
    print "Help pages l10n\n"
    wd = os.getcwd()

    subprocess.call("mkdir -p ./"+ os.path.basename(args.extension.name) + "_extracted/help/"+new_locale+"/com.addon.pagenumbering/",shell=True)

    # l10n on pages
    subprocess.call("itstool -i rules.its -o base.pot ./"+ os.path.basename(args.extension.name) + "_extracted/help/en/com.addon.pagenumbering/Page01.xhp", shell=True)    
    
    print "Save file in current directory as base.po using poedit"
    subprocess.call("cp ./base.pot ./base.po",shell=True)
    subprocess.call("poedit ./base.po >/dev/null 2>&1",shell=True)

    subprocess.call("itstool -m base.mo -o ./"+ os.path.basename(args.extension.name) + "_extracted/help/"+new_locale+"/com.addon.pagenumbering/ ./"+ os.path.basename(args.extension.name) + "_extracted/help/en/com.addon.pagenumbering/Page01.xhp",shell=True)    

    # l10n on help tree

    subprocess.call("itstool -i rules.its -o base.pot ./"+ os.path.basename(args.extension.name) + "_extracted/help/en/help.tree", shell=True)    
    
    print "Save file in current directory as base.po using poedit"
    subprocess.call("cp ./base.pot ./base.po",shell=True)
    subprocess.call("poedit ./base.po >/dev/null 2>&1",shell=True)

    subprocess.call("itstool -m base.mo -o ./"+ os.path.basename(args.extension.name) + "_extracted/help/"+new_locale+"/ ./"+ os.path.basename(args.extension.name) + "_extracted/help/en/help.tree",shell=True)
    print "9. Back"
    print "0. Quit" 
    choice = raw_input(" >>  ")
    exec_menu(choice)
    return

# License l10n
def menu3():
    print "License l10n\n"

    subprocess.call("cp ./"+ os.path.basename(args.extension.name) + "_extracted/Legal/license-en.txt ./"+ os.path.basename(args.extension.name) + "_extracted/Legal/license-"+new_locale+".txt",shell=True)

    #open file and edit using the default editor
    subprocess.call("${EDITOR:-vi} ./"+ os.path.basename(args.extension.name) + "_extracted/Legal/license-"+new_locale+".txt",shell=True)

    # Update description.xml
    with open("./"+ os.path.basename(args.extension.name) + "_extracted/description.xml", "r") as in_file:
        buf = in_file.readlines()

    with open("./"+ os.path.basename(args.extension.name) + "_extracted/description.xml", "w") as out_file:
        for line in buf:
            if line == "      </simple-license>\n":
                line = "         <license-text xlink:href=\"Legal/license-"+new_locale+".txt\" lang=\""+new_locale+"\" />\n" + line
            out_file.write(line)


    print "9. Back"
    print "0. Quit" 
    choice = raw_input(" >>  ")
    exec_menu(choice)
    return

# Extension Description l10n
def menu4():
    print "Extension Description l10n\n"

    subprocess.call("cp ./"+ os.path.basename(args.extension.name) + "_extracted/Descriptions/descr-en.txt ./"+ os.path.basename(args.extension.name) + "_extracted/Descriptions/descr-"+new_locale+".txt",shell=True)

    #open file and edit using the default editor
    subprocess.call("${EDITOR:-vi} ./"+ os.path.basename(args.extension.name) + "_extracted/Descriptions/descr-"+new_locale+".txt",shell=True)

    # Update description.xml
    with open("./"+ os.path.basename(args.extension.name) + "_extracted/description.xml", "r") as in_file:
        buf = in_file.readlines()

    with open("./"+ os.path.basename(args.extension.name) + "_extracted/description.xml", "w") as out_file:
        for line in buf:
            if line == "   </extension-description>\n":
                line = "      <src xlink:href=\"Descriptions/descr-"+new_locale+".txt\" lang=\""+new_locale+"\" />\n" + line
            out_file.write(line)

    print "9. Back"
    print "0. Quit" 
    choice = raw_input(" >>  ")
    exec_menu(choice)
    return

# Compile localized extension
def menu5():
    print "Compile localized extension\n"

    #zip_folder(r'./'+ os.path.basename(args.extension.name) + '_extracted/',
    #           r'./ext_new.oxt')

    wd = os.getcwd()
    os.chdir("./"+ os.path.basename(args.extension.name) + "_extracted/")

    subprocess.call("mkdir  ../l10n_translated",shell=True)    
    subprocess.call("zip -r ../l10n_translated/"+os.path.basename(args.extension.name) +" ./*",shell=True)    
    
    os.chdir(wd)
    print "9. Back"
    print "0. Quit" 
    choice = raw_input(" >>  ")
    exec_menu(choice)
    return
 
# Back to main menu
def back():
    menu_actions['main_menu']()
 
# Exit program
def exit():
    sys.exit()
 
# =======================
#    MENUS DEFINITIONS
# =======================
 
# Menu definition
menu_actions = {
    'main_menu': main_menu,
    '1': menu1,
    '2': menu2,
    '3': menu3,
    '4': menu4,
    '5': menu5,
    '9': back,
    '0': exit,
}
 
# =======================
#      MAIN PROGRAM
# =======================
 
# Main Program
if __name__ == "__main__":
    # Launch main menu
    main_menu()
