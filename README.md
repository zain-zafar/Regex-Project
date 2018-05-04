# Regex Tree Program 

This program allows user to create regex tree's using valid REGEX inputs. 

  ## PREREQ:
1. Valid Symbols:

	• 0

	• 1

	• 2

	• e  

		If any of these are in the input, a regex tree MAY be formed. 

2. Possible Pathway/Tree:

	• |	(Bar tree)

	• *	(Star tree)	

	• .	(Dot tree)  

		These indicate which tree will be created and 1 of these expressions MUST be between 2 symbols/star. 

3. All the REGEX's MUST be contained in circular brackets.

##
# Valid Examples of Regex Tree 

1. '(1|0)'	The corresponding Object is: BarTree(Leaf('1'), Leaf('2'))

2. '1****'	The Object type: StarTree(StarTree(StarTree(StarTree(Leaf('1')))))

 ##
	