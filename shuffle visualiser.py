#################################################################
#
# Program to help visualize efficiency of different shuffling algorithms
# I wanted to examine the best ways of shuffling a large number of cards,
# when traditional approaches such as bridge shuffling are either difficult
# or inefficient.
# In particular, I had developed an approach to pile shuffling
# (any shuffle involving dealing the cards into piles before recombining)
# which I believed to be very efficient. I set out to quantify why I feel
# this approach is efficient, and I believe the diagrams produced herein
# illustrate these ideas well.
#
# Eden Carrier, 2024
#
# 


import numpy as np
import png
import random as r

# creates a list of colors that range from red to blue over the course of the list
# for a more visually distinguishable look, range is broken into four segments
# which use linear gradients
# n needs to be a multi of 4
def gradient_codex( n ):
    quart = int(n/4)
    codex = []
    for i in range( quart ):
        offset = (255 * i) // quart
        codex.append( (255, offset, 0) )
    for i in range( quart ):
        offset = (255 * i) // quart
        codex.append( (255 - offset, 255, 0) )
    for i in range( quart ):
        offset = (255 * i) // quart
        codex.append( (0, 255, offset) )
    for i in range( quart - 1 ):
        offset = (255 * i) // (quart - 1)
        codex.append( (0, 255 - offset, 255) )
    codex.append( (0, 0, 255) )
    codex.append( (255, 255, 255) )
    codex.append( (0, 0, 0) )
    return codex

# to make this more flexible, specifies a list of colors for the first
# len(codex) values. further values will be set to val % len,
# but are not really intended
# if codex is None, then will use default codex from above
def printimg( grid, filename, colorcodex ):
    height = len(grid)
    width = len(grid[0])
    img = []
    for y in range(height):
        row = ()
        for x in range(width):
            row = row + colorcodex[ int(grid[y,x] % len(colorcodex)) ]
        img.append(row)
    with open( filename, 'wb' ) as f:
        w = png.Writer( width, height, greyscale=False )
        w.write(f, img)

# column indices in a form that allows easily adding labels to the final image for readability
numbers = [[0, 0, 1, 0, 0,  1, 1, 1, 1, 1,  1, 1, 1, 1, 1,  1, 0, 0, 0, 1,  1, 1, 1, 1, 1,  1, 0, 0, 0, 0,  1, 1, 1, 1, 1,  1, 1, 1, 1, 1,  1, 1, 1, 1, 1,  0, 1, 1, 1, 0,  1, 1, 1, 1, 0,  0, 1, 1, 1, 1,  1, 1, 1, 1, 0,  1, 1, 1, 1, 1,  1, 1, 1, 1, 1],
           [0, 1, 1, 0, 0,  0, 0, 0, 0, 1,  0, 0, 0, 0, 1,  1, 0, 0, 0, 1,  1, 0, 0, 0, 0,  1, 0, 0, 0, 0,  0, 0, 0, 0, 1,  1, 0, 0, 0, 1,  1, 0, 0, 0, 1,  1, 0, 0, 0, 1,  1, 0, 0, 0, 1,  1, 0, 0, 0, 0,  1, 0, 0, 0, 1,  1, 0, 0, 0, 0,  1, 0, 0, 0, 0],
           [1, 0, 1, 0, 0,  1, 1, 1, 1, 1,  0, 0, 1, 1, 1,  1, 1, 1, 1, 1,  1, 1, 1, 1, 1,  1, 1, 1, 1, 1,  0, 0, 0, 0, 1,  1, 1, 1, 1, 1,  1, 1, 1, 1, 1,  1, 1, 1, 1, 1,  1, 1, 1, 1, 0,  1, 0, 0, 0, 0,  1, 0, 0, 0, 1,  1, 1, 1, 0, 0,  1, 1, 1, 0, 0],
           [0, 0, 1, 0, 0,  1, 0, 0, 0, 0,  0, 0, 0, 0, 1,  0, 0, 0, 0, 1,  0, 0, 0, 0, 1,  1, 0, 0, 0, 1,  0, 0, 0, 0, 1,  1, 0, 0, 0, 1,  0, 0, 0, 0, 1,  1, 0, 0, 0, 1,  1, 0, 0, 0, 1,  1, 0, 0, 0, 0,  1, 0, 0, 0, 1,  1, 0, 0, 0, 0,  1, 0, 0, 0, 0],
           [1, 1, 1, 1, 1,  1, 1, 1, 1, 1,  1, 1, 1, 1, 1,  0, 0, 0, 0, 1,  1, 1, 1, 1, 1,  1, 1, 1, 1, 1,  0, 0, 0, 0, 1,  1, 1, 1, 1, 1,  0, 0, 0, 0, 1,  1, 0, 0, 0, 1,  1, 1, 1, 1, 0,  0, 1, 1, 1, 1,  1, 1, 1, 1, 0,  1, 1, 1, 1, 1,  1, 0, 0, 0, 0]]

# assembles the various shuffles into a single grid for image processing
# shuffles is a list of arrays
def makeoutgrid( shuffles ):
    n = len(shuffles[0])
    grid = np.zeros(shape=(2*n+5,5*len(shuffles)))
    for i in range(n):
        for j in range(len(shuffles)):
            for a in range(2):
                for b in range(5):
                    grid[2*i + a][5*j + b] = shuffles[j][i]
    for i in range(5):
        for j in range(5*len(shuffles)):
            grid[2*n+i][j] = numbers[i][j] + n  # shift to end of codex
    return grid

# utility function which perfectly shuffles a list, with no regard for physical ability
# used as a baseline for what true randomness "looks like"
def truerand( deck ):
    n = len(deck)
    newdeck = list(np.arange(n))
    for i in range(n):
        choice = r.randint( 1, n - i ) - 1
        a = newdeck.pop(choice)
        newdeck.append(a)
    return newdeck

# utility function used for a couple of different shuffles
# it attempts to do a non-deterministic merge of two similar sized piles
# in order to keep things some what realistic, runs of cards alternate
# between the two piles, but with longer runs becoming increasingly unlikely
# since in practice a decent recombination shouldn't take twenty consecutive cards
# from one pile
def combine( left, right ):
    newdeck = []
    c = 0       # parameter to avoid runs getting too long. reset every switch
    while len(left) > 0 and len(right) > 0:
        val = r.random() + c / 10
        if val < 0.5:
            if c < 0:
                c = 0
            c += 1
            newdeck.append( left.pop(0) )
        else:
            if c > 0:
                c = 0
            c -= 1
            newdeck.append( right.pop(0) )
    while len(left) > 0:
        newdeck.append( left.pop(0) )
    while len(right) > 0:
        newdeck.append( right.pop(0) )
    return newdeck

# splits the deck roughly in half, then calls combine()
# mimics a traditional bridge shuffle
def bridge( deck ):
    n = len(deck)
    split = int( n * r.uniform( 0.45, 0.55 ) )
    left = deck[:split]
    right = deck[split:]
    return combine( left, right )

# divides the deck into count piles
# used as a first step for all pile shuffles
def makepiles( deck, count ):
    n = len(deck)
    piles = []
    for i in range(count):
        piles.append([])
    for i in range(n):
        piles[ r.randint(0, count-1) ].append( deck[n-i-1] )
    return piles

# pile shuffle recombination in which you simply stack the piles
def simplepiles( deck, count ):
    piles = makepiles( deck, count )
    newdeck = []
    for i in range(len(piles)):
        newdeck.extend( piles[i] )
    return newdeck

# pile shuffle recombination in which the piles are "mashed" together
# similar effect to bridging the sub piles
# one of my goals with this is to show that this recombination approach mostly
# defeats the purpose of the pile shuffle, by returning cards to roughly the point
# in the deck they originated from
def pilesbad( deck, count ):
    piles = makepiles( deck, count )
    while len(piles) > 1:
        left = piles.pop(0)
        right = piles.pop(0)
        piles.append( combine(left,right) )
    return piles[0]

# the building block of my method. full description is given below
def halfcombine( top, bottom ):
    n1 = len(top)
    n2 = len(bottom)
    split1 = int( n1 * r.uniform( 0.45, 0.55 ) )
    split2 = int( n2 * r.uniform( 0.45, 0.55 ) )
    topleft = top[:split1]
    topright = top[split1:]
    bottomleft = bottom[:split2]
    bottomright = bottom[split2:]
    newdeck = []
    c = 0
    newdeck.extend( topleft )
    left = bottomleft
    right = topright
    while len(left) > 0 and len(right) > 0:
        val = r.random() + c / 10
        if val < 0.5:
            if c < 0:
                c = 0
            c += 1
            newdeck.append( left.pop(0) )
        else:
            if c > 0:
                c = 0
            c -= 1
            newdeck.append( right.pop(0) )
    while len(left) > 0:
        newdeck.append( left.pop(0) )
    while len(right) > 0:
        newdeck.append( right.pop(0) )
    newdeck.extend( bottomright )
    return newdeck

# pile shuffle recombination of my own design, intended to maximize the entropy of a single shuffle
# only defined for 4 piles currently, as attempts to extend to 8 have not really yielded much benefit
# separate into four piles. called A,B,C,D in this function
# take two of these piles. instead of merging as normal, offset them by half
# say the piles are A and B. the end result has a section of just A, then a section of A and B mixed
# and then a section of just B
# repeat with the other two piles
# finally, cut one of these new piles so the top and bottom halves switch
# then do a tradional merge
# end result moves any card to a fairly arbitrary position in the deck
def edeniscool( deck ):
    piles = makepiles( deck, 4 )
    (A,B,C,D) = (piles[0],piles[1],piles[2],piles[3])
    AB = halfcombine( A, B )
    CD = halfcombine( C, D )
    split = len(AB) // 2
    newAB = []
    newAB.extend( AB[split:] )
    newAB.extend( AB[:split] )
    return combine( newAB, CD )

## metrics ##

# measures how far each card ends from its original position
# since e.g. reversing a deck is not really shuffling
# (and pile shuffles generally flip the deck over while dealing)
# the metric is computed from both the initial deck and a reversed one
# and then the lesser one is reported
def averagedist( deck, shuffle ):
    n = len(shuffle)
    kced = deck.reverse()
    total = 0
    rtotal = 0
    for i in range(n):
        val = shuffle[i]
        total += deck.index(val)
        rtotal += kced.index(val)
    if total < rtotal:
        return total / n
    return rtotal / n

# takes a list of many shuffles done via the same algorithm
# measures the tendency for any given card to end up in any given position
# then averages the square of these values
# if a shuffle tends to e.g. keep cards near the end of the deck they started at,
# this average will be higher
# minimum is realised for a perfectly even distribution
def saturation( shuffles ):
    n = len(shuffles[0])
    counts = np.zeros(shape=(n,n))
    # counts[val][index]
    for i in range(len(shuffles)):
        for j in range(n):
            counts[ shuffles[i][j] ][ j ] += 1
    total = 0
    for i in range(n):
        for j in range(n):
            counts[i][j] /= len(shuffles)
            total += counts[i][j] ** 2
    return total
    

# all actual calls are down here

# assemble list of shuffle candidates
n = 100
deck = list(np.arange(n))
spacer = np.zeros(n)
shuffles = [ deck ]
shuffles.append( truerand(deck) )
shuffles.append( bridge(deck) )
shuffles.append( bridge(bridge(bridge(bridge(bridge(deck))))) )
shuffles.append( spacer )
shuffles.append( simplepiles( deck, 4 ) )
shuffles.append( pilesbad( deck, 4 ) )
shuffles.append( edeniscool( deck ) )
shuffles.append( spacer )
shuffles.append( simplepiles( deck, 8 ) )
shuffles.append( pilesbad( deck, 8 ) )

# create display image
outgrid = makeoutgrid( shuffles )
printimg( outgrid, "decks.png", gradient_codex(n) )


# constructs metrics for a bunch of different shuffles
sats = []

shuffles = []
for i in range(1000):
    shuffles.append( truerand(deck) )
sats.append( saturation( shuffles ) )

shuffles = []
for i in range(1000):
    shuffles.append( bridge(deck) )
sats.append( saturation( shuffles ) )

shuffles = []
for i in range(1000):
    shuffles.append( simplepiles(deck,4) )
sats.append( saturation( shuffles ) )

shuffles = []
for i in range(1000):
    shuffles.append( pilesbad(deck,4) )
sats.append( saturation( shuffles ) )

shuffles = []
for i in range(1000):
    shuffles.append( edeniscool(deck) )
sats.append( saturation( shuffles ) )

print(sats)
