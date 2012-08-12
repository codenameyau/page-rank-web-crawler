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
            if l not in visited and l not in unvisited:
                new_links.append(l)
    return new_links

# Crawls seed page up to depth of max_depth, limit crawl to domain
# Returns a dictionary containing keywords and its urls
def web_index_crawler(seed, max_depth, limit=True):
    search_index = {}
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
            url = unvisited.pop(0)
            print "Crawling: %s" % url
            if current_depth > max_depth:
                break
            visited.append(url)
            source_code = get_page_source(url)
            links_found = find_links(source_code, domain, visited, unvisited)
            index_page(search_index, url, source_code)
            for u in links_found:
                unvisited.append(u)
            if current_branch < current_seeds:
                current_branch += 1
            else:
                current_branch = 0
                current_seeds = len(unvisited)-1
                current_depth += 1
        except Exception:
            pass
    return search_index

# Adds all keywords in source content to index
def index_page(index, url, content):
    source_contents = content.split()
    keywords = []
    for i in source_contents:
        if i.isalnum():
            keywords.append(i)
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

def compute_ranks(graph):
    d = 0.8 # damping factor
    numloops = 10
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
    
def ordered_search(index, ranks, keyword):
    urls = []
    if keyword not in index:
        return None
    for i in index[keyword]:
        urls.append([i,ranks[i]])
    quicksort_urls = quicksort(urls)
    rankings = []
    for l in quicksort_urls:
        rankings.append(l[0])
    return rankings

# Test functions
def test_crawler():
    filename = 'links'
    # Sample seed links
    hstat = "http://www.hstat.org"
    udacity = "http://www.udacity.com/cs101x/index.html"
    xkcd = "http://www.xkcd.com"
    python = "http://docs.python.org/index.html"
    depth = 1
    print "Starting web crawler...\n"
    
    # Start web crawler
    start_time = time.clock()
    index = web_index_crawler(python, depth, True)
    
    # Index Searching
    lookup_test = 'python'
    print "\nSearching: %s" % lookup_test
    results = lookup(index, lookup_test)
    linksfound = len(results)
    print "Results Found: %d" % linksfound
    print results

    # Saving results to text file
    #new_file(filename)
    #txtfile = open(filename+'.txt', 'a')
    #txtfile.write("\nRunning time: %.5f sec" % (time.clock()-start_time))
    #txtfile.close()
    print "\nTask complete."
    
    # Computation time for session
    print "Running time: %.5f sec" % (time.clock()-start_time)
    

def main():
    test_crawler()
    
main()