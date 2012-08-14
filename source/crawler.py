# File: crawler.py
# Domain web crawler with searching
import urllib2, re, time 

# Returns source code from url (changes all characters to lowercase)
def get_page_source(link):
    try:
        return urllib2.urlopen(link).read().lower()
    except Exception:
        return ""

# Returns list containing all links found from page source
def find_links(source, domain, visited, unvisited):
    linkpattern = re.compile('(?<=<a href=")http[^"]+')
    links_found = re.findall(linkpattern, source)
    new_links = []
    for l in links_found:
        if "#" in l:
            p = l.find("#")
            l = l[:p]
        if l.endswith('/'):
            l = l[:-1]
        if domain in l and l not in new_links:
            new_links.append(l)
    return new_links

# Crawls seed page up to depth of max_depth, limit crawl to domain
# Returns a dictionary containing keywords and its urls
def web_index_crawler(seed, max_depth, limit=True):
    search_index = {}
    web_graph = {}
    visited   = []
    unvisited = [seed]
    current_depth  = 0
    current_branch = 0
    current_seeds = len(unvisited)-1
    # Limit web crawler to seed domain
    domain = ""
    if limit:
        domain = re.search(R'\.\w+\.', seed).group().strip('.')
    while unvisited:
        try:
            if current_depth > max_depth:
                break
            url = unvisited.pop(0)
            web_graph[url] = []
            print "Crawling: %s" % url
            visited.append(url)
            source_code = get_page_source(url)
            links_found = find_links(source_code, domain, visited, unvisited)
            index_page(search_index, url, source_code)
            for u in links_found:
                if u not in visited and u not in unvisited:
                    unvisited.append(u)
                web_graph[url].append(u)
            if current_branch < current_seeds:
                current_branch += 1
            else:
                current_branch = 0
                current_seeds = len(unvisited)-1
                current_depth += 1
        except Exception:
            pass
    return search_index, web_graph

# Takes in source code are returns all words not in tags
def html_get_words(source):
    words = []
    s, t = 0, 0
    while True:
        t = source.find(">", s)
        s = source.find("<", t)
        keywords = source[t+1:s].split()
        for i in keywords:
            if i not in words:
                words.append(i)
        if s == -1:
            break
    return words

# Adds all keywords in source content to index, removing punctuation
def index_page(index, url, content):
    source_contents = html_get_words(content)
    keywords = []
    for i in source_contents:
        if i.isalnum() and i not in keywords:
            keywords.append(i)
        elif not i.isalnum():
            w = i.strip('!?.,;:')
            if len(w) > 0:
                keywords.append(w)
    for word in keywords:
        if word not in index:
            index[word] = [url]
        elif url not in index[word]:
            index[word].append(url)

# Returns associated urls with keyword
def lookup(index, keyword):
    try:
        return index[keyword]
    except Exception:
        return []

def quicksort(n):
    size = len(n)
    if size <= 1:
        return n
    # Choose pivots, make list of partitions
    pivot = [n[0]]
    left  = []
    right = []
    for i in n:
        value = i[1]
        # Add to smaller partition
        if value < pivot[0][1]:
            left.append(i)
        # Add to larger partition
        elif value > pivot[0][1]:
            right.append(i)
    # Recursive quicksort of left and right partitions
    left = quicksort(left)
    right = quicksort(right)
    # Returns sorted 2-dimension list of urls and ranking
    ranking = left + pivot + right
    return ranking
    
def compute_ranks(graph):
    d = 0.8 # damping factor
    numloops = 8
    ranks = {}
    npages = len(graph)
    for page in graph:
        ranks[page] = 1.0 / npages
    for i in range(0, numloops):
        newranks = {}
        for page in graph:
            newrank = (1 - d) / npages
            for node in graph:
                if page in graph[node]:
                    newrank = newrank + d * (ranks[node] / len(graph[node]))
            newranks[page] = newrank
        ranks = newranks
    return ranks

# Returns list containing urls sorted in highest to lowest ranking
def ordered_search(index, ranks, keyword):
    keywords = keyword.split()
    urls = []
    for k in keywords:
        if k not in index:
            return []
    for word in keywords:
        links = index[word]
        for i in links:
            if i not in urls:
                urls.append([i,ranks[i]])
    sorted_ranks = quicksort(urls)
    urls = []
    for i in reversed(sorted_ranks):
        urls.append(i[0])
    return urls

# Test functions
def test_crawler():
    filename = 'links'
    # Sample seed links
    hstat = "http://www.hstat.org"
    udacity = "http://www.udacity.com/cs101x/index.html"
    xkcd = "http://www.xkcd.com"
    python = "http://docs.python.org/index.html"
    depth = 2
    print "Starting web crawler...\n"
    
    # Start web crawler
    start_time = time.clock()
    index, network = web_index_crawler(udacity, depth, True)
    rankings = compute_ranks(network)
    
    print "\nWeb crawler complete."
    # Computation time for session
    print "Running time: %.5f sec" % (time.clock()-start_time)
    print "Permitting searches. Enter 'q' to quit."
    
    # Loop lookup until user quits
    while True:
        try:
            # Enter q to quit
            keyword = raw_input("\nEnter search: ").lower()
            if keyword == 'q':
                print "\nSearch complete."
                break
            start = time.clock()
            results = ordered_search(index, rankings, keyword)
            print "Found %d results in %.5f sec" % (len(results), time.clock()-start)
            for link in results:
                print link
        except Exception:
            pass
    
def main():
    test_crawler()
    
main()