import xml.etree.ElementTree as xml
from xml.dom import minidom
import os

__user_db__ = {}
__channel_db__ = {}
__user_db_path__ : str

__USERS_TAG__ = "Users"
__CHANNELS_TAG = "Channels"
__NAME_ATTR__ = "Name"
__BDAY_ATTR__ = "Bday"

def init(db_path = "users_db.xml"):
    __user_db_path__ = db_path
    
    if not os.path.exists(__user_db_path__):
        db = xml.Element(tag="Db")
        xml.SubElement(parent=db, tag=__USERS_TAG__)
        xml.SubElement(parent=db, tag=__CHANNELS_TAG)
        
        with open(__user_db_path__, "w") as new_db:
            new_db.write(minidom.parseString(xml.tostring(db, "unicode")).toprettyxml(indent="\t"))


    tree = xml.parse(__user_db_path__)
    root = tree.getroot()

    for channel in root:
        channel_name = channel.get(__NAME_ATTR__)
        for user in channel:
            __user_db__[channel_name] = [ user.get(__NAME_ATTR__), user.get(__BDAY_ATTR__) ]

def register_user(name : str, bday : str):
    tree = xml.parse(__user_db_path__)
    root = tree.getroot()


def unregister_user(name : str):
    pass

def get_user(name : str):
    pass