import urllib2, re, time
    
def find_links(link):
    # Input takes in a link address
    # Outputs list containing all links found
    # Function uses regular expression search
    source_code = urllib2.urlopen(link).read()
    linkpattern = re.compile('(?<=<a href=")http[^"]+')
    links_found = re.findall(linkpattern, source_code)
    return links_found

def web_crawler(seed, max_depth):
    # Will only searches for full link addresses
    # Input parameters takes seed, max_depth, filename
    # Outputs list of all links crawled to a certain depth
    # seed: starting link for crawling
    # max_depth: maximum depth of links to find while crawling
    # filename: file name to save results
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
            if url not in visited:
                visited.append(url)
                for u in find_links(url):
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
    return visited

def new_file(filename):
    txtfile = open(filename+'.txt', 'w')
    txtfile.close()

def add_to_index(index, keyword, url):
    key_index  = 0
    key_exists = False
    for keys in index:
        if keys[0] == keyword:
            key_exists = True
            break
        key_index += 1
    if key_exists:
        index[key_index][1].append(url)
    else:
        index.append([keyword, [url]])

def main():
    filename = 'links'
    # Sample seed links
    hstat = "http://www.hstat.org"
    udacity = "http://www.udacity.com/cs101x/index.html"
    xkcd = "http://www.xkcd.com"
    wiki = "http://en.wikipedia.org/wiki/Website"
    depth = 1
    print "Starting web crawler...\n"
    
    # Start web crawler
    start_time = time.clock()
    all_links = web_crawler(wiki, depth)
    
    # Saving results to text file
    new_file(filename)
    txtfile = open(filename+'.txt', 'a')
    for i in all_links:
        txtfile.write(i+'\n')
    txtfile.write("\nRunning time: %.5f sec" % (time.clock()-start_time))
    txtfile.close()
    print "\nTask complete."
    
    # Computation time for session
    print "Running time: %.5f sec" % (time.clock()-start_time)

main()