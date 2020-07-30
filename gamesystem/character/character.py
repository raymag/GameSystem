# from .element import Air, Earth, Fire, Water, Element, random_element
import character.element as element
import random

class Attributes:
    def __init__(self, values = (0, 0, 0, 0, 0, 0) ):
        self.__set(values)
    
    def __set(self, values):
        self.__str = values[0]
        self.__dex = values[1]
        self.__vit = values[2]
        self.__int = values[3]
        self.__per = values[4]
        self.__cha = values[5]
    
    def values(self):
        return ( self.__str, self.__dex, self.__vit, self.__int, self.__per, self.__cha,  )
    
    def get(self):
        attributes = ('str', 'dex', 'vit', 'int', 'per', 'cha')
        values = self.values()
        return { attributes[i]:values[i] for i in range(len(attributes)) }

    def apply_modifiers(self, modifiers):
        values = self.values()
        attributes = tuple( values[i] + modifiers[i] for i in range(len(values)) )
        self.__set(attributes)
        return self.get()

    def load(self, dict_attr):
        values = [ dict_attr[i] for i in dict_attr  ]
        self.__set(values)

class Character:
    def __init__(
                self,
                name,
                user,
                gender = 'unknown',
                age = 18,
                species = 'unknown',
                attributes = Attributes(),
                affinity = element.random_element(),
                status = "alive",
                lv = 1,
                ):
        attributes.apply_modifiers(affinity.get_modifiers())

        self.__name = name
        self.__gender = gender
        self.__age = age
        self.__species = species
        self.__affinity = affinity
        self.__attributes = attributes
        self.__status = status
        self.__lv = lv 
        self.__xp = 0
        self.__cp = 0
        self.__ip = 0
        self.__gold = 0
        self.__main = False
        self.__user = user

        values = self.__attributes.get()
        self.__def = values["dex"] + values["vit"] + 10
        self.__hp = 12 + values["vit"]
        self.__mp = 10 + values["int"]
        
    def get_user(self):
        return self.__user

    def get_name(self):
        return self.__name
    
    def get_gender(self):
        return self.__gender
    
    def get_age(self):
        return self.__age
    
    def get_species(self):
        return self.__species
    
    def get_attributes(self):
        return self.__attributes.get()

    def get_attribute_values(self):
        return self.__attributes.values()

    def get_attributes_dict(self):
        return self.__attributes.__dict__

    def get_affinity(self):
        return self.__affinity.get_name()

    def get_affinity_values(self):
        return self.__affinity.__dict__

    def get_status(self):
        return self.__status
    
    def get_def(self):
        return self.__def
    
    def get_hp(self):
        return self.__hp
    
    def get_mp(self):
        return self.__mp
    
    def get_lv(self):
        return self.__lv

    def get_xp(self):
        return self.__xp
    
    def get_cp(self):
        return self.__cp
    
    def get_ip(self):
        return self.__ip
    
    def get_gold(self):
        return self.__gold
    
    def is_main(self):
        return self.__main

    
    def set_main(self):
        self.__main = not self.__main

    def defend(self, attack):
        if self.__def > attack:
            return True
        return False

    def hit(self, damage):
        self.__hp -= damage  
        if self.__hp <= 0:
            successes, fails = 0, 0
            while True:
                chance = random.randint(1, 20)
                if chance >= 10:
                    successes += 1
                    if successes == 3:
                        self.__hp = 0
                        self.__status = "unconscious"
                        break
                else:
                    fails += 1
                    if fails == 3:
                        self.__hp = 0
                        self.__status = "dead"
                        break
        
    def rest(self):
        blocked_status = ["dead"]
        if self.__status not in blocked_status:
            values = self.__attributes.get()
            self.__hp = 12 + values["vit"]
            self.__mp = 10 + values["int"]

    def res(self):
        values = self.__attributes.get()
        self.__hp = 12 + values["vit"]
        self.__mp = 10 + values["int"]
        self.__status = "alive"

    def test(self, attribute):
        try:
            values = self.__attributes.get()
            chance = random.randint(1, 20) 
            result = chance + values[attribute]
            return (result, chance, values[attribute])
        except:
            raise Exception("Attribute doesn't match Character attribute.")

    def dump(self):
        dict_char = self.__dict__.copy()
        dict_char["_Character__affinity"] = self.get_affinity_values()
        dict_char["_Character__attributes"] = self.get_attributes_dict()
        return dict_char
    
    def load(self, dict_char):
        attrs = Attributes()
        attrs.load(dict_char["_Character__attributes"])
        dict_char["_Character__attributes"] = attrs

        if dict_char["_Character__affinity"]["_Element__name"] == 'earth':
            affinity = element.Earth()
        if dict_char["_Character__affinity"]["_Element__name"] == 'air': 
            affinity = element.Air()
        if dict_char["_Character__affinity"]["_Element__name"] == 'fire':
            affinity = element.Fire()
        if dict_char["_Character__affinity"]["_Element__name"] == 'water':
            affinity = element.Water()
        dict_char["_Character__affinity"] = affinity

        dict_char_keys = [i for i in dict_char]
        for i in range(len(dict_char)):
            setattr(self, dict_char_keys[i], dict_char[dict_char_keys[i]])

class Human(Character):
    def __init__(self, name, user, gender = 'unknown', age = 18, attributes = Attributes(), affinity = element.random_element()):
        super().__init__(name, user, gender, age, 'human', attributes, affinity)

# eu = Human("Magno")
# print(eu.get_name())
# print(eu.get_affinity())
# print(eu.isMain())
# eu.setMain()
# print(eu.isMain())