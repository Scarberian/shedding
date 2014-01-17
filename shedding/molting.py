
"""
TODO:(brian)
    Write Factory() class to dynamically define as much or as little
    conversion information for valid idv3v1 tags
TODO:(brian)
    implement threading à la http://docs.python.org/3/library/threading.html
    leveraging queuing and threading is good
    http://docs.python.org/3/library/queue.html#module-queue

    Molting: Snake like audio conversion tool that wraps around
    the venerable ffmpeg.

    Instances of the class Flaccing are instanciated with a list of
    positional arguments corresponding to track, artist, album, title
    genre, bpm, date

"""
from collections import OrderedDict
import ipdb
import os
from unittest.mock import patch

txa = ['1',
       'Artist-here',
       'album-here',
       'title-here',
       'genre-here',
       '999',
       '2014']

class Molting(object):
    """(list of str) audio conversion and idv3 data work
        only the subset of valid idv3 fields are used
        for now...
    """
    track = None
    clargs = None
    file = None
    #just because this almost looks like duplicated code, it isnt.

    field = [ "track" ,
              "artist",
              "album",
              "title",
              "genre",
              "bpm",
              "date" ]

    metadata = OrderedDict()
#these strings are idv3 keys. The ones prior are for internal book keeping
    idv3_head = [";FFMETADATA1"+'\n']
    idv3_flds = ["track=",
                 "ARTIST=",
                 "ALBUM=",
                 "TITLE=",
                 "GENRE=",
                 "DATE=",
                 "BPM="]
    idv3_media =["APIC=folder.jpg"+'\n',
                 "PICTURE=folder.jpg"+'\n']


# this class is a good candidate for class factory patter
# http://code.activestate.com/recipes/86900/

    def __init__(self,tx=txa):
        """(list of arguments) - > file open for editing
        """

        #the indexing here  on tx be buffed out once input protocol stabilizes
        self.clargs = [i for i in tx[1 :]]

        self.title = self.clargs[0]+' - '+self.clargs[1]+' - '+self.clargs[2]
        self.file = open(self.title+'.mdta', 'w')
        for i in zip(self.field, txa):
            self.metadata[i[0]]=i[1]

  #  def skin(self):
  #      """()-*.mdta file in the pwd with all pertinent ID3V2 infos within
  #          this is where the shitty old hide is sundered away and gleaming
  #          new scales(well ordered flacs emerge)
  #      """
    def flake(self):

        title = self.title
        idv_map = "map_metadata 1 \
                     -id3v2_version 3 \
                     -write_id3v1 1 et \
                     -acodec flac .flac "

        call = os.system(\
        '''fmpeg -y -i \
        {0}.wav -i \
        {0}.mdta '''.format(title)+idv_map+'''\
        {0}'''.format(self.title))
        return call

    def scales(self):

        call = os.system(\
        '''metaflac --import-picture-from=folder.jpg \
        {0}.flac'''.format(self.title))
        return call


    def deglove(self):
        call = os.system(\
        '''ffmpeg -y -i \
        {0}.wav -i \
        {0}.mdta -i folder.jpg \
        -map_metadata 1 -map 0 -map 2 -metadata:s:v title="Album cover" \
        -metadata:s:v comment="Cover (Front)" -id3v2_version 3 \
        -write_id3v1 1 -acodec mp3 -b:a 320k {0}.mp3'''.format(self.title))
        return call






    def filer(self, head, media, fields):
        """(static contents, values, keys) -> Valid IDV3 output
        """
        boilerplate = head+media
            #recall the book keeping
        t_num = self.metadata['track']
        if t_num != None and len(str(t_num)) < 2 :
            t_num = t_num.rjust(2,'0')
        content = [self.metadata[i] for i in self.metadata.keys()]

        for i in boilerplate:
            self.file.write(i)
        fielder = zip(self.idv3_flds, content)
        for i in fielder:
            self.file.write("".join((i[0],i[1]))+'\n')
        self.file.close()
    def test_syscalls(self):

        @patch('os.system', return_value=0)
        def test_call0(system_returns_zero):
            self.flake()
        @patch('os.system', return_value=0)
        def test_call1(system_returns_zero):
            self.scales()
        @patch('os.system', return_value=0)
        def test_call2(system_returns_zero):
            self.deglove()
        return test_call0(),test_call1(), test_call2()

influx = ['01', 'Artist-here', 'album-here', 'title-here', 'genre-here', '999', '2014']
x = Molting(influx)
x.test_syscalls()
x.filer(x.idv3_head, x.idv3_media, x.idv3_flds)
x.flake()
x.scales()
x.deglove()
