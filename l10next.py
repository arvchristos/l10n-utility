#!/usr/bin/env python

import sys, os
import argparse
import zipfile
import subprocess
import re

# Argument parsing
parser = argparse.ArgumentParser(description='Localize LibreOffice extension')
parser.add_argument('extension', metavar='E', type=argparse.FileType('r'),
                   help='an .oxt extension for l10n')

parser.add_argument('locale', metavar='L', type=str,
                   help='Locale code')

args = parser.parse_args()

# Unzip our extension in current directory
# check if there is unfinished work
if os.path.isdir("./"+ os.path.basename(args.extension.name) + "_extracted/"):
    pass
else:
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


    # check if there is an unfinished translation
    if os.path.isfile("./locales/"+new_locale+"/LC_MESSAGES/base.po"):
        pass
    else:

        # generate newest pot template file
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

    # create directory for help pages pot files
    subprocess.call("mkdir -p ./"+ os.path.basename(args.extension.name) + "_help_pages_"+new_locale+"/pages/",shell=True)
    subprocess.call("mkdir -p ./"+ os.path.basename(args.extension.name) + "_help_pages_"+new_locale+"/tree/",shell=True)

    subprocess.call("mkdir -p ./"+ os.path.basename(args.extension.name) + "_extracted/help/"+new_locale+"/com.addon.pagenumbering/",shell=True)

    # check if pot file for help pages already exists
    
    if os.path.isfile("./"+ os.path.basename(args.extension.name) + "_help_pages_"+new_locale+"/pages/base.po"):
        pass
    else:
        # l10n on pages
        subprocess.call("itstool -i rules.its -o base.pot ./"+ os.path.basename(args.extension.name) + "_extracted/help/en/com.addon.pagenumbering/Page01.xhp", shell=True)    
        
        print "Save file in current directory as base.po using poedit"
        subprocess.call("cp ./base.pot ./"+ os.path.basename(args.extension.name) + "_help_pages_"+new_locale+"/pages/base.po",shell=True)
    
    subprocess.call("poedit ./"+ os.path.basename(args.extension.name) + "_help_pages_"+new_locale+"/pages/base.po >/dev/null 2>&1",shell=True)

    subprocess.call("itstool -m ./"+ os.path.basename(args.extension.name) + "_help_pages_"+new_locale+"/pages/base.mo -o ./"+ os.path.basename(args.extension.name) + "_extracted/help/"+new_locale+"/com.addon.pagenumbering/ ./"+ os.path.basename(args.extension.name) + "_extracted/help/en/com.addon.pagenumbering/Page01.xhp",shell=True)    

    

    if os.path.isfile("./"+ os.path.basename(args.extension.name) + "_help_pages_"+new_locale+"/tree/base.po"):
        pass
    else:
        # l10n on help tree
        subprocess.call("itstool -i rules.its -o base.pot ./"+ os.path.basename(args.extension.name) + "_extracted/help/en/help.tree", shell=True)    
        
        print "Save file in current directory as base.po using poedit"
        subprocess.call("cp ./base.pot ./"+ os.path.basename(args.extension.name) + "_help_pages_"+new_locale+"/tree/base.po",shell=True)
    
    subprocess.call("poedit ./"+ os.path.basename(args.extension.name) + "_help_pages_"+new_locale+"/tree/base.po >/dev/null 2>&1",shell=True)

    subprocess.call("itstool -m ./"+ os.path.basename(args.extension.name) + "_help_pages_"+new_locale+"/tree/base.mo -o ./"+ os.path.basename(args.extension.name) + "_extracted/help/"+new_locale+"/ ./"+ os.path.basename(args.extension.name) + "_extracted/help/en/help.tree",shell=True)

    print "9. Back"
    print "0. Quit" 
    choice = raw_input(" >>  ")
    exec_menu(choice)
    return

# License l10n
def menu3():
    print "License l10n\n"

    # check if there is unfinished content. If so load it

    if os.path.isfile("./"+ os.path.basename(args.extension.name) + "_extracted/Legal/license-" + new_locale + ".txt"):
        pass
    else:
        subprocess.call("cp ./"+ os.path.basename(args.extension.name) + "_extracted/Legal/license-en.txt ./"+ os.path.basename(args.extension.name) + "_extracted/Legal/license-"+new_locale+".txt",shell=True)

    #open file and edit using the default editor
    subprocess.call("${EDITOR:-vi} ./"+ os.path.basename(args.extension.name) + "_extracted/Legal/license-"+new_locale+".txt",shell=True)

    # Update description.xml
    with open("./"+ os.path.basename(args.extension.name) + "_extracted/description.xml", "r") as in_file:
        text = in_file.read()
        if re.search(r" +<license-text\sxlink:href=\"Legal/license-"+ new_locale +r"\.txt\"\slang=\""+new_locale+r"\"\s/>", text):
            pass
        else:
            in_file.seek(0)
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

    if os.path.isfile("./"+ os.path.basename(args.extension.name) + "_extracted/Descriptions/descr-"+new_locale+".txt"):
        pass
    else:
        subprocess.call("cp ./"+ os.path.basename(args.extension.name) + "_extracted/Descriptions/descr-en.txt ./"+ os.path.basename(args.extension.name) + "_extracted/Descriptions/descr-"+new_locale+".txt",shell=True)

    #open file and edit using the default editor
    subprocess.call("${EDITOR:-vi} ./"+ os.path.basename(args.extension.name) + "_extracted/Descriptions/descr-"+new_locale+".txt",shell=True)

    # Update description.xml
    with open("./"+ os.path.basename(args.extension.name) + "_extracted/description.xml", "r") as in_file:
        text = in_file.read()
        if re.search(r" +<src\sxlink:href=\"Descriptions/descr-"+new_locale+r"\.txt\"\slang=\""+new_locale+r"\"/>", text):
            pass
        else:
            in_file.seek(0)
            buf = in_file.readlines()
            with open("./"+ os.path.basename(args.extension.name) + "_extracted/description.xml", "w") as out_file:
                for line in buf:
                    if line == "   </extension-description>\n":
                        line = "      <src xlink:href=\"Descriptions/descr-"+new_locale+".txt\" lang=\""+new_locale+"\"/>\n" + line
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
