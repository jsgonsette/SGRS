# MIT License

# Copyright (c) [2020] [Jean-Sébastien Gonsette]

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

__author__ = "Jean-Sébastien Gonsette"
__year__ = 2019



import Tools.ciphers as ciphers

mendeleiv_fr = [
    'Hydrogene', 'Helium', 'Lithium', 'Beryllium', 'Bore', 'Carbone', 'Azote', 'Oxygene', 'Fluor',
    'Sodium', 'Magnesium', 'Aluminium', 'Silicium', 'Phosphore', 'Soufre', 'Chlore', 'Argon', 'Potassium',
    'Calcium', 'Scandium', 'Titane', 'Vanadium', 'Chrome', 'Manganese', 'Fer', 'Cobalt', 'Nickel', 'Cuivre',
    'Zinc', 'Germanium', 'Arsenic', 'Selenium', 'Brome', 'Krypton', 'Rubidium', 'Strontium', 'Yttrium', 'Zirconium', 'Niobium', 'Molybdene',
    'Technetium', 'Ruthenium', 'Rhodium', 'Palladium', 'Argent', 'Cadmium', 'Indium', 'etain', 'Antimoine', 'Tellure', 'Iode',
    'Xenon', 'Cesium', 'Baryum', 'Lanthane', 'Cerium', 'Praseodyme', 'Neodyme', 'Promethium', 'Samarium', 'Europium', 'Gadolinium',
    'Terbium', 'Dysprosium', 'Holmium', 'Erbium', 'Thulium', 'Ytterbium', 'Lutecium', 'Hafnium', 'Tantale', 'Tungstene',
    'Rhenium', 'Osmium', 'Iridium', 'Platine', 'Or', 'Mercure', 'Thallium', 'Plomb', 'Bismuth', 'Polonium', 'Astate', 'Radon',
    'Francium', 'Radium', 'Actinium', 'Thorium', 'Protactinium', 'Uranium', 'Neptunium', 'Plutonium', 'Americium', 'Curium', 'Berkelium',
    'Californium', 'Einsteinium', 'Fermium', 'Mendelevium', 'Nobelium', 'Lawrencium', 'Rutherfordium', 'Dubnium', 'Seaborgium', 'Bohrium',
    'Hassium', 'Meitnerium', 'Darmstadtium', 'Roentgenium', 'Ununbium', 'Ununtrium', 'Ununquadium', 'Ununpentium',
    'Ununhexium', 'Ununseptium', 'Ununoctium']

mendeleiv_en= [
    'Hydrogen', 'Helium', 'Lithium', 'Beryllium', 'Boron', 'Carbon',
    'Nitrogen', 'Oxygen', 'Fluorine', 'Neon', 'Sodium', 'Magnesium',
    'Aluminum', 'Silicon', 'Phosphorus', 'Sulfur', 'Chlorine', 'Argon',
    'Potassium', 'Calcium', 'Scandium', 'Titanium', 'Vanadium', 'Chromium',
    'Manganese', 'Iron', 'Cobalt', 'Nickel', 'Copper', 'Zinc',
    'Gallium', 'Germanium', 'Arsenic', 'Selenium', 'Bromine', 'Krypton',
    'Rubidium', 'Strontium', 'Yttrium', 'Zirconium', 'Niobium', 'Molybdenum',
    'Technetium', 'Ruthenium', 'Rhodium', 'Palladium', 'Silver', 'Cadmium',
    'Indium', 'Tin', 'Antimony', 'Tellurium', 'Iodine', 'Xenon',
    'Cesium', 'Barium', 'Lanthanum', 'Cerium', 'Praseodymium', 'Neodymium',
    'Promethium', 'Samarium', 'Europium', 'Gadolinium', 'Terbium', 'Dysprosium',
    'Holmium', 'Erbium', 'Thulium', 'Ytterbium', 'Lutetium', 'Hafnium',
    'Tantalum', 'Tungsten', 'Rhenium', 'Osmium', 'Iridium', 'Platinum',
    'Gold', 'Mercury', 'Thallium', 'Lead', 'Bismuth', 'Polonium',
    'Astatine', 'Radon', 'Francium', 'Radium', 'Actinium', 'Thorium',
    'Protactinium', 'Uranium', 'Neptunium', 'Plutonium', 'Americium', 'Curium',
    'Berkelium', 'Californium', 'Einsteinium', 'Fermium', 'Mendelevium', 'Nobelium',
    'Lawrencium', 'Rutherfordium', 'Dubnium', 'Seaborgium', 'Bohrium', 'Hassium',
    'Meitnerium', 'Darmstadtium', 'Roentgenium', 'Copernicium', 'Nihonium', 'Flerovium',
    'Moscovium', 'Livermorium', 'Tennessine', 'Oganesson']    

anagrams = ['Robe', 'Racines', "Melusine", "Ombre", "Truelle", "Etalant", "Epilant", "Plainte", "Pliante"]

def build_mendeleiev_list ():

    # Merge french and english
    mendel_set = set (mendeleiv_fr)
    for item in mendeleiv_en: mendel_set.add (item)
    for item in anagrams: mendel_set.add (item)

    mendel_list = []
    dico_reverse = {}

    keys = ["MENDELEIEV", "DIMITRIMENDELEIEV", "TABLEAUMENDELEIEV", "TABLEAUPERIODIQUE"]

    for item in mendel_set:
        
        item = item.upper ()        
        
        # Add item in direct and reverse directions
        mendel_list.append (item)
        mendel_list.append (''.join (reversed (item)))

        # Add every possible rotations
        for i in range (1, 26):
            encoded = ciphers.rotate (item, i)
            mendel_list.append (encoded)
            dico_reverse [encoded] = item + '/ROT-' + str (i)

        # Autoclave with Vigenere
        encoded = ciphers.vigenere (item, item)
        mendel_list.append (encoded)
        dico_reverse [encoded] = item + '/VIG-AUTO'

        # Add item ciphered with Vigenere and Beaufort
        for key in keys:

            encoded1 =  ciphers.vigenere (item, key, reverse=False)
            encoded2 =  ciphers.vigenere (item, key, reverse=True)
            encoded3 =  ciphers.beaufort (item, key)
            mendel_list.append (encoded1)
            mendel_list.append (encoded2)
            mendel_list.append (encoded3)
            dico_reverse [encoded1] = item + '/VIG-' + key
            dico_reverse [encoded2] = item + '/VIG-R-' + key
            dico_reverse [encoded3] = item + '/BEAU-' + key

    return mendel_list, dico_reverse
