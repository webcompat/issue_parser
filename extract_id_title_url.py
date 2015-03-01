# dumps data from webcompat.com bug tracker
# by default creates one CSV file (webcompatdata.csv)
# and one JSON file (webcompatdata-bzlike.json) - this JSON file uses many of the field names
# Bugzilla uses in its export, so the output from this script can be used where Bugzilla data
# is expected

import json, urllib2, re, sys, socket, pdb
socket.setdefaulttimeout(240) # Seconds. Loading searches can be slow

def get_remote_file(url, req_json=False):
    print('Getting '+url)
    req = urllib2.Request(url)
    req.add_header('User-agent', 'hallvors')
    if req_json:
        req.add_header('Accept', 'application/vnd.github.v3+json')
#   req.add_header('User-agent', 'Mozilla/5.0 (Windows NT 5.1; rv:27.0) Gecko/20100101 Firefox/27.0')
    bzresponse = urllib2.urlopen(req, timeout=240)
    return {"headers":bzresponse.info(), "data": json.loads(bzresponse.read().decode('utf8'))}

def extract_data(json_data, results_csv, results_bzlike):
    translation_map = {
    "title":"summary",
    "state" : {"name":"status", "values": {"closed":"RESOLVED", "open": "OPEN"}},
    "updated_at": "last_change_time",
    "created_at": "creation_time",
    "number": "id",
    "closed_at": "cf_last_resolved",
    }
    resolution_labels = ["duplicate", "invalid", "wontfix", "fixed", "worksforme"]
    whiteboard_labels = ["needsinfo", "contactready", "sitewait", "needscontact", "needsdiagnosis"]
    browser_os_labels = ["firefox", "mozilla", "android", "mobile"] # areWEcompatibleyet doesn't care about non-moz, sorry - that's the purpose of webcompat.com
    for issue in json_data["data"]:
        url_match = re.search(re.compile('\*\*URL\*\*\: (.*)\n'), issue["body"])
        if url_match:
            url = url_match.group(1).strip()
            if 'http://' not in url and 'https://' not in url:
                url = "http://%s" % url
        else:
            url = ""
        bug_id = issue["number"]
        link = 'https://webcompat.com/issues/%s' % bug_id
        if issue["title"] != "":
            results_csv.append("%i\t%s\t%s\t%s" % (bug_id, issue["title"].strip(), url,link))
        bzlike = {"id":bug_id, "summary":issue["title"].strip(), "url":url, "whiteboard":"", "op_sys":""}
        for prop in translation_map:
            if isinstance(translation_map[prop], basestring):
                bzlike[translation_map[prop]] = issue[prop]
            elif issue[prop] in translation_map[prop]['values']:
                bzlike[translation_map[prop]['name']] = translation_map[prop]['values'][issue[prop]]
            else:
                print("Warning: not sure what to do with %s, value: %s" % (prop, issue[prop]))
        # GitHub labels require some special processing..
        for labelobj in issue['labels']:
            if labelobj['name'] in resolution_labels:
                bzlike['resolution'] = labelobj['name'].upper()
            elif labelobj['name'] in whiteboard_labels or labelobj['name'] in browser_os_labels:
                bzlike['whiteboard'] += "[%s] " % labelobj['name']
        if '[firefox]' in bzlike['whiteboard'] and '[mobile]' in bzlike['whiteboard']:
            bzlike['op_sys'] = 'Gonk (Firefox OS)'
        elif '[firefox]' in bzlike['whiteboard'] and '[android]' in bzlike['whiteboard']:
            bzlike['op_sys'] = 'Android'
        results_bzlike.append(bzlike)

def extract_links(link_hdr):
    all_links = {"next":"", "last":"", "first":"", "prev":""}
    links = re.split(',', link_hdr)
    for link in links:
        details = re.split(';', link)
        the_type = re.search(r'rel="(.*)"', details[1]).group(1)
        all_links[the_type] = details[0].strip(' <>')
    return all_links

def get_webcompat_data():
    url_base = "https://api.github.com/"
    links = {"next": url_base + 'repos/webcompat/web-bugs/issues?per_page=100&page=1'}

    results = []
    bzresults = []

    while links["next"]:
        response_data = get_remote_file(links["next"], True)
        extract_data(response_data, results, bzresults)
        links = extract_links(response_data["headers"]["link"])
    # Link: <https://api.github.com/repositories/17914657/issues?per_page=10&page=2>; rel="next", <https://api.github.com/repositories/17914657/issues?per_page=10&page=23>; rel="last"
    return [results, {"bugs":bzresults}]

def main():
    tmp = get_webcompat_data()
    results = tmp[0]
    bzresults = tmp[1]
    # open('webcompatdata.csv', 'w').write("\n".join(results))
    f = open('webcompatdata.csv', 'w')
    f.write("\n".join(results).encode('utf8'))
    f.write('\n')
    f.close()
    print("Wrote %d items to webcompatdata.csv " % len(results))
    f = open('webcompatdata-bzlike.json', 'w')
    f.write(json.dumps(bzresults, indent=4).encode('utf8'))
    f.close()
    print("Wrote %d items to webcompatdata-bzlike.json" % len(bzresults))

if __name__ == "__main__":
    sys.exit(main())