#! /usr/bin/env python3

__author__ = "Francesco Ripa"
__copyright__ = "Copyright © 2017"
__credits__ = ["Francesco Ripa"]
__license__ = "GPL"
__version__ = "0.4a"
__maintainer__ = "Francesco Ripa"
__email__ = "monkeesmart@gmail.com"
__status__ = "Pre-release"

#    A "Hide-n-Seek" Trial/Demo Framework
#
#    Copyright (C) 2017 Francesco Ripa
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.

#    _locale.enEN
#
#    Description:
#
#    The app starts loading path and safepath:
#
#    Path 1a + 1b --> data 1 + hash
#    Path 2a + 2b --> data 2 + hash
#    Path 3a + 3b --> data 3 + hash
#    Path 4a + 4b --> data 4 + hash
#    Safepath 1a + 1b --> data 5 + hash
#
#    Data = base85 == [YYYY-MM-DD, HH, appversion]
#    Hash = sha256 [data]
#
#    Path contains the address to the data stored under local files
#    Safepath is the only with random name, which is stored in the invisible file under Users/<utente>/.machine_id
#
#    When a valid <data> file is found, the content occurs and then prints to the output
#
#    If no file is found or its contents are corrupted, the process of generating or writing <data> content is initiated
#
#    Finally it prints the contents of all files created/available.
#
#    Notes:
#
#    In this version, some features that have already been developed and envisaged in the project have not been implemented as a result of GUI development

#    _locale.itIT
#
#    Descrizione:
#
#    L'app avvia il caricamento di path e safepath:
#
#    Path 1a + 1b --> data 1 + hash
#    Path 2a + 2b --> data 2 + hash
#    Path 3a + 3b --> data 3 + hash
#    Path 4a + 4b --> data 4 + hash
#    Safepath 1a + 1b --> data 5 + hash
#
#    Data = base85 == [YYYY-MM-DD, HH, appversion]
#    Hash = sha256 [data]
#
#    Path contiene l'indirizzo ai data salvati in file locali
#    Safepath é l'unico con nome casuale, memorizzato nel file invisibile sotto Utenti/<utente>/.machine_id
#
#    Quando viene trovato un file data valido, si verifica il contenuto e poi viene stampato in output
#
#    Nel caso non venga trovato nessun file o il suo contenuto sia illeggibile, si avviano i processi di generazione o scrittura del contenuto (data)
#
#    Infine si stampano i contenuti di tutti i file creati/disponibili.
#
#    Note:
#
#    In questa versione, non sono state implementate alcune funzionalità già sviluppate e previste nel progetto in seguito allo sviluppo del GUI

import base64
import hashlib
import os
import pwd
import random
import shutil
import time

print("""
A
    __    _     __                          __  
   / /_  (_)___/ /__  ____  ________  ___  / /__
  / __ \/ / __  / _ \/ __ \/ ___/ _ \/ _ \/ //_/
 / / / / / /_/ /  __/ / / (__  )  __/  __/ ,<   
/_/ /_/_/\__,_/\___/_/ /_/____/\___/\___/_/|_|  
                            Trial/Demo Framework
version 0.4 alpha, © 2017 Francesco Ripa

Please view this source to read License and DOC.

Notes: if 3 blank spaces are displayed below,
it means that <data> could be missing/corrupted.

Errors are always displayed for istance:
<files already exist> raise CREATION ERROR, etc.

""")

# LOGIN USERNAME

tmp_uid=pwd.getpwuid(os.getuid())[0]

# RANDOM INIT

rinit=random.random()
rinit=str(rinit).split('.')
rname_00="."+rinit[-1]
rinit=random.random()
rinit=str(rinit).split('.')
rname_01="."+rinit[-1]

# SAFEPATH INIT

print('[ READING AND CREATING SAFEPATH DATA...........]\n')
try:
    with open('/Users/'+tmp_uid+'/.machine_id', 'x') as f:
        print(rname_00+'\n'+rname_01, file=f)
        aname=open(f, 'r')
        aname=aname.read()
        print('SAFEPATH @/Users/'+tmp_uid+':\n' + aname) # (DELETE ME)
except OSError:
    print('\n//SAFEPATH FAILED @CREATION\n')
    try:
        aname=open('/Users/'+tmp_uid+'/.machine_id', 'r')
        aname=aname.read()
        print('SAFEPATH @/Users/'+tmp_uid+':\n' + aname)
    except OSError:
        print('\n//SAFEPATH FAILED @VERIFICATION\n')
        try:
            with open('/Users/'+tmp_uid+'/.machine_id', 'w') as f:
                print(rname_00+'\n'+rname_01, file=f)
                aname=open('/Users/'+tmp_uid+'/.machine_id', 'r')
                aname=aname.read()
                print('SAFEPATH @/Users/'+tmp_uid+':\n' + aname)
        except OSError:
            print('\n//SAFEPATH FAILED @MODIFICATION\n')
            try:
                aname=open('/Users/'+tmp_uid+'/.machine_id', 'r')
                aname=aname.read()
                print('SAFEPATH @/Users/'+tmp_uid+':\n' + aname)
            except OSError:
                print('\n//SAFEPATH FAILED @VERIFICATION\n')

# SAFEPATH DATA

aname=aname.split('\n')
rname_00=aname[0]
rname_01=aname[1]

# MAIN DATA

cryptdate=list(time.gmtime())
cryptdate=str(cryptdate[0])+"-"+str(cryptdate[1])+"-"+str(cryptdate[2])+"\n"+str(cryptdate[3])+"\n"+__status__

# CRYPT DATA

crypton=(base64.b85encode(bytes(cryptdate,"utf-8")))

# STDOUT STREAM

cryptdat=str(crypton, "utf-8")

# CRYPT REV

cryptln=len(cryptdat)
crypta0=cryptln/2
crypta1=str(crypta0).split(".")
cryptb0=int(crypta1[0])

# HASHED

crypths=hashlib.sha256(crypton).hexdigest()

# TEMP GEN

tmp_j0=cryptdat[:cryptb0]+crypths # (SPLIT 1)
tmp_j1=cryptdat[cryptb0:] # (SPLIT 2)
tmp_j2='#export DYLD_LIBRARY=/usr/lib'+cryptdat+crypths # (DUMMY + REAL)

# DECODE CHK (DELETE ME)

cryptoff=str((base64.b85decode(crypton)),"utf-8")

# PATHS (MUST BE ENCRYPTED)

tmp_00='/Users/'+tmp_uid+'/.bash_profile' # PART 1 !NO SPLIT
tmp_10='/Users/'+tmp_uid+'/Library/Application Support/Dock/.DS_Store '#        first part (SPLIT 1) -------------------- # PART 2
tmp_11='/Users/'+tmp_uid+'/Library/Application Support/AddressBook/.DS_Store '# -------------------- second one (SPLIT 2)
tmp_12='/Users/'+tmp_uid+'/Library/Application Support/iCloud/.DS_Store '# PART 3
tmp_22='/Users/'+tmp_uid+'/Library/Application Support/App Store/updatejournal.plist '
tmp_23='/Users/'+tmp_uid+'/Library/Preferences/ByHost/.DS_Store '# PART 4
tmp_33='/Users/'+tmp_uid+'/Library/Preferences/com.apple.internetconnect.plist '
tmp_34='/Users/'+tmp_uid+'/Library/Preferences/'+rname_00 # (SAFEPATH 1) # PART 5
tmp_44='/Users/'+tmp_uid+'/Library/Preferences/'+rname_01 # (SAFEPATH 2)

# LOTS { VERIFICATION | CREATION | MODIFICATION } (MUST BE ENCRYPTED)

for entry in os.scandir('/Users/'+tmp_uid):
    if entry.name.startswith('.bash_profile') and entry.is_file():
        try:
            print("\n[ READING AND CREATING TRIAL DATA..............]\n") # (DELETE ME)
            tmp_s0=open(tmp_00, 'r')
            tmp_b0=tmp_s0.read()
            tmp_d0=tmp_b0[-87:-65]
            tmp_dd=tmp_b0[-65:-1] #sha256
            tmp_bs=bytes(tmp_d0, "utf-8")
            tmp_f0=str((base64.b85decode(tmp_bs)),"utf-8")
            print('\n'+tmp_f0+"\n\n//VERIFICATION No.1\n") # (DELETE ME)
        except OSError:
            print("\n\n//VERIFICATION No.1 FAILED\n")
        except ValueError:
            print("\n\n//VERIFICATION No.1 FAILED\n")
    else:
        pass
try:
    with open(tmp_00, 'x') as f:
        print(tmp_j2, file=f)
        tmp_s0=open(tmp_00, 'r')
        tmp_b0=tmp_s0.read()
        tmp_d0=tmp_b0[-87:-65]
        tmp_dd=tmp_b0[-65:-1]
        tmp_bs=bytes(tmp_d0, "utf-8")
        tmp_f0=str((base64.b85decode(tmp_bs)),"utf-8")
        print('\n'+tmp_f0+"\n\n//VERIFICATION No.1\n")
except OSError:
    print("FILE No.1 FAILED @CREATION")
except ValueError:
    print("FILE No.1 FAILED @CREATION")
    try:
        with open(tmp_00, 'a') as f:
            print(tmp_j2, file=f)
            tmp_s0=open(tmp_00, 'r')
            tmp_b0=tmp_s0.read()
            tmp_d0=tmp_b0[-87:-65]
            tmp_dd=tmp_b0[-65:-1]
            tmp_bs=bytes(tmp_d0, "utf-8")
            tmp_f0=str((base64.b85decode(tmp_bs)),"utf-8")
            print('\n'+tmp_f0+"\n\n//VERIFICATION No.1\n")
    except OSError:
        print("FILE No.1 FAILED @MODIFICATION")
    except ValueError:
        print("FILE No.1 FAILED @MODIFICATION")
for entry in os.scandir('/Users/'+tmp_uid+'/Library/Application Support/Dock/') and os.scandir('/Users/'+tmp_uid+'/Library/Application Support/AddressBook/'):
    if entry.name.startswith('.DS_Store ') and entry.is_file():
        try:
            tmp_s0=open(tmp_10, 'r')
            tmp_s1=open(tmp_11, 'r')
            tmp_b0=tmp_s0.read()
            tmp_d0=tmp_b0[:-65]
            tmp_dd=tmp_b0[-65:-1]
            tmp_b1=tmp_s1.read()
            tmp_d1=tmp_b1[:-1]
            tmp_ss=(tmp_d0+tmp_d1)
            tmp_bs=bytes(tmp_ss, "utf-8")
            tmp_f0=str((base64.b85decode(tmp_bs)),"utf-8")
            print('\n'+tmp_f0+"\n\n//VERIFICATION No.2\n")
        except OSError:
            print("\n\n//VERIFICATION No.2 FAILED\n")
        except ValueError:
            print("\n\n//VERIFICATION No.2 FAILED\n")
    else:
        pass
try:
    with open(tmp_10, 'x') as f:
        print(tmp_j0, file=f)
        tmp_s0=open(tmp_10, 'r')
        tmp_s1=open(tmp_11, 'r')
        tmp_b0=tmp_s0.read()
        tmp_d0=tmp_b0[:-65]
        tmp_dd=tmp_b0[-65:-1]
        tmp_b1=tmp_s1.read()
        tmp_d1=tmp_b1[:-1]
        tmp_ss=(tmp_d0+tmp_d1)
        tmp_bs=bytes(tmp_ss, "utf-8")
        tmp_f0=str((base64.b85decode(tmp_bs)),"utf-8")
        print('\n'+tmp_f0+"\n\n//VERIFICATION No.2\n")
except OSError:
    print("FILE No.2a FAILED @CREATION")
except ValueError:
    print("FILE No.2a FAILED @CREATION")
    try:
        with open(tmp_10, 'w') as f:
            print(tmp_j0, file=f)
            tmp_s0=open(tmp_10, 'r')
            tmp_s1=open(tmp_11, 'r')
            tmp_b0=tmp_s0.read()
            tmp_d0=tmp_b0[:-65]
            tmp_dd=tmp_b0[-65:-1]
            tmp_b1=tmp_s1.read()
            tmp_d1=tmp_b1[:-1]
            tmp_ss=(tmp_d0+tmp_d1)
            tmp_bs=bytes(tmp_ss, "utf-8")
            tmp_f0=str((base64.b85decode(tmp_bs)),"utf-8")
            print('\n'+tmp_f0+"\n\n//VERIFICATION No.2\n")
    except OSError:
        print("FILE No.2a FAILED @MODIFICATION")
    except ValueError:
        print("FILE No.2a FAILED @MODIFICATION")
try:
    with open(tmp_11, 'x') as f:
        print(tmp_j1, file=f)
        tmp_s0=open(tmp_10, 'r')
        tmp_s1=open(tmp_11, 'r')
        tmp_b0=tmp_s0.read()
        tmp_d0=tmp_b0[:-65]
        tmp_dd=tmp_b0[-65:-1]
        tmp_b1=tmp_s1.read()
        tmp_d1=tmp_b1[:-1]
        tmp_ss=(tmp_d0+tmp_d1)
        tmp_bs=bytes(tmp_ss, "utf-8")
        tmp_f0=str((base64.b85decode(tmp_bs)),"utf-8")
        print('\n'+tmp_f0+"\n\n//VERIFICATION No.2\n")
except OSError:
    print("FILE No.2b FAILED @CREATION")
except ValueError:
    print("FILE No.2b FAILED @CREATION")
    try:
        with open(tmp_11, 'w') as f:
            print(tmp_j1, file=f)
            tmp_s0=open(tmp_10, 'r')
            tmp_s1=open(tmp_11, 'r')
            tmp_b0=tmp_s0.read()
            tmp_d0=tmp_b0[:-65]
            tmp_dd=tmp_b0[-65:-1]
            tmp_b1=tmp_s1.read()
            tmp_d1=tmp_b1[:-1]
            tmp_ss=(tmp_d0+tmp_d1)
            tmp_bs=bytes(tmp_ss, "utf-8")
            tmp_f0=str((base64.b85decode(tmp_bs)),"utf-8")
            print('\n'+tmp_f0+"\n\n//VERIFICATION No.2\n")
    except OSError:
        print("FILE No.2b FAILED @MODIFICATION")
    except ValueError:
        print("FILE No.2b FAILED @MODIFICATION")
for entry in os.scandir('/Users/'+tmp_uid+'/Library/Application Support/iCloud/') and os.scandir('/Users/'+tmp_uid+'/Library/Application Support/App Store/'):
    if entry.name.startswith('.DS_Store ' and 'updatejournal.plist ') and entry.is_file():
        try:
            tmp_s0=open(tmp_12, 'r')
            tmp_s1=open(tmp_22, 'r')
            tmp_b0=tmp_s0.read()
            tmp_d0=tmp_b0[:-65]
            tmp_dd=tmp_b0[-65:-1]
            tmp_b1=tmp_s1.read()
            tmp_d1=tmp_b1[:-1]
            tmp_ss=(tmp_d0+tmp_d1)
            tmp_bs=bytes(tmp_ss, "utf-8")
            tmp_f0=str((base64.b85decode(tmp_bs)),"utf-8")
            print('\n'+tmp_f0+"\n\n//VERIFICATION No.3\n")
        except OSError:
            print("\n\n//VERIFICATION No.3 FAILED\n")
        except ValueError:
            print("\n\n//VERIFICATION No.3 FAILED\n")
    else:
        pass
try:
    with open(tmp_12, 'x') as f:
        print(tmp_j0, file=f)
        tmp_s0=open(tmp_12, 'r')
        tmp_s1=open(tmp_22, 'r')
        tmp_b0=tmp_s0.read()
        tmp_d0=tmp_b0[:-65]
        tmp_dd=tmp_b0[-65:-1]
        tmp_b1=tmp_s1.read()
        tmp_d1=tmp_b1[:-1]
        tmp_ss=(tmp_d0+tmp_d1)
        tmp_bs=bytes(tmp_ss, "utf-8")
        tmp_f0=str((base64.b85decode(tmp_bs)),"utf-8")
        print('\n'+tmp_f0+"\n\n//VERIFICATION No.3\n")
except OSError:
    print("FILE No.3a FAILED @CREATION")
except ValueError:
    print("FILE No.3a FAILED @CREATION")
    try:
        with open(tmp_12, 'w') as f:
            print(tmp_j0, file=f)
            tmp_s0=open(tmp_10, 'r')
            tmp_s1=open(tmp_11, 'r')
            tmp_b0=tmp_s0.read()
            tmp_d0=tmp_b0[:-65]
            tmp_dd=tmp_b0[-65:-1]
            tmp_b1=tmp_s1.read()
            tmp_d1=tmp_b1[:-1]
            tmp_ss=(tmp_d0+tmp_d1)
            tmp_bs=bytes(tmp_ss, "utf-8")
            tmp_f0=str((base64.b85decode(tmp_bs)),"utf-8")
            print('\n'+tmp_f0+"\n\n//VERIFICATION No.3\n")
    except OSError:
        print("FILE No.3a FAILED @MODIFICATION")
    except ValueError:
        print("FILE No.3a FAILED @MODIFICATION")
try:
    with open(tmp_22, 'x') as f:
        print(tmp_j1, file=f)
        tmp_s0=open(tmp_12, 'r')
        tmp_s1=open(tmp_22, 'r')
        tmp_b0=tmp_s0.read()
        tmp_d0=tmp_b0[:-65]
        tmp_dd=tmp_b0[-65:-1]
        tmp_b1=tmp_s1.read()
        tmp_d1=tmp_b1[:-1]
        tmp_ss=(tmp_d0+tmp_d1)
        tmp_bs=bytes(tmp_ss, "utf-8")
        tmp_f0=str((base64.b85decode(tmp_bs)),"utf-8")
        print('\n'+tmp_f0+"\n\n//VERIFICATION No.3\n")
except OSError:
    print("FILE No.3b FAILED @CREATION")
except ValueError:
    print("FILE No.3b FAILED @CREATION")
    try:
        with open(tmp_22, 'w') as f:
            print(tmp_j1, file=f)
            tmp_s0=open(tmp_12, 'r')
            tmp_s1=open(tmp_22, 'r')
            tmp_b0=tmp_s0.read()
            tmp_d0=tmp_b0[:-65]
            tmp_dd=tmp_b0[-65:-1]
            tmp_b1=tmp_s1.read()
            tmp_d1=tmp_b1[:-1]
            tmp_ss=(tmp_d0+tmp_d1)
            tmp_bs=bytes(tmp_ss, "utf-8")
            tmp_f0=str((base64.b85decode(tmp_bs)),"utf-8")
            print('\n'+tmp_f0+"\n\n//VERIFICATION No.3\n")
    except OSError:
        print("FILE No.3b FAILED @MODIFICATION")
    except ValueError:
        print("FILE No.3b FAILED @MODIFICATION")
for entry in os.scandir('/Users/'+tmp_uid+'/Library/Preferences/ByHost/') and os.scandir('/Users/'+tmp_uid+'/Library/Preferences/'):
    if entry.name.startswith('.DS_Store ' and 'com.apple.internetconnect.plist ') and entry.is_file():
        try:
            tmp_s0=open(tmp_23, 'r')
            tmp_s1=open(tmp_33, 'r')
            tmp_b0=tmp_s0.read()
            tmp_d0=tmp_b0[:-65]
            tmp_dd=tmp_b0[-65:-1]
            tmp_b1=tmp_s1.read()
            tmp_d1=tmp_b1[:-1]
            tmp_ss=(tmp_d0+tmp_d1)
            tmp_bs=bytes(tmp_ss, "utf-8")
            tmp_f0=str((base64.b85decode(tmp_bs)),"utf-8")
            print('\n'+tmp_f0+"\n\n//VERIFICATION No.4\n")
        except OSError:
            print("\n\n//VERIFICATION No.4 FAILED\n")
        except ValueError:
            print("\n\n//VERIFICATION No.4 FAILED\n")
    else:
        pass
try:
    with open(tmp_23, 'x') as f:
        print(tmp_j0, file=f)
        tmp_s0=open(tmp_23, 'r')
        tmp_s1=open(tmp_33, 'r')
        tmp_b0=tmp_s0.read()
        tmp_d0=tmp_b0[:-65]
        tmp_dd=tmp_b0[-65:-1]
        tmp_b1=tmp_s1.read()
        tmp_d1=tmp_b1[:-1]
        tmp_ss=(tmp_d0+tmp_d1)
        tmp_bs=bytes(tmp_ss, "utf-8")
        tmp_f0=str((base64.b85decode(tmp_bs)),"utf-8")
        print('\n'+tmp_f0+"\n\n//VERIFICATION No.4\n")
except OSError:
    print("FILE No.4a FAILED @CREATION")
except ValueError:
    print("FILE No.4a FAILED @CREATION")
    try:
        with open(tmp_23, 'w') as f:
            print(tmp_j0, file=f)
            tmp_s0=open(tmp_23, 'r')
            tmp_s1=open(tmp_33, 'r')
            tmp_b0=tmp_s0.read()
            tmp_d0=tmp_b0[:-65]
            tmp_dd=tmp_b0[-65:-1]
            tmp_b1=tmp_s1.read()
            tmp_d1=tmp_b1[:-1]
            tmp_ss=(tmp_d0+tmp_d1)
            tmp_bs=bytes(tmp_ss, "utf-8")
            tmp_f0=str((base64.b85decode(tmp_bs)),"utf-8")
            print('\n'+tmp_f0+"\n\n//VERIFICATION No.4\n")
    except OSError:
        print("FILE No.4a FAILED @MODIFICATION")
    except ValueError:
        print("FILE No.4a FAILED @MODIFICATION")
try:
    with open(tmp_33, 'x') as f:
        print(tmp_j1, file=f)
        tmp_s0=open(tmp_23, 'r')
        tmp_s1=open(tmp_33, 'r')
        tmp_b0=tmp_s0.read()
        tmp_d0=tmp_b0[:-65]
        tmp_dd=tmp_b0[-65:-1]
        tmp_b1=tmp_s1.read()
        tmp_d1=tmp_b1[:-1]
        tmp_ss=(tmp_d0+tmp_d1)
        tmp_bs=bytes(tmp_ss, "utf-8")
        tmp_f0=str((base64.b85decode(tmp_bs)),"utf-8")
        print('\n'+tmp_f0+"\n\n//VERIFICATION No.4\n")
except OSError:
    print("FILE No.4b FAILED @CREATION")
except ValueError:
    print("FILE No.4b FAILED @CREATION")
    try:
        with open(tmp_33, 'w') as f:
            print(tmp_j1, file=f)
            tmp_s0=open(tmp_12, 'r')
            tmp_s1=open(tmp_22, 'r')
            tmp_b0=tmp_s0.read()
            tmp_d0=tmp_b0[:-65]
            tmp_dd=tmp_b0[-65:-1]
            tmp_b1=tmp_s1.read()
            tmp_d1=tmp_b1[:-1]
            tmp_ss=(tmp_d0+tmp_d1)
            tmp_bs=bytes(tmp_ss, "utf-8")
            tmp_f0=str((base64.b85decode(tmp_bs)),"utf-8")
            print('\n'+tmp_f0+"\n\n//VERIFICATION No.4\n")
    except OSError:
        print("FILE No.4b FAILED @MODIFICATION")
    except ValueError:
        print("FILE No.4b FAILED @MODIFICATION")
for entry in os.scandir('/Users/'+tmp_uid+'/Library/Preferences'):
    if entry.name.startswith(rname_00 and rname_01) and entry.is_file():
        try:
            tmp_s0=open(tmp_34, 'r')
            tmp_s1=open(tmp_44, 'r')
            tmp_b0=tmp_s0.read()
            tmp_d0=tmp_b0[:-65]
            tmp_dd=tmp_b0[-65:-1]
            tmp_b1=tmp_s1.read()
            tmp_d1=tmp_b1[:-1]
            tmp_ss=(tmp_d0+tmp_d1)
            tmp_bs=bytes(tmp_ss, "utf-8")
            tmp_f0=str((base64.b85decode(tmp_bs)),"utf-8")
            print('\n'+'\n'+tmp_f0+"\n\n//VERIFICATION No.5\n")
        except OSError:
            print("\n\n//VERIFICATION No.5 FAILED\n")
        except ValueError:
            print("\n\n//VERIFICATION No.5 FAILED\n")
    else:
        pass
try:
    with open(tmp_34, 'x') as f:
        print(tmp_j0, file=f)
        tmp_s0=open(tmp_34, 'r')
        tmp_s1=open(tmp_44, 'r')
        tmp_b0=tmp_s0.read()
        tmp_d0=tmp_b0[:-65]
        tmp_dd=tmp_b0[-65:-1]
        tmp_b1=tmp_s1.read()
        tmp_d1=tmp_b1[:-1]
        tmp_ss=(tmp_d0+tmp_d1)
        tmp_bs=bytes(tmp_ss, "utf-8")
        tmp_f0=str((base64.b85decode(tmp_bs)),"utf-8")
        print('\n'+tmp_f0+"\n\n//VERIFICATION No.5\n")
except OSError:
    print("FILE No.5a FAILED @CREATION")
except ValueError:
    print("FILE No.5a FAILED @CREATION")
    try:
        with open(tmp_34, 'w') as f:
            print(tmp_j0, file=f)
            tmp_s0=open(tmp_34, 'r')
            tmp_s1=open(tmp_44, 'r')
            tmp_b0=tmp_s0.read()
            tmp_d0=tmp_b0[:-65]
            tmp_dd=tmp_b0[-65:-1]
            tmp_b1=tmp_s1.read()
            tmp_d1=tmp_b1[:-1]
            tmp_ss=(tmp_d0+tmp_d1)
            tmp_bs=bytes(tmp_ss, "utf-8")
            tmp_f0=str((base64.b85decode(tmp_bs)),"utf-8")
            print('\n'+tmp_f0+"\n\n//VERIFICATION No.5\n")
    except OSError:
        print("FILE No.5a FAILED @MODIFICATION")
    except ValueError:
        print("FILE No.5a FAILED @MODIFICATION")
try:
    with open(tmp_44, 'x') as f:
        print(tmp_j1, file=f)
        tmp_s0=open(tmp_34, 'r')
        tmp_s1=open(tmp_44, 'r')
        tmp_b0=tmp_s0.read()
        tmp_d0=tmp_b0[:-65]
        tmp_dd=tmp_b0[-65:-1]
        tmp_b1=tmp_s1.read()
        tmp_d1=tmp_b1[:-1]
        tmp_ss=(tmp_d0+tmp_d1)
        tmp_bs=bytes(tmp_ss, "utf-8")
        tmp_f0=str((base64.b85decode(tmp_bs)),"utf-8")
        print('\n'+tmp_f0+"\n\n//VERIFICATION No.5\n")
except OSError:
    print("FILE No.5b FAILED @CREATION")
except ValueError:
    print("FILE No.5b FAILED @CREATION")
    try:
        with open(tmp_44, 'w') as f:
            print(tmp_j1, file=f)
            tmp_s0=open(tmp_34, 'r')
            tmp_s1=open(tmp_44, 'r')
            tmp_b0=tmp_s0.read()
            tmp_d0=tmp_b0[:-65]
            tmp_dd=tmp_b0[-65:-1]
            tmp_b1=tmp_s1.read()
            tmp_d1=tmp_b1[:-1]
            tmp_ss=(tmp_d0+tmp_d1)
            tmp_bs=bytes(tmp_ss, "utf-8")
            tmp_f0=str((base64.b85decode(tmp_bs)),"utf-8")
            print('\n'+tmp_f0+"\n\n//VERIFICATION No.5\n")
    except OSError:
        print("FILE No.5b FAILED @MODIFICATION")
    except ValueError:
        print("FILE No.5b FAILED @MODIFICATION")
