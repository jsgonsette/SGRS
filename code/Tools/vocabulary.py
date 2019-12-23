import os
import re
import platform
import random
import time
from Tools.libWizium import Wizium


class Vocabulary:

    # ============================================================================
    def __init__ (self, wizium_path, dico_path):
    # ============================================================================
        self.wiz = Wizium (os.path.join (os.getcwd (), wizium_path))
        self._load_dictionary (os.path.join (os.getcwd (), dico_path))


    # ============================================================================
    def is_valid_start (self, sentence, can_extend=True):
        """Return true if the begining of a sentence make sense, that is, if it
        is made up of several known words. The last word may be incomplete"""        
    # ============================================================================

        possib_starts = [0]
        extention_length = 0

        while True:
            possib_ends = self._find_possibile_end_pos (sentence, possib_starts, can_extend)

            if any ([len (sentence) <= p for p in possib_ends]) : 
                return True

            if not len (possib_ends):
                return False

            possib_starts = possib_ends



    # ============================================================================
    def _find_possibile_end_pos (self, sentence, possible_start_pos, can_extend=False):
    # ============================================================================

        max_extention = 10
        possibilities = set ()

        for pos_start in possible_start_pos:
            pos_end = pos_start +1
            extention = ''
           
            while pos_end <= len (sentence) + len (extention):
               
                # Find a match for this sub string
                word = sentence [pos_start: pos_end] + extention
                if pos_end - pos_start > 1:
                    entry = self.wiz.dic_find_entry (word)
                elif word in ['A', 'C', 'J', 'N', 'S', 'M', 'T', 'L']:
                    entry = None #word
                else: entry = None

                # Add this valid end to our list
                if entry is not None:
                    length = (pos_end-pos_start)
                    if pos_end not in possible_start_pos: possibilities.add ( pos_end )
                    pos_end += 1

                # Keep searching with longer words
                elif len (extention) < 10:
                    pos_end += 1
                    if pos_end > len (sentence) and can_extend:
                        extention += '*'

                # Or give up
                else: break
        
        return possibilities



    # ============================================================================
    def _load_dictionary (self, dico_path):
        """Load the dictionary content from a file
            
        dico_path   Path to the dictionary to load
        """
    # ============================================================================

        # Read file content
        with open (dico_path, 'r') as f:
            words = f.readlines ()

        # Remove what is not a letter, if any
        words = [re.sub('[^a-zA-Z]+', '', s) for s in words]
        
        words.extend (["SEIZE", "QUINZE", "DIXSEPT", "DIXHUIT", "DIXNEUF", 
                    "VINGT", "VINGTETUN", "VINGTDEUX", "VINGTROIS", "VINGTQUATRE", 
                    "VINGTCINQ", "VINGTSIX", "VINGTSEPT", "VINGTHUIT", "VINGTNEUF",
                    "TRENTE", "TRENTEETUN", "TRENTEDEUX", "TRENTETROIS", "TRENTEQUATRE", 
                    "TRENTECINQ", "TRENTESIX", "TRENTESEPT", "TRENTEHUIT", "TRENTENEUF",
                    "QUARANTE", "QUARANTEETUN", "QUARANTEDEUX", "QUARANTETROIS", "QUARANTEQUATRE", 
                    "QUARANTECINQ", "QUARANTESIX", "QUARANTESEPT", "QUARANTEHUIT", "QUARANTENEUF",
                    "CINQUANTE", "CINQUANTEETUN", "CINQUANTEDEUX", "CINQUANTETROIS", "CINQUANTEQUATRE", 
                    "CINQUANTECINQ", "CINQUANTESIX", "CINQUANTESEPT", "CINQUANTEHUIT", "CINQUANTENEUF",
                    ])
 
        # Load dictionary
        self.wiz.dic_clear ()
        n = self.wiz.dic_add_entries (words)



        print ("Number of words: ")
        print (" - in file: ", len (words))
        print (" - added: ", n)
        print (" - final: ", self.wiz.dic_gen_num_words ())


