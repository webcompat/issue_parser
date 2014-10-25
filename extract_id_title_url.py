import json, urllib2, re, sys, socket
socket.setdefaulttimeout(240) # Seconds. Loading searches can be slow

results = []

def get_remote_file(url, req_json=False):
    print('Getting '+url)
    req = urllib2.Request(url)
    req.add_header('User-agent', 'hallvors')
    if req_json:
        req.add_header('Accept', 'application/vnd.github.v3+json')
#   req.add_header('User-agent', 'Mozilla/5.0 (Windows NT 5.1; rv:27.0) Gecko/20100101 Firefox/27.0')
    bzresponse = urllib2.urlopen(req, timeout=240)
    return {"headers":bzresponse.info(), "data": json.loads(bzresponse.read())}

def extract_data(json_data, results):
    for issue in json_data["data"]:
        url_match = re.search(re.compile('\*\*URL\*\*\: (.*)\n'), issue["body"])
        if url_match:
            url = url_match.group(1).strip()
        else:
            url = ""
        bug_id = issue["number"]
        if issue["title"] != "":
            results.append("%i\t%s\t%s" % (bug_id, issue["title"].strip(), url))

def extract_links(link_hdr):
    all_links = {"next":"", "last":"", "first":"", "prev":""}
    links = re.split(',', link_hdr)
    for link in links:
        details = re.split(';', link)
        the_type = re.search(r'rel="(.*)"', details[1]).group(1)
        all_links[the_type] = details[0].strip(' <>')
    return all_links

def main():
    url_base = "https://api.github.com/"

    links = {"next": url_base + 'repos/webcompat/web-bugs/issues?per_page=100&page=1'}

    while links["next"]:
        response_data = get_remote_file(links["next"], True)
        extract_data(response_data, results)
        links = extract_links(response_data["headers"]["link"])

    # Link: <https://api.github.com/repositories/17914657/issues?per_page=10&page=2>; rel="next", <https://api.github.com/repositories/17914657/issues?per_page=10&page=23>; rel="last"
    # open('webcompatdata.csv', 'w').write("\n".join(results))
    print("\n".join(results))


if __name__ == "__main__":
    sys.exit(main())