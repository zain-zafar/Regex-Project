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

1. '(1|0)'	  The corresponding Object in memory: BarTree(Leaf('1'), Leaf('2'))

2. '1****'	  The Object in memory: StarTree(StarTree(StarTree(StarTree(Leaf('1')))))

 ##
	
```html
<h2>Example of code</h2>

<pre>
    <div class="container">
        <div class="block two first">
            <h2>Your title</h2>
            <div class="wrap">
            //Your content
            </div>
        </div>
    </div>
</pre>
```