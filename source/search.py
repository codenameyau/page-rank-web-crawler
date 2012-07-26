import urllib2, re, time

# Returns source code from url (changes all characters to lowercase)
def get_page_source(link):
    try:
        return urllib2.urlopen(link).read().lower()
    except Exception:
        return ""

# Outputs list containing all links found from source
def find_links(link, source):
    linkpattern = re.compile('(?<=<a href=")http[^"]+')
    links_found = re.findall(linkpattern, source)
    return links_found

# Returns an index containing keywords and its associated urls
def web_index_crawler(seed, max_depth):
    search_index = []
    visited   = []
    unvisited = [seed]
    current_depth  = 0
    current_branch = 0
    current_seeds = len(unvisited)-1
    while unvisited:
        try:
            url = unvisited.pop(0)
            if current_depth > max_depth:
                break
            visited.append(url)
            source_code = get_page_source(url)
            links_found = find_links(url, source_code)
            index_page(search_index, url, source_code)
            for u in links_found:
                if u not in visited and u not in unvisited:
                    unvisited.append(u)
            print "Crawled: %s" % url
            if current_branch < current_seeds:
                current_branch += 1
            else:
                current_branch = 0
                current_seeds = len(unvisited)-1
                current_depth += 1
        except Exception:
            pass
    return search_index

# Creates a new blank text file using filename
def new_file(filename):
    txtfile = open(filename+'.txt', 'w')
    txtfile.close()

# ---Data Structure commands
# Adds a keyword and its url to index
def add_to_index(index, keyword, url):
    for keys in index:
        if keys[0] == keyword:
            keys[1].append(url)
            return
    index.append([keyword, [url]])

# Adds all keywords in page source to index
def index_page(index, url, content):
    keywords = content.split()
    for word in keywords:
        add_to_index(index, word, url)

# Returns associated urls with keyword
def lookup(index, keyword):
    for entries in index:
        if entries[0] == keyword:
            return entries[1]
    return []

# Separates phrases by characters in splitlist
def split_string(source, splitlist):
    words = []
    build = ""
    for c in source:
        if c not in splitlist:
            build += c
        else:
            if len(build) > 0:
                words.append(build)
                build = ""
    if len(build) > 0:
        words.append(build)
    return words

def main():
    filename = 'links'
    # Sample seed links
    hstat = "http://www.hstat.org"
    udacity = "http://www.udacity.com/cs101x/index.html"
    xkcd = "http://www.xkcd.com"
    depth = 1
    print "Starting web crawler...\n"
    
    # Start web crawler
    start_time = time.clock()
    index = web_index_crawler(udacity, depth)
    
    # Index Searching
    lookup_test = 'the'
    print "\nPerforming search: %s" % lookup_test 
    print lookup(index, lookup_test)
    
    # Saving results to text file
    #new_file(filename)
    #txtfile = open(filename+'.txt', 'a')
    #txtfile.write("\nRunning time: %.5f sec" % (time.clock()-start_time))
    #txtfile.close()
    print "\nTask complete."
    
    # Computation time for session
    print "Running time: %.5f sec" % (time.clock()-start_time)

main()