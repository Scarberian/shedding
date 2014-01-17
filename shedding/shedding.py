import glob
import ipdb
import subprocess
from sys import argv
from collections import OrderedDict
#import Queue #this is for the final form 
from snakepit import *

#import threading # or at least once testing is going down
#keep while same
#http://stackoverflow.com/a/101739

class Molting:
    """()-*.mdta file in the pwd with all pertinent ID3V2 infos within
        this is where the shitty old hide is sundered away and gleaming
        new scales(well ordered flacs emerge)
    """
    def __init__(\
            self,
            bpm,
            year,
            track,
            artist=None,
            title=None,
            album=None,
            genre=None,
            file_in=None,
            name=None,
            id_head=None,
            id_flds=None,
            id_media=None,
            mdta=None,
            cwd=None):

        self.bpm = bpm
        self.year = year
        self.track= track
        self.artist = artist
        self.title = title
        self.album = album
        self.genre = genre
        self.file_in = file_in
        self.name = name
        self.idv3_head = id_head
        self.idv3_flds = id_flds
        self.idv3_media = id_media
        self.mdta = mdta
        self.cwd=cwd

    def filer(self,clargs):
        """(static contents, values, keys) -> Valid IDV3 output
            As it is in molting.py:
            filer(x.idv3_head, x.idv3_media, x.idv3_flds)
        """
        print("Filer: ")
        with open(self.mdta, 'w') as mdta:
            for i in self.idv3_head+self.idv3_media:
                print(i)
                mdta.write(i)
            tagger = zip(self.idv3_flds, clargs)
            for i in tagger:
                print("".join((i[0],i[1]))+'\n')
                mdta.write("".join((i[0],i[1]))+'\n')
        pass

    def flaker(self):

        cwd = self.cwd.encode('string-escape')
        file = self.file_in.encode('string-escape')
        name = self.name.encode('string-escape')

        flac_call = '''ffmpeg -i {0}{2}.wav  -acodec flac {0}{1}.flac'''.format(cwd, name, file)
        mdta_impreg = '''ffmpeg -i {0}{1}.flac -i {0}{1}.mdta map_metadata 1 -id3v2_version 3 -write_id3v1 1 -acodec /usr/bin/flac"{0}{1}.flac '''.format(cwd,name)
        print("FLAC CALL: "+ flac_call)
        print("FLAC CALL: "+ mdta_impreg)
        return subprocess.call(flac_call,shell=True),subprocess.call(mdta_impreg,shell=True)

    def deglover(self):

        call = '''/usr/bin/ffmpeg -y -i "{0}{2}.wav" -i "{0}{1}.mdta" -i "{0}folder.jpg" -map_metadata 1 -map 0 -map 2 -metadata:s:v title="Album cover" -metadata:s:v comment="Cover (Front)" -id3v2_version 3 -write_id3v1 1 -acodec libmp3lame -b:a 320k "{0}{1}.mp3"'''.format(self.cwd,self.name, self.file_in)
        print("Deglover: "+call)
        return subprocess.call(call,shell=True)

    def scales(self):

        call = '''/usr/bin/metaflac --import-picture-from="{0}folder.jpg" "{0}{1}.flac"'''.format(self.cwd,self.name)
        print("Scales: "+call)
        return subprocess.call(call,shell=True)

    pass

def shedding(Snake, user):
    """(Class(), str, str)
    """
    pwd = str(subprocess.check_output("pwd",shell=True)).strip()#+"/"
    file_name=user[2]+" - "+user[3]+" - "+user[4]
    user[7] = user[7].split('.')[0]
    Snake.register("hatch",
                   Molting,
                   user[0],
                   user[1],
                   user[2],
                   artist=user[3].strip(),
                   title=user[4].strip(),
                   album=user[5].strip(),
                   genre=user[6].strip(),
                   file_in=user[7].strip(),
                   name=file_name.strip(),
                   id_head = [";FFMETADATA1"+'\n'],
                   id_flds = ["BPM=",
                              "DATE=",
                              "TRACK=",
                              "ARTIST=",
                              "TITLE=",
                              "ALBUM=",
                              "GENRE="],
                   id_media = [\
                           "APIC={}folder.jpg".format(pwd)+'\n',
                           "PICTURE={}folder.jpg".format(pwd)+'\n'],
                   mdta=pwd+file_name+".mdta",
                   cwd=pwd)

    x = Snake.hatch()
    x.filer(user)
    x.flaker()
    x.deglover()
    x.scales()
    return Snake.unregister("hatch")

def main():
    """
    cli input in this order
    python3 shedding.py 01 ARTNAME TRACKNAME ALBUMTITLE GENRE BPM YEAR
    """
    clargs = argv[1 :]

    convert = Constrictor()
    return shedding(convert ,clargs)
main()
