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
        if dico_path: self._load_dictionary (os.path.join (os.getcwd (), dico_path))


    # ============================================================================
    def is_valid_start (self, sentence, can_extend=True):
        """Return if the begining of a sentence make sense, that is, if it
        is made up of several known words. The last word may be incomplete.
        
        return  Minimum number of words in this sentence. 0 if not a valid sentence.
        """        
    # ============================================================================

        slices_list = [[0]]
        progress = 0

        while True:
            slices_list = self._extend_slices (sentence, slices_list, can_extend)
            if len (slices_list) == 0: return False
            new_progress = max ([slices [-1] for slices in slices_list])

            if len (sentence) <= new_progress :
                for slices in slices_list:
                    if slices [-1] == new_progress: 
                        return len (slices) -1

            if new_progress <= progress:
                return 0

            progress = new_progress


    # ============================================================================
    def is_valid_word_start (self, pattern):
        """Return True is the word given is the begining of any word in the dictionary"""
    # ============================================================================
        
        n = len (pattern)
        while n < 16:
            entry = self.wiz.dic_find_entry (pattern)
            if entry is not None: return True
            n += 1
            pattern = pattern + '*'

        return False

   # ============================================================================
    def is_valid_word (self, word):
        """Return True is the word is in the dictionary"""
    # ============================================================================
        entry = self.wiz.dic_find_entry (word)
        return entry is not None


     # ============================================================================
    def _extend_slices (self, sentence, slices_list, can_extend=False):
    # ============================================================================

        max_extention = 10
        possible_start_pos = [slices [-1] for slices in slices_list]
        new_slices_list = []

        for slices in slices_list:

            pos_start = slices [-1]
            pos_end = pos_start +1
            extention = ''
           
            while pos_end <= len (sentence) + len (extention):
               
                # Find a match for this sub string
                word = sentence [pos_start: pos_end] + extention
                if pos_end - pos_start > 1:
                    entry = self.wiz.dic_find_entry (word)
                elif word in ['A', 'C', 'J', 'N', 'S', 'M', 'T', 'L', 'Y']:
                    entry = word
                else: entry = None

                # Add this valid end to our list
                if entry is not None:
                    length = (pos_end-pos_start)
                    if pos_end not in possible_start_pos: 
                        new_slices = list (slices)
                        new_slices.append (pos_end)
                        new_slices_list.append (new_slices)
                    pos_end += 1

                # Keep searching with longer words
                elif len (extention) < 10:
                    pos_end += 1
                    if pos_end > len (sentence) and can_extend:
                        extention += '*'

                # Or give up
                else: break
        
        return new_slices_list
        


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


