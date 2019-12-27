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


def build_mendeleiev_list ():

    mendel_set = set (mendeleiv_fr)
    for item in mendeleiv_en: mendel_set.add (item)
    mendel_list = []
    dico_reverse = {}

    keys = ["MENDELEIEV", "DIMITRIMENDELEIEV", "DMITRIMENDELEIEV", "TABLEAUMENDELEIEV", "TABLEAUPERIODIQUE"]

    for item in mendel_set:
        
        item = item.upper ()        
        
        # Add item
        mendel_list.append (item)
        mendel_list.append (''.join (reversed (item)))

        # Add every possible rotations
        for i in range (1, 26):
            encoded = ciphers.rotate (item, i)
            mendel_list.append (encoded)
            dico_reverse [encoded] = item + '/ROT-' + str (i)

        # Add item ciphered with Vigenere
        for key in keys:

            encoded1 =  ciphers.vigenere (item, key, reverse=False)
            encoded2 =  ciphers.vigenere (item, key, reverse=True)
            mendel_list.append (encoded1)
            mendel_list.append (encoded2)
            dico_reverse [encoded1] = item + '/VIG-' + key
            dico_reverse [encoded2] = item + '/VIG-R-' + key

    return mendel_list, dico_reverse
