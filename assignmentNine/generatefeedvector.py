# -*- coding: utf-8 -*-
import feedparser
import collections
import re
import feedfilter as f
entryFile = open('entryfile.txt', 'w')
outputFile = open('output.txt', 'w')
def getwords(html):
  text = re.compile(r'<[^>]+>').sub('', html)
  words = re.compile(r'[^A-z^a-z]+').split(text)
  return [word.lower() for word in words if word]

  
  

#def getwordcounts(url):
 # d = feedparser.parse(url)
 # print d
 # wc = collections.defaultdict(int)

  #for e in d.entries:
   # if 'summary' in e: summary = e.summary
   # else: summary = e.description

    #words = getwords('%s %s' % (e.title, summary))
    #for word in words:
   #   wc[word] += 1

  #if 'title' not in d.feed:
  #  print 'Invalid url', url
  #  return 'bogus data', wc
 # return d.feed.title, wc

# Returns title and dictionary of 
# word counts for an RSS feed

def getwordcounts(url):
  # Parse the feed
  d=feedparser.parse(url)
  wc={}

  # Loop over all the entries
  # description==RSS; summary==Atom
  for e in d.entries:
    if 'summary' in e: summary=e.summary
    else: summary=e.description
    outputFile.write(e.title.replace(u"\u2019", "'").replace(u"\u2026", "...").replace(u"\u201c", "'").replace(u"\u201d", "'").replace(u"\u2122", "tm").replace(u"\u2013", "-"))
    outputFile.write("\n")
    entryFile.write(str(e))
    entryFile.write("\n")
    # Extract a list of words
    words=getwords(e.title+' '+summary)
    for word in words:
      wc.setdefault(word,0)
      wc[word]+=1

  if 'title' not in d.feed:
    print 'Invalid url', url
    return 'bogus data', wc
  return d.feed.title, wc



def main():

  # XXX: break this up into smaller funtions, write tests for them

  apcount = collections.defaultdict(int)
  wordcounts = {}
  feedlist = open('feedlist.txt').readlines()
  for url in feedlist:
    title, wc = getwordcounts(url)
    wordcounts[title] = wc
    for word, count in wc.iteritems():
      if count > 1:
        apcount[word] += 1

  wordlist = []
  for w, bc in apcount.iteritems():
    frac = float(bc)/len(feedlist)
    if 0.1 < frac < 0.5: wordlist.append(w)

  out = file('blogdata.txt', 'w')
  out.write('Blog')
  for w in wordlist: out.write('\t' + w)
  out.write('\n')
  for blogname, counts in wordcounts.iteritems():
    blog = blogname.encode('UTF-8')
    out.write(blog)
    for w in wordlist:
      if w in counts: out.write('\t%d' % counts[w])
      else: out.write('\t0')
    out.write('\n')

if __name__ == '__main__':
  main()
  outputFile.close()
  entryFile.close()