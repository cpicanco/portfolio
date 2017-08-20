#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
  author: Rafael Picanço.
  Import publications (zotero api) as csljson.
  Hack to save them as html and translated by available locales (citeproc).
  Do not recommended for production. Need better handling of unicode strings.

  citeproc:
    - UserWarning: The following arguments for Reference are unsupported: journalAbbreviation
    - apa.csl is returns duplicates dots e.g.: '.. '
"""
from __future__ import (absolute_import, division, print_function,unicode_literals)

import os
import json
from libZotero import zotero # https://github.com/fcheslack/libZotero
import xml.etree.ElementTree as ET #read only operations on private lib, no security concerns

#from citeproc.py2compat import *
from citeproc import CitationStylesStyle, CitationStylesBibliography
from citeproc import Citation, CitationItem
from citeproc import formatter
from citeproc.source.json import CiteProcJSON

def warn(citation_item):
    return "{}' not found.".format(citation_item.key)

def apa_html_utf8(json_data, alocale='en-US'):
  # CiteProcJSON receives a [{}] not a {}
  bib_source = CiteProcJSON([json_data])
  apa = CitationStylesStyle('apa', locale=alocale, validate=False)
  bibliography = CitationStylesBibliography(apa, bib_source, formatter.html)
  citation = Citation([CitationItem(json_data['id'])])
  bibliography.register(citation)

  # handle python weird string type
  return str(''.join(bibliography.bibliography()[0]).encode('utf-8'))

# weird chars hack
latin_chars = [('&iexcl;','¡'),('&cent;','¢'),('&pound;','£'),('&curren;','¤'),
  ('&yen;','¥'),('&brvbar;','¦'),('&sect;','§'),('&uml;','¨'),('&copy;','©'),
  ('&ordf;','ª'),('&laquo;','«'),('&not;','¬'),('&reg;','®'),('&macr;','¯'),
  ('&deg;','°'),('&plusmn;','±'),('&sup2;','²'),('&sup3;','³'),('&acute;','´'),
  ('&micro;','µ'),('&para;','¶'),('&middot;','·'),('&cedil;','¸'),('&sup1;','¹'),
  ('&ordm;','º'),('&raquo;','»'),('&frac14;','¼'),('&frac12;','½'),('&frac34;','¾'),
  ('&iquest;','¿'),('&Agrave;','À'),('&Aacute;','Á'),('&Acirc;','Â'),('&Atilde;','Ã'),
  ('&Auml;','Ä'),('&Aring;','Å'),('&AElig;','Æ'),('&Ccedil;','Ç'),('&Egrave;','È'),
  ('&Eacute;','É'),('&Ecirc;','Ê'),('&Euml;','Ë'),('&Igrave;','Ì'),('&Iacute;','Í'),
  ('&Icirc;','Î'),('&Iuml;','Ï'),('&ETH;','Ð'),('&Ntilde;','Ñ'),('&Ograve;','Ò'),
  ('&Oacute;','Ó'),('&Ocirc;','Ô'),('&Otilde;','Õ'),('&Ouml;','Ö'),('&times;','×'),
  ('&Oslash;','Ø'),('&Ugrave;','Ù'),('&Uacute;','Ú'),('&Ucirc;','Û'),('&Uuml;','Ü'),
  ('&Yacute;','Ý'),('&THORN;','Þ'),('&szlig;','ß'),('&agrave;','à'),('&aacute;','á'),
  ('&acirc;','â'),('&atilde;','ã'),('&auml;','ä'),('&aring;','å'),('&aelig;','æ'),
  ('&ccedil;','ç'),('&egrave;','è'),('&eacute;','é'),('&ecirc;','ê'),('&euml;','ë'),
  ('&igrave;','ì'),('&iacute;','í'),('&icirc;','î'),('&iuml;','ï'),('&eth;','ð'),
  ('&ntilde;','ñ'),('&ograve;','ò'),('&oacute;','ó'),('&ocirc;','ô'),('&otilde;','õ'),
  ('&ouml;','ö'),('&oslash;','ø'),('&ugrave;','ù'),('&uacute;','ú'),('&ucirc;','û'),
  ('&uuml;','ü'),('&yacute;','ý'),('&thorn;','þ'),('&yuml;','ÿ'),('&ndash;','–'),
  ('&mdash;', '—'),('&hellip;', '…'),('&#8220;','“'),('&#8221;','”')]

publicati_path = os.path.join(os.sep, os.path.dirname(os.getcwd()), '_data', 'publications')
csljson_path = os.path.join(os.sep, os.getcwd(), 'csljson')

# credential
with open('.credential.json') as credential:
  c = json.loads(credential.read())
  # libZotero/zotero config
  library = zotero.Library(c['libraryType'], c['libraryID'], c['librarySlug'], c['apiKey'])

  # fetch some items
  items = library.fetchItems({'collectionKey':c['collectionID'],'content':'json','sort':'date'})

for item in items:
  yamlname = os.path.join(os.sep, publicati_path, item.get('date').replace('-', ''))
  jsonname = os.path.join(os.sep, csljson_path, item.get('date').replace('-', ''))

  # csljson must be fetched individually it is parsed as xml
  itemFetched = library.fetchItem(item.itemKey,{'content':'csljson' })

  # load json dictionary from xml
  xmle = ET.fromstring(itemFetched.content.encode('utf-8'))
  csljson = xmle.find('{http://www.w3.org/2005/Atom}content').text
  for cs in latin_chars:
    csljson = csljson.replace(cs[1],cs[0])
  json_dict = json.loads(csljson)

  # add 'date-parts' from 'raw'
  y, _, _ = json_dict['issued']['raw'].split('-')
  #json_dict['issued']['date-parts'] = [[y, m, d]]
  json_dict['issued']['date-parts'] = [[y]]

  # debug
  # print(json_dict['id'])
  # print('#######')
  
  # save csljson
  with open(jsonname+'.json', 'w+') as f:
    json.dump(json_dict, f, indent=4, sort_keys=True, ensure_ascii=False)

  # translate and save a reference as html into our custom yml
  with open(yamlname+'.yml', 'w+') as f:
    f.write('pt-BR:\n  '.encode('utf-8'))
    f.write('html: >\n    '.encode('utf-8'))
    f.write(apa_html_utf8(json_dict, alocale='pt-BR'))
    f.write('\n\nen:\n  '.encode('utf-8'))
    f.write('html: >\n    '.encode('utf-8'))
    f.write(apa_html_utf8(json_dict))
    if 'DOI' in json_dict:
      f.write('\n\ndoi: >\n  ')
      f.write(json_dict['DOI'])

    if 'URL' in json_dict:
      f.write('\n\nurl: >\n  ')
      f.write(json_dict['URL'])

    if 'type' in json_dict:
      f.write('\n\ntype: ')
      f.write(json_dict['type'])