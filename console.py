#!/usr/bin/python3
'''defines The HBnB Console'''

import re
import cmd
from models.user import User
from models.state import State
from models.city import City
from shlex import split
from models.place import Place
from models.amenity import Amenity
from models.review import Review
from models import storage
from models.base_model import BaseModel

def parse(arg):
    crly_brces = re.search(r"\{(.*?)\}", arg)
    brckets = re.search(r"\[(.*?)\]", arg)
    if crly_brces is None:
        if brckets is None:
            return [i.strip(",") for i in split(arg)]
        else:
            lxer = split(arg[:brckets.span()[0]])
            rtl = [i.strip(",") for i in lxer]
            rtl.append(brckets.group())
            return rtl
    else:
        lxer = split(arg[:crly_brces.span()[0]])
        rtl = [i.strip(",") for i in lxer]
        rtl.append(crly_brces.group())
        return rtl


class HBNBCommand(cmd.Cmd):
    '''defines The holbertonBnB Command Interpreter

    attributes:
        Prompt (str): a Command Prompt
    '''

    prompt = "(hbnb) "
    __classes = {
        "BaseModel",
        "User",
        "State",
        "City",
        "Place",
        "Amenity",
        "Review"
    }

    def emptyline(self):
        '''do Nothing Upon Receiving An Empty Line'''
        pass

    def default(self, arg):
        '''default Behavior For Cmd Module When Input Is Invalid'''
        rgdct = {
            "all": self.do_all,
            "show": self.do_show,
            "destroy": self.do_destroy,
            "count": self.do_count,
            "update": self.do_update
        }
        match = re.search(r'\.', arg)
        if match is not None:
            rgl = [arg[:match.span()[0]], arg[match.span()[1]:]]
            match = re.search(r'\((.*?)\)', rgl[1])
            if match is not None:
                comand = [rgl[1][:match.span()[0]], match.group()[1:-1]]
                if comand[0] in rgdct.keys():
                    cal = '{} {}'.format(rgl[0], comand[1])
                    return rgdct[comand[0]](cal)
        print('*** unknown Syntax: {}'.format(arg))
        return False

    def do_quit(self, arg):
        '''quit Command To Exit The Program'''
        return True

    def do_EOF(self, arg):
        '''eOF Signal To Exit The Program'''
        print("")
        return True

    def do_create(self, arg):
        '''usage: Create <class>
        create the New Class Instance And Print Its Id
        '''
        rgl = parse(arg)
        if len(rgl) == 0:
            print('** class name missing **')
        elif rgl[0] not in HBNBCommand.__classes:
            print("** class doesn't exist **")
        else:
            print(eval(rgl[0])().id)
            storage.save()

    def do_show(self, arg):
        ''' usage: Show <class> <id> Or <class>.show(<id>)
        display The String Representation Of THE Class Instance Of THE Given Id
        '''
        rgl = parse(arg)
        bjdct = storage.all()
        if len(rgl) == 0:
            print('** class name missing **')
        elif rgl[0] not in HBNBCommand.__classes:
            print("** class doesn't exist **")
        elif len(rgl) == 1:
            print('** instance id missing **')
        elif '{}.{}'.format(rgl[0], rgl[1]) not in bjdct:
            print('** no instance found **')
        else:
            print(bjdct['{}.{}'.format(rgl[0], rgl[1])])

    def do_destroy(self, arg):
        '''usage: Destroy <class> <id> Or <class>.destroy(<id>)
        delete THE Class Instance Of THE Given Id'''
        rgl = parse(arg)
        bjdct = storage.all()
        if len(rgl) == 0:
            print('** Class Name Missing **')
        elif rgl[0] not in HBNBCommand.__classes:
            print("** Class Doesn't exist **")
        elif len(rgl) == 1:
            print('** Instance Id Missing **')
        elif "{}.{}".format(rgl[0], rgl[1]) not in bjdct.keys():
            print('** No Instance Found **')
        else:
            del bjdct["{}.{}".format(rgl[0], rgl[1])]
            storage.save()

    def do_all(self, arg):
        '''usage: All Or All <class> Or <class>.all()
        display String Representations Of All Instances Of THE Given Class
        if No Class Is Specified Displays All Instantiated Objects'''
        rgl = parse(arg)
        if len(rgl) > 0 and rgl[0] not in HBNBCommand.__classes:
            print("** Class Doesn't Exist **")
        else:
            bjl = []
            for obj in storage.all().values():
                if len(rgl) > 0 and rgl[0] == obj.__class__.__name__:
                    bjl.append(obj.__str__())
                elif len(rgl) == 0:
                    bjl.append(obj.__str__())
            print(bjl)

    def do_count(self, arg):
        '''usage: Count <class> Or <class>.count()
        retrieve The Number Of Instances Of THE Given Class'''
        rgl = parse(arg)
        cunt = 0
        for obj in storage.all().values():
            if rgl[0] == obj.__class__.__name__:
                cunt += 1
        print(cunt)

    def do_update(self, arg):
        '''usage: Update <class> <id> <attribute_name> <attribute_value> Or
       <class>.update(<id>, <attribute_name>, <attribute_value>) Or
       <class>.update(<id>, <dictionary>)
        update the Class Instance Of THE Given Id By Adding Or Updating
        THE Given Attribute Key/Value Pair Or Dictionary'''
        rgl = parse(arg)
        bjdct = storage.all()

        if len(rgl) == 0:
            print('** Class Name Missing **')
            return False
        if rgl[0] not in HBNBCommand.__classes:
            print("** Class Doesn't Exist **")
            return False
        if len(rgl) == 1:
            print('** Instance Id Missing **')
            return False
        if "{}.{}".format(rgl[0], rgl[1]) not in bjdct.keys():
            print('** No Instance Found **')
            return False
        if len(rgl) == 2:
            print('** Attribute Name Missing **')
            return False
        if len(rgl) == 3:
            try:
                type(eval(rgl[2])) != dict
            except NameError:
                print('** Value Missing **')
                return False

        if len(rgl) == 4:
            bj = bjdct["{}.{}".format(rgl[0], rgl[1])]
            if rgl[2] in bj.__class__.__dict__.keys():
                vltype = type(bj.__class__.__dict__[rgl[2]])
                bj.__dict__[rgl[2]] = vltype(rgl[3])
            else:
                bj.__dict__[rgl[2]] = rgl[3]
        elif type(eval(rgl[2])) == dict:
            bj = bjdct["{}.{}".format(rgl[0], rgl[1])]
            for k, v in eval(rgl[2]).items():
                if (k in bj.__class__.__dict__.keys() and
                        type(bj.__class__.__dict__[k]) in {str, int, float}):
                    vltype = type(bj.__class__.__dict__[k])
                    bj.__dict__[k] = vltype(v)
                else:
                    bj.__dict__[k] = v
        storage.save()


if __name__ == "__main__":
    HBNBCommand().cmdloop()
