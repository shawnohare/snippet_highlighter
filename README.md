This is a very simple prototype program using regular expressions
and NumPy to highlight a relevant search query snippet from a document.

We find the first instance of a minimal length substring
from the document that contains all the query terms.  This substring
is deemed the most relevant.  We return a snippet
that consists of the substring and a certain fixed number
of buffer words to the left and right of the substring, in order
to achieve some context and also avoid the rather
complex NLP problem of determining sentence boundaries.
Moreover, this approach robustly deals with anomalous
sentence structures that pervade the Net, at
the expensive of aesthetic perfection.

Suppose that the search query contains m words.
Then to find the minimal substring in doc containing
the query terms, we find all sorted m-tuples consisting
of the match locations for the m query terms, one entry
in each tuple per query term.  
When this set of tuples is lexicographically ordered,
we can obtain an ordered list of substrings and compute
the lengths of these substrings, allowing us to
extract the first instance of a minimal length
substring containing all the query terms, as desired.