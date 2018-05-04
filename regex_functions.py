"""
# Copyright Nick Cheng, Brian Harrington, Danny Heap, 2013, 2014, 2015, 2016
# Distributed under the terms of the GNU General Public License.
#
# This file is part of Assignment 2, CSCA48, Winter 2016
#
# This is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This file is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this file.  If not, see <http://www.gnu.org/licenses/>.
"""

# Do not change this import statement, or add any of your own!
from regextree import RegexTree, StarTree, DotTree, BarTree, Leaf

# Do not change anything above this comment except for the copyright
# statement

# Student code below this comment.

zero = '0'
one = '1'
two = '2'
epsilon = 'e'
bar = '|'
dot = '.'
star = '*'
left_p = '('
right_p = ')'
number_one = 1


def is_regex(string):
    '''(str) -> Bool

    >>> is_regex('1****')
    True

    >>> is_regex('(1.0)')
    True

    >>> is_regex('1.0')
    False

    >>> is_regex('(1*********************.2)**')
    True

    >>> is_regex('3')
    False

    >>> is_regex('((1.0)*|4)')
    True
    '''
    # If a empty string is entered, return False
    if len(string) == 0:
        return False
    # Check for Case 2: which is if length of str is 1, then the str should
    # only contain zero, one, two, or epsilon.
    if len(string) == number_one:
        # if string contains zero, one, two, or epsilon, then return True
        if string in [zero, one, two, epsilon]:
            return True
        # if string does not contain zero, one, two, epsilon, return False
        else:
            return False
    # If the string contains a star
    elif star in string:
        # Find the star's index:
        star_index = string.find(star)
        # if the string starts with a star, return false, as this is invalid
        if string[0] == star:
            return False
        # if the string contains a star, whose value is 0,1,2,e,), then
        # replace that star, as it will not effect the regex.
        elif string[star_index - 1] in \
        [zero, one, two, epsilon, star, right_p]:
            string = string.replace(star, '', 1)
        # if anything else is found, then not a proper regex, so return False
        else:
            return False

    elif (dot in string or bar in string) and \
         (left_p in string and right_p in string):
        # find the left most bracket
        left_p_index = string.rfind(left_p)
        # check the next index, which must be a length regex.
        if (string[left_p_index + 1] in [zero, one, two, epsilon]) \
            and (string[left_p_index + 2] in [bar, dot]) \
            and (string[left_p_index + 3] in [zero, one, two, epsilon]):

            # the right bracket must be 4 index after, if its not,
            # then return false
            if string[left_p_index + 4] == right_p:
                # set the right_p_index
                right_p_index = (left_p_index + 4)
                # check if the regex operator inside the brackets is a bar
                # or dot
                if string[left_p_index + 2] in [bar, dot]:
                    # Now, since from the left bracket to the right
                    # corresponding bracket is a valid regex, replace it by 1,
                    # which allows to slowly break the regex into valid pieces
                    # recursively
                    string = string[0: left_p_index] + '1' \
                        + string[right_p_index + 1:]
                else:
                    return False
            else:
                return False
    else:
        return False

    return is_regex(string)


def all_regex_permutations(string):
    '''(str) -> set
    REQ: string is not empty

    >>> all_regex_permutations('1**')
    {'1**'}

    >>> all_regex_permutations('1')
    {'1'}

    >>> all_regex_permutations('4')
    set()

    Return a set of permutations of all valid regex's of string.
    If set is empty, then no regex permutation was valid.
    '''
    # Create a set which will store all the final permutations in it
    hold_perms = set()
    # this gets the list of the all the permutations
    check = perms(string)
    # now check if each element in the list a proper regex or not
    for element in check:
        # If the string is a valid regex, then store it in a set
        if is_regex(element):
            # Then add it to our set
            hold_perms.add(element)
    # Return the set
    return hold_perms


def perms(string):
    '''(str) -> set
    REQ: length of string is greater than 0

    >>> perms('ap')
    {'pa', 'ap'}

    >>> perms('zain')
    {'niza', 'izan', 'inaz', 'aniz', 'nzai', 'izna', 'ainz', 'zian', 'znia',
    'anzi', 'azni', 'azin', 'naiz', 'znai', 'iazn', 'inza', 'nzia', 'nazi',
    'zina', 'zani', 'niaz', 'ianz', 'zain', 'aizn'}

    >>> perms('ok')
    {'ok', 'ko'}

    >>> perms('aab')
    {'aab', 'aba', 'baa'}

    >>> perms('aaa')
    {'aaa'}

    Return the total number of possible computations/permutations of the
    string in a set. The set will remove all the duplicates.
    '''
    # Keep reducting the string, until it reaches base case of 1
    # return the string
    if len(string) == 1 and is_regex(string) == True:
        return {string}
    # Base case can be 1 or less than 1
    # return the string
    if len(string) < 1:
        return {string}
    # Initialize for finding permutations
    # get each first element of the string and put it into remaining
    # words in all possible ways
    final, things_changed, first_word = list(), perms(string[1:]), string[0]
    # Starting from the end, take each element and make all possible perms
    for changes in things_changed:
        # append the word taken word into the words in each possible way
        # this way the number of permutations are formed
        for counter in range(len(changes) + 1):
            final.append(changes[counter:] + first_word + changes[:counter])

    # Turn the list into a set, this way all the duplicates are removed
    # and the permutations are now stored in a set
    return final


def regex_match(regex, string):
    '''(RegexTree, str) -> Bool
    REQ: Valid Regex tree is made

    >>> a = build_regex_tree('(1.0)')
    >>> regex_match(a, '10')
    True

    >>> a = build_regex_tree('1****')
    >>> regex_match(a, '')
    True
    >>> regex_match(a, '2')
    False
    >>> regex_match(a, '1')
    True
    >>> regex_match(a, '111111')
    True

    >>> a = build_regex('(1|2)')
    >>> regex_match(a, '1')
    True
    >>> regex_match(a, '0')
    True
    >>> regex_match(a, '12')
    False

    >>> a = build_regex_tree('(1|1)')
    >>> regex_match(a, '1')
    True
    >>> regex_match(a, '11')
    False

    Return True, iff regex matches the given string. Each tree, star,bar,dot,
    Leaf tree, there are certain rules that can be applied in order to generate
    string(s) which might match string.
    '''
    # Make a list of possible strings which match string
    possible_matches = []
    # check if the regex has any children
    children = regex.get_children()
    symbol = []
    # if children is equal to 1, that means the redex must be a leaf
    if len(children) == 1:
        # Find the symbol
        symbol = children[0].get_symbol()
        # if the length of children is 1, check if symbol is equal to bar
        if symbol in [bar, dot]:
            return regex_match(children[0], string)

        # if the symbol is equal to star
        elif symbol == star:
            try:
                # check if the regex contains more stars
                possibility = regex_match1(children[0], string)
                # print(possibility)
                possible_matches.append('')
            except:
                return True
        # if the symbol is a leaf of 0,1,2, append into list of possibilities
        elif symbol in [zero, one, two]:
            # append the symbol once
            possible_matches.append(symbol)
            # append the symbol endless times to ensure, that if a star is used
            # then that number shows up many times
            possible_matches.append(symbol*50)
        # if symbol is a leaf of e
        else:
            # append empty string, as e is equal to ''
            possible_matches.append('')
            # return True iff string lies in possible_matches
            return string in possible_matches

    # if children is not equal to 1, then a dot or bar tree are being used
    if len(children) == 2:
        symbol = regex.get_symbol()
        # get the 2 leafs
        leaf_one = children[0].get_symbol()
        leaf_second = children[1].get_symbol()
        # if the symbol is a bar, then the possible list will be
        # the leaf + leaf
        if symbol == bar:
            # if the leafs are the same, then just append 1 leaf to the list
            if leaf_one == leaf_second:
                possible_matches.append(leaf_one)
            # if the leafs are different
            else:
                # append both leafs as they are both valid cases for a bar
                possible_matches.append(leaf_one)
                possible_matches.append(leaf_second)

            # Since 2 children exist, if they have no children, then
            # there can be no more results, so compare string to possiblities.
            if children[0].get_children() == [] and \
               children[1].get_children() == []:
                return string in possible_matches
       # The only possible symbol will be a dot
        else:
            possible_matches.append((leaf_one + leaf_second))
            # Since 2 children exist, if they have no children, then
            # there can be no more results, so compare string to possiblities.
            if children[0].get_children() == [] and \
               children[1].get_children() == []:
                return string in possible_matches

    # Just to catch a few errors, if the string is made up of the maximum
    # value in the list, then return true
    if string in str(max(possible_matches)):
        return True
    else:
        # Compare the string to check if any values from possible_matches match
        return string in possible_matches


def build_regex_tree(regex):
    '''(str) -> RegexTree
    REQ: A valid regex as string is given

    >>> build_regex_tree('1*')
    StarTree(Leaf('1'))

    >>> build_regex_tree('1**')
    StarTree(StarTree(Leaf('1')))

    >>> build_regex_tree('(1.0)')
    DotTree(Leaf('1'), Leaf('0'))

    >>> build_regex_tree('(1.0)**')
    StarTree(StarTree(DotTree(Leaf('1'), Leaf('0'))))

    >>> build_regex_tree('(1.(0.1))**')
    StarTree(StarTree(DotTree(Leaf('1'), DotTree(Leaf('0'), Leaf('1')))))

    Return a RegexTree made of the given regex.
    '''
    # use the helper function to breakdown the regex, into a list, which
    # contains parent, left_child, and right_child of the regex
    list_of_tree = break_down(regex)
    # If the length of the tree is 1, then only root exist
    if len(list_of_tree) == 1:
        # There list_of_tree[0] must be a tree
        return Leaf(list_of_tree[0])
    # if the length of list_of_tree is 2, then this could be a star tree
    elif len(list_of_tree) == 2:
        # If the first element of list_of_tree is a star, then the
        # next value in list will be a leaf
        if list_of_tree[0] == star:
            if len(list_of_tree[1]) == 1:
                # return a starTree with leaf of list_of_tree[1]
                return StarTree(Leaf(list_of_tree[1]))
            # if the length of first element is not, then break it down
            # more
            else:
                return StarTree(build_regex_tree(list_of_tree[1]))
    # Check if the first element is a list
    # checking the length of all the other elements we can figure out
    # whether or not to break it down further.
    # this allows us to build a dot tree
    elif list_of_tree[0] == dot:
        # If length of any element 1 or 2, is greater than 1, then break it
        # down further with parent as dot tree
        # if length of any element is 1, then it is a leaf child.
        if len(list_of_tree[1]) == 1 and len(list_of_tree[2]) == 1:
            return DotTree(Leaf(list_of_tree[1]), Leaf(list_of_tree[2]))

        elif len(list_of_tree[1]) > 1 and len(list_of_tree[2]) == 1:
            return DotTree(build_regex_tree(list_of_tree[1]), \
                           Leaf(list_of_tree[2]))

        elif len(list_of_tree[1]) == 1 and len(list_of_tree[2]) > 1:
            return DotTree(Leaf(list_of_tree[1]), \
                           build_regex_tree(list_of_tree[2]))

        elif len(list_of_tree[1]) > 1 and len(list_of_tree[2]) > 1:
            return DotTree(build_regex_tree(list_of_tree[1]), \
                           build_regex_tree(list_of_tree[2]))
    # Check if the first element is a list
    # checking the length of all the other elements we can figure out
    # whether or not to break it down further.
    # this allows us to build a bar tree
    elif list_of_tree[0] == bar:
        # if the length of element 1 or 2 in list_of_tree is 1, then
        # it is a leaf of the BarTree, if length is greater than 1,
        # break it down until it reaches length of 1.
        if len(list_of_tree[1]) == 1 and len(list_of_tree[2]) == 1:
            return BarTree(Leaf(list_of_tree[1]), Leaf(list_of_tree[2]))

        elif len(list_of_tree[1]) > 1 and len(list_of_tree[2]) == 1:
            return BarTree(build_regex_tree(list_of_tree[1]), \
                           Leaf(list_of_tree[2]))

        elif len(list_of_tree[1]) == 1 and len(list_of_tree[2]) > 1:
            return BarTree(Leaf(list_of_tree[1]), \
                           build_regex_tree(list_of_tree[2]))

        elif len(list_of_tree[1]) > 1 and len(list_of_tree[2]) > 1:
            return BarTree(build_regex_tree(list_of_tree[1]), \
                           build_regex_tree(list_of_tree[2]))


def break_down(regex):
    '''(str) -> list
    REQ: A string of a valid regex form is inputted

    >>> a = break_down('1*')
    >>> print(a)
    ['*', '1']

    >>> a = break_down('((1.2)**.1)')
    >>> print(a)
    ['.', '(1.2)**', '1']

    >>> a = break_down('(1.0)')
    >>> print(a)
    ['.', '1', '0']

    >>> a = break_down('(1|0)')
    >>> print(a)
    ['|', '1', '0']

    Return a list which contains at most 3 elements, where the first element
    is the parent of the regex, and the 2nd element is the left child, and
    the 3rd element is the right child.

    For regex's which contains more than 1 pair of brackets, this
    function recursively breaks down the regex until the regex cannot
    be simplified further
    '''
    # Initialize a counter
    counter = 0
    # If the regex is None, then return a list as none.
    if regex is None:
        return [None]
    # if the length of the regex is 1, then return the parent of the regex
    # in a list
    if len(regex) == 1:
        return [regex]

    # If 1 pair of brackets exist
    if left_p in regex and right_p in regex:
        # find the first left bracket and the corresponding last bracket
        left_p_index = regex.find(left_p)
        right_p_index = regex.rfind(right_p)

        # if more pairs of brackets lie inside the first pair of brackets
        if left_p in regex[left_p_index + 1: right_p_index] and \
           right_p in regex[left_p_index + 1: right_p_index]:

            # But first Check if the last right parenthesis has a
            # star after it:
            if regex[len(regex) - 1] == star:
                # if a star exist, then make it the parent and everything
                # after it a left_child
                return [regex[len(regex) - 1], regex[:len(regex)-1]]
            # If no star exists after the right bracket, then set regex
            # equal to the the inside of those brackets
            regex = regex[left_p_index + 1: right_p_index]
            # check if the first element is a left bracket
            if regex[0] == left_p:
                # if so, then find the corresponding right bracket
                left_child_index = regex.find(right_p)
                # Check if a star or right_parenthesis lies after the
                # right bracket
                # if it is, then keep moving through the
                # string, until a bar or dot is not found.
                # Save the index of bar or star, which is the root of the tree
                if regex[left_child_index + 1] in [star, right_p]:
                    counter = (left_child_index + 1)
                    while ((regex[counter] is not dot) and \
                           (regex[counter] is not bar)):
                        counter += 1

                else:
                    # get the bar or dot from from the regex
                    bar_or_dot = regex[left_child_index + 1]
                    # Set the bar/dot as the parent, and everything before it
                    # as the left child and before it as the right child
                    return [bar_or_dot, regex[0: (left_child_index + 1)], \
                            regex[(left_child_index + 2):]]

            elif regex[0] in [zero, one, two, epsilon]:
                # if the next value is a star, then keep moving until a bar
                # or dot is not found
                counter = 1
                if regex[1] == star:
                    while ((regex[counter] is not dot) and \
                           (regex[counter] is not bar)):
                        counter += 1
            # set the root as the found dot/bar index
            # set everything before the parent as left_child and everything
            # after it as the right child
            root = regex[counter]
            right_child_index = regex[counter + 1:]
            return [root, regex[0:counter], right_child_index]

        # If only 1 pair of brackets exist
        else:
            # if bar/dot and star lie in regex, then:
            if (bar in regex or dot in regex) and (star in regex):
                # Find the right bracket index
                right_p_index = regex.find(right_p)
                last_star_index = regex.rfind(star)

                # if last star idex is greater than right_p index:
                if last_star_index > right_p_index:
                    parent = regex[last_star_index]
                    child = regex[:last_star_index]
                    return [parent, child]

            # find dot in regex if it exists
            if dot in regex:
                bar_or_dot_index = regex.find(dot)
                # find the left child, right child, and root.
                left_child = regex[1:bar_or_dot_index]
                root = regex[bar_or_dot_index]
                right_child = regex[(bar_or_dot_index + 1):-1]
                return [root, left_child, right_child]

            # find bar in regex
            elif bar in regex:
                bar_or_dot_index = regex.find(bar)
                # find the left child, right child, and root.
                left_child = regex[1:bar_or_dot_index]
                root = regex[bar_or_dot_index]
                right_child = regex[(bar_or_dot_index + 1):-1]
                return [root, left_child, right_child]

            # if star exists
            elif star in regex:
                right_child = None
                root_index = regex.find(star)
                left_child = regex[:root_index]
                return [regex[root_index], left_child, right_child]

    # if no brackets exist, then
    else:
        # if its a redex of length 1, then it will be a leaf root
        if len(regex) == 1:
            root = regex
            return [root]
        # if length is not 1, then it will have star(s)
        else:
            last_star_index = regex.rfind(star)
            root = regex[last_star_index]
            left_child = regex[:last_star_index]
            return [root, left_child]
