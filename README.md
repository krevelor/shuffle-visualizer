# shuffle-visualizer
### A program to demonstrate the efficiency of different shuffling techniques

When shuffling a large number of cards, traditional approaches such as bridge shuffling are generally difficult and/or inefficient. A common approach to this fact is to perform a pile shuffle, where in the deck is dealt out into a few piles at random, then recombined in some fashion. While this can be fairly effective, it's also generally quite time consuming, and so I wanted to optimize things.

After spending some time considering different ways of going about it, I figured out an approach to pile shuffling recombination which is much better at increasing entropy in a single pass than the "obvious" ways to go about it. In addition, I came to the realization that the most common way I was seeing people go about it - taking the piles and simply "mashing" them back together to interleave them - was actually tremendously inefficient. In short, if a card is near the top of the deck before shuffling, it ends up near the bottom of whichever pile it ends up in. If the piles are then interleaved naively, it will end up necessarily near the bottom of the deck - and so will every other card near the top beforehand. In fact, while somewhat counterintuitive, simply stacking the piles back up makes for a far better shuffle than mashing does.

My approach, which uses offset recombinations, leads to a much more shuffled deck after a single shuffle. It's a bit difficult to describe in text (the code may even be more understandable haha), but the general idea is:
 - deal into four piles
 - take two of the piles, call them A and B. Interleave A and B so that they are halfway offset. That is to say that the end result should be, from top to bottom, about half of A, then half of A mixed with half of B, then the other half of B
 - Do the same with the other two piles
 - Cut one of the combined piles and swap the halves
 - Recombine them in the standard, aligned way
As this program demonstrates, this results in a shuffle where the tendency for a particular card to go to a particular spot, as well as the tendency for clumped cards to stay clumped, are both minimized.

However, as this readme is no doubt demonstrating, getting across exactly *why* this shuffle is good (and the simple recombination is bad) is quite difficult with words, and is generally fairly abstract. To that end, I created this program to show visually the ideas I'm presenting here. Included with the program is an example output. 

The general idea is that the program assigns each card in the deck a color along a gradient, so that when shuffled you can see roughly which part of the deck each card started in. The various columns represent various different shuffling procedures. Of note, column 2 is a true random shuffle, as an example of what a proper shuffle is striving to look like. 6, 7, and 8 are the main purpose, as they represent the three kinds of pile shuffles talked about here - stacking the piles, simple reombination, and my complicated recombination, respectively. From this you can see that column 7 is actually quite similar to the starting gradient, but with the order reversed. Column 6 has high clumping, but makes it less obvious where a particular card will end up in the deck. And column 8 has much less clumping, as well as making it very unclear what part of the deck any particular card may end up in. 

The program also makes some measurements of the above ideas quantitatively, over many shuffles, to make the ideas presented here more concrete.
