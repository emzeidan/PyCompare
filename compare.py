#! /usr/bin/env python

""" A simple metric to compare two translation strings.

    There are already a lot of statistical measures for similarity of
    machine translations. I decided to write something that just "looks"
    at a translation, the same way that a human translator might do a
    first pass glance at a pair of comparisons.

    "Where do words line up? And do words even line up?"

    This measure simply shows how many words do not line up in this pair
    of translations -- from 0.000 (none) to 1.000 (all)

    USAGE: ./compare.py <human translation> <machine translation>
    
        (C) 2012 Elias Zeidan

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""
import sys, string
from nltk.tokenize import *

def add_filler(sent1, sent2):
    """ Adds filler word "blah" to even out sentence lengths.
        Sent1 is the longer sentence.
        >>> add_filler(["hello", "this", "is", "a", "test", "sentence"], \
                        ["hello", "this", "is", "a", "test"])
        ['hello', 'this', 'is', 'a', 'test', 'blah']
    """
    difference = len(sent1) - len(sent2)
    for i in range(difference):  
        sent2.append("blah")         
    return sent2

def only_lower(input):
    """ Return copy of input with only 0 - 9, a - z characters.
        >>> only_lower("hello.")
        'hello'
    """
    intab = string.uppercase
    outtab = string.lowercase
    trantab = string.maketrans(intab, outtab)
    return str(input.translate(trantab, string.punctuation))

def compare(human, machine):
    """ Compares lowercase sentences with punctuation removed.
        >>> compare("Hello there, big guy", "Hey, big man!")
        human translation: Hello there, big guy
        machine translation: Hey, big man!
        'Comparison index: 1.000'

        >>> compare("Hello there, big guy", "Hey there, big man!")
        human translation: Hello there, big guy
        machine translation: Hey there, big man!
        'Comparison index: 0.500'

        >>> compare("a, b c d!", "a, b b, c d!")
        human translation: a, b c d!
        machine translation: a, b b, c d!
        'Comparison index: 0.600'
    """
    human_lower = str(only_lower(human))
    machine_lower = str(only_lower(machine))
    # print "--DEBUG: Lowercase sentences:\n -Human: %s \
    # \n -Machine %s" %(human_lower, machine_lower)

    human_token = word_tokenize(human_lower)
    machine_token = word_tokenize(machine_lower)
    # print "--DEBUG: Tokenized sentences:\n -Human: %s \
    # \n -Machine %s" % (human_token, machine_token)
    
    total_unmatched = 0     
    if len(human_token) != len(machine_token):
	# print "--DEBUG: Sentence length:\n -Human: %d \
        # \n -Machine %d" %(len(human_token), len(machine_token))
	if len(human_token) > len(machine_token):
        	machine_token = add_filler(human_token, machine_token)     
    	else:
        	human_token = add_filler(machine_token, human_token)
    # print "--DEBUG: Sentences after filler:\n -Human: %s \
    # \n -Machine %s" %(human_token, machine_token)
    for i in range(min(len(human_token), len(machine_token))):         
        if human_token[i] != machine_token[i]:
            # print "--DEBUG: Non-matches:\n -human_token[i]: %s \
            # \n -machine_token[i] %s" %(human_token[i], machine_token[i])
            total_unmatched += 1
    print "human translation: %s" % human
    print "machine translation: %s" % machine     
    return "Comparison index: %.3f" %(float(total_unmatched)/len(human_token))

def compare2(human, machine):
    human_lower = str(only_lower(human))
    machine_lower = str(only_lower(machine))
    # print "--DEBUG: Lowercase sentences:\n -Human: %s \
    # \n -Machine %s" %(human_lower, machine_lower)

    human_token = word_tokenize(human_lower)
    machine_token = word_tokenize(machine_lower)
    # print "--DEBUG: Tokenized sentences:\n -Human: %s \
    # \n -Machine %s" % (human_token, machine_token)

    # print "--DEBUG Length of translations: \n -Human: %d \n -Machine: %d" \
    #     % (len(human_token), len(machine_token))

    index = 0
    print "Index    Word"
    for word in human_token:
        print "%d    %s" % (index, word)
        
def main():
    print compare(human, machine)

if __name__ == "__main__":
    human = str(sys.argv[1])
    machine = str(sys.argv[2])
    main()
