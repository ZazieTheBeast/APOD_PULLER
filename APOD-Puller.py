from urllib.request import Request, urlopen, urlretrieve
from urllib.error import URLError, HTTPError
from bs4 import BeautifulSoup
from tkinter import Tk, ttk
import re, time, ctypes, os, sys

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
    pattern = re.compile('^image.*\.(bmp|jpg|gif|png)$')
    for x in soup.find_all('a'):
        if pattern.search(x['href']) != None:
            path_to_img = (site + x['href'])
            print(path_to_img)
            get_n_store(path_to_img)
            break


def get_n_store(path):


    def getScriptPath():
        return os.path.dirname(os.path.realpath(sys.argv[0]))

    def determine_os():
        os_type = os.name

        if os_type == 'nt':
            print('nt')

    newpath = getScriptPath()+'/APOD_Pics'
    if not os.path.exists(newpath):
        os.makedirs(newpath)

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

    if determine_os() == 'linux':
        switch = '/'
    elif determine_os() == 'mac':
        switch = '/'
    else:
        switch = '\\'
    ext = path.rsplit('.',1)[-1]
    timestr = time.strftime("%Y%m%d")
    fname = (timestr+'.'+ext)
    full_path = newpath+switch+fname
    if not os.path.isfile(full_path):
        download2(path, full_path)
        set_background_windows(full_path)

def set_background_linux(path_to_img):


def set_background_windows(path_to_img):
    ctypes.windll.user32.SystemParametersInfoA(SPI_SETDESKWALLPAPER, 0, path_to_img , 0)

__init__(url)