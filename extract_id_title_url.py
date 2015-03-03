#!/usr/bin/env python2.7
# encoding: utf-8
'''
extract_id_title.py

Created by Hallvord R. M. Steen on 2014-10-25.
Modified by Karl
Mozilla Public License, version 2.0
see LICENSE

Dumps data from webcompat.com bug tracker
by default creates one CSV file (webcompatdata.csv)
and one JSON file (webcompatdata-bzlike.json)
the JSON file uses many of the field names Bugzilla uses in its export,
so the output from this script can be used where Bugzilla data is expected
'''

import json
import re
import socket
import sys
import urllib2

# Seconds. Loading searches can be slow
socket.setdefaulttimeout(240)


def get_remote_file(url, req_json=False):
    print('Getting '+url)
    req = urllib2.Request(url)
    req.add_header('User-agent', 'AreWeCompatibleYetBot')
    if req_json:
        req.add_header('Accept', 'application/vnd.github.v3+json')
    bzresponse = urllib2.urlopen(req, timeout=240)
    return {"headers": bzresponse.info(),
            "data": json.loads(bzresponse.read().decode('utf8'))}


def extract_data(json_data, results_csv, results_bzlike):
    translation_map = {
        "title": "summary",
        "state": {"name": "status",
                  "values": {"closed": "RESOLVED", "open": "OPEN"}},
        "updated_at": "last_change_time",
        "created_at": "creation_time",
        "number": "id",
        "closed_at": "cf_last_resolved",
        }
    resolution_labels = ["duplicate", "invalid", "wontfix", "fixed",
                         "worksforme"]
    whiteboard_labels = ["needsinfo", "contactready", "sitewait",
                         "needscontact", "needsdiagnosis"]
    # areWEcompatibleyet is only about mozilla bugs
    browser_os_labels = ["firefox", "mozilla", "android", "mobile"]
    # URL in webcompat.com bugs follow this pattern:
    # **URL**: https://example.com/foobar
    url_pattern = re.compile('\*\*URL\*\*\: (.*)\n')
    for issue in json_data["data"]:
        url_match = re.search(url_pattern, issue["body"])
        if url_match:
            url = url_match.group(1).strip()
            if not url.startswith(('http://', 'https://')):
                url = "http://%s" % url
        else:
            url = ""
        bug_id = issue["number"]
        link = 'https://webcompat.com/issues/%s' % bug_id
        if issue["title"] != "":
            results_csv.append("%i\t%s\t%s\t%s"
                               % (bug_id, issue["title"].strip(), url, link))
        bzlike = {"id": bug_id,
                  "summary": issue["title"].strip(),
                  "url": url,
                  "whiteboard": "",
                  "op_sys": ""}
        for prop in translation_map:
            if isinstance(translation_map[prop], basestring):
                bzlike[translation_map[prop]] = issue[prop]
            elif issue[prop] in translation_map[prop]['values']:
                bzlike[translation_map[prop]['name']] = translation_map[prop]['values'][issue[prop]]
            else:
                print("Warning: not sure what to do with %s, value: %s"
                      % (prop, issue[prop]))
        # GitHub labels require some special processing..
        for labelobj in issue['labels']:
            if labelobj['name'] in resolution_labels:
                bzlike['resolution'] = labelobj['name'].upper()
            elif (labelobj['name'] in whiteboard_labels
                  or labelobj['name'] in browser_os_labels):
                bzlike['whiteboard'] += "[%s] " % labelobj['name']
        if ('[firefox]' in bzlike['whiteboard'] and '[mobile]' in bzlike['whiteboard']):
            bzlike['op_sys'] = 'Gonk (Firefox OS)'
        elif ('[firefox]' in bzlike['whiteboard']
              and '[android]' in bzlike['whiteboard']):
            bzlike['op_sys'] = 'Android'
        results_bzlike.append(bzlike)


def extract_next_link(link_hdr):
    '''Given a HTTP Link header, extract the "next" link.

    Link header has the pattern:
    '<https://example.com/foobar?page=2>; rel="next",
     <https://example.com/foobar?page=100>; rel="last"'
    We need:
    https://example.com/foobar?page=2
    When no more "next", we return an empty string.
    '''
    next_link = ''
    links = link_hdr.split(',')
    for link in links:
        link_only, rel = link.split(';')
        if 'next' in rel:
            next_link = link_only.strip(' <>')
            break
    return next_link


def get_webcompat_data():
    url_base = "https://api.github.com/repos/webcompat/web-bugs"
    next_link = url_base + '/issues?per_page=100&page=1'

    results = []
    bzresults = []

    while next_link:
        response_data = get_remote_file(next_link, True)
        extract_data(response_data, results, bzresults)
        next_link = extract_next_link(response_data["headers"]["link"])
    return [results, {"bugs": bzresults}]


def main():
    tmp = get_webcompat_data()
    results = tmp[0]
    bzresults = tmp[1]
    with open('webcompatdata.csv', 'w') as f:
        f.write("\n".join(results).encode('utf8'))
        f.write('\n')
    print("Wrote %d items to webcompatdata.csv " % len(results))
    with open('webcompatdata-bzlike.json', 'w') as f:
        f.write(json.dumps(bzresults, indent=4).encode('utf8'))
    print("Wrote %d items to webcompatdata-bzlike.json" % len(bzresults))

if __name__ == "__main__":
    sys.exit(main())