import re
import numpy as np

def product(ar_list):
    """
    A recursive generator for the Cartesian product of lists.
    
    Args:
        ar_list - a list of lists
    
    """
    if not ar_list:
        yield ()
    else:
        for a in ar_list[0]:
            for prod in product(ar_list[1:]):
                yield (a,)+prod    

def highlight_sentence(sentence, query):
    """
    Given a sentence, wrap [[HIGHLIGHT]] and [[ENDHIGHLIGH]] 
    tags around the query terms.  
    
    Args:
        sentence - string in which highlighting occurs
        query - list of words to be highlighted
    
    Returns:
        sentence, after wrapping highlight tags around given query terms
    """
    # replace whitespace with | in query string
    query = (' ').join(query)
    terms = re.sub('\s+', '|', query)
    regex = re.compile(r'(\s*)((?:\b\s*(?:%s)(es|s)?\b)+)' % terms, re.I)
    return regex.sub(r'\1[[HIGHLIGHT]]\2[[ENDHIGHLIGHT]]', sentence)


def highlight_doc(doc, query):
    """
    Select to display the most relevant snippet that contains all query words.
    Highlight all query words in the snippet. 
    
    Args:
        doc - String that is a document to be highlighted
        query - String that contains the search query
    
    Returns:
        The most relevant snippet with the query terms highlighted.
    """
    
    # scrub punctuation from query 
    query = re.findall(r'\w+', query)
    
    # init a list M whose kth element is a list
    # containing the match locations in doc
    # of the kth query term
    M = []
    for term in query:
        # try to deal with basic plurals, but avoid
        # matching unrelated substrings of words
        # e.g., cat in catatonic
        pattern = '%s(es|s)?' % term
        term_match = re.finditer(pattern, doc, re.IGNORECASE)
        term_leftidx = [match.span()[0] for match in term_match]
        if term_leftidx == []:
            return 'Search terms not found in doc'
        M.append(term_leftidx)
    
    # create a list of tuples from the sets in M  
    T = list(product(M))
    
    # D contains the lengths of the substrings
    D = np.array([max(item) - min(item) for item in T])
    
    # extract the index of the first tuple with minimal length
    # This is easy to do without NumPy, incidentally.
    min_idx = np.argmin(D)
    
    # obtain the bounds in doc on the desired substring
    bounds = list(T[min_idx])
    bounds.sort()
    
    # create a list of the left index of each word in doc
    # ignores punctuation, which can cause problems
    # for words like p!zza.
    words_match = re.finditer(r'\w+', doc)
    word_leftidx = [word.span()[0] for word in words_match]
    
    # epsilon is the amount of buffer words to the left and right
    # of the substring to include in order to obtain the
    # relevant snippet from doc
    epsilon_left = 3
    epsilon_right = 10
    
    # obtain the word indices of the word epsilon units to 
    # either side of the substring, assuming these words exist
    left = max(word_leftidx.index(bounds[0])-epsilon_left, 0)
    right = min(word_leftidx.index(bounds[-1])+epsilon_right, len(word_leftidx)-1)
    start = word_leftidx[left]
    end = word_leftidx[right]
    
    # If the boundary of the relevant snippet is close enough to the
    # start or end of a review, include more.
    l = len(doc)
    if l - end < 20:
        end = l
    if start < 20:
        start = 0

    
    # create the snippet to pass to highlight_sentence
    sentence = doc[start:end]
    
    result = highlight_sentence(sentence, query)
    return result
  

if __name__ == "__main__":
 
    # some tests 
    print highlight_doc("These...are...good -- and tasty! -- apples.", "tasty apple")
    print highlight_doc("herr dr. herr dr. schlaenker, come quick!", "Dr Schlaenker")
