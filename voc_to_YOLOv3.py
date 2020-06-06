 
import xml.etree.ElementTree as ET
from os import getcwd
import os

class XML_to_txt:
    def __init__(self):
        self.dataset_train = 'Dataset/train/'
        self.dataset_file = 'Hand_Class.txt'
        self.classes_file = self.dataset_file[:-4]+'_classes.txt'
        self.CLS = os.listdir(self.dataset_train)
        self.classes =[self.dataset_train+CLASS for CLASS in self.CLS]
        self.wd = getcwd()


    def test(self,fullname):
        bb = ""
        in_file = open(fullname)
        tree=ET.parse(in_file)
        root = tree.getroot()
        for i, obj in enumerate(root.iter('object')):
            difficult = obj.find('difficult').text
            cls = obj.find('name').text
            if cls not in self.CLS or int(difficult)==1:
                continue
            cls_id = self.CLS.index(cls)
            xmlbox = obj.find('bndbox')
            b = (int(xmlbox.find('xmin').text), int(xmlbox.find('ymin').text), int(xmlbox.find('xmax').text), int(xmlbox.find('ymax').text))
            bb += (" " + ",".join([str(a) for a in b]) + ',' + str(cls_id))

            # we need this because I don't know overlapping or something like that
            if cls == 'Traffic_light':
                list_file = open(self.dataset_file, 'a')
                file_string = str(fullname)[:-4]+'.jpg'+bb+'\n'
                list_file.write(file_string)
                list_file.close()
                bb = ""

        if bb != "":
            list_file = open(self.dataset_file, 'a')
            file_string = str(fullname)[:-4]+'.jpg'+bb+'\n'
            list_file.write(file_string)
            list_file.close()


    def convert(self):
        for CLASS in self.classes:
            for filename in os.listdir(CLASS):
                if not filename.endswith('.xml'):
                    continue
                fullname = os.getcwd()+'/'+CLASS+'/'+filename
                self.test(fullname)

        for CLASS in self.CLS:
            list_file = open(self.classes_file, 'a')
            file_string = str(CLASS)+"\n"
            list_file.write(file_string)
            list_file.close()