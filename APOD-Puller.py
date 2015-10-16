from urllib.request import Request, urlopen
from urllib.error import URLError, HTTPError
from bs4 import BeautifulSoup
from tkinter import Tk, ttk
from time import strftime
from re import compile
from ctypes import windll
from os import path, makedirs
from subprocess import call
from sys import argv
from platform import system

__author__ = 'kmkass'
url = 'http://apod.nasa.gov/apod/'

def __init__(url):
    test_url(url)


def test_url(site):
    req = Request(site)
    try:
        data = urlopen(req)
    except HTTPError as e:
        print('The server couldn\'t fulfill the request.')
        print('Error code: ', e.code)
    except URLError as e:
        print('We failed to reach a server.')
        print('Reason: ', e.reason)
    else:
        print('Established Connection.')
        find_itod(site, data)


def find_itod(site, data):
    soup = BeautifulSoup(data, 'html.parser')
    pattern = compile('^image.*\.(bmp|jpg|gif|png)$')
    for x in soup.find_all('a'):
        if pattern.search(x['href']) != None:
            path_to_img = (site + x['href'])
            print(path_to_img)
            get_n_store(path_to_img)
            break


def get_n_store(img_path):


    def getScriptPath():
        return path.dirname(path.realpath(argv[0]))

    newpath = getScriptPath()+'/APOD_Pics'
    if not path.exists(newpath):
        makedirs(newpath)

    def download2(url, filename):
        response = urlopen(url)
        totalsize = int(response.headers['Content-Length']) # assume correct header
        outputfile = open(filename, 'wb')

        def download_chunk(readsofar=0, chunksize=1 << 13):
            # report progress
            percent = readsofar * 1e2 / totalsize # assume totalsize > 0
            root.title('%%%.0f %s' % (percent, filename,))
            progressbar['value'] = percent

            # download chunk
            data = response.read(chunksize)
            if not data: # finished downloading
                outputfile.close()
                root.destroy() # close GUI
            else:
                outputfile.write(data) # save to filename
                # schedule to download the next chunk
                root.after(0, download_chunk, readsofar + len(data), chunksize)

        # setup GUI to show progress
        root = Tk()
        root.withdraw() # hide
        progressbar = ttk.Progressbar(root, length=400)
        progressbar.grid()
        # show progress bar if the download takes more than .5 seconds
        root.after(500, root.deiconify)
        root.after(0, download_chunk)
        root.mainloop()

    this_os = system()
    # unix or linux
    if this_os == 'Linux':
        switch = '/'
    elif this_os == 'mac':
        switch = '/'
    elif this_os == 'Windows':
        switch = '\\'
    else:
        print('unknown OS')
    ext = img_path.rsplit('.', 1)[-1]
    timestr = strftime("%Y%m%d")
    fname = (timestr+'.'+ext)
    full_path = newpath+switch+fname
    if not path.isfile(full_path):
        download2(img_path, full_path)
        if this_os == 'Linux':
            set_background_raspi(full_path)
        elif this_os == 'Windows':
            set_background_windows(full_path)
        else:
            print("unknown OS")
        # set to windows background, edited out until i can test it.
        # set_background_windows(full_path)

def set_background_linux(path_to_img):
    print("This is where the linux commands would go.")

def set_background_raspi(path_to_img):
    call("pcmanfm --set-wallpaper " + path_to_img, shell=True)

def set_background_windows(path_to_img):
    windll.user32.SystemParametersInfoA(SPI_SETDESKWALLPAPER, 0, path_to_img, 0)

__init__(url)