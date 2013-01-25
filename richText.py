#!/usr/bin/python
# -*- coding: utf-8 -*-

# richText class manages a block of text and a list of items with ranges of the text to which they apply
# the items are dicts so you can add your own properties to them.  'name', 'start' and 'end' are reserved.
# items may cover zero or more characters within the text (if you delete all the text in an item you'll leave an empty item - it's not removed.  subclasses may do such removals)

# TODO could use a networkx network instead of a list of dicts for the items for added functionality

class richText:

  def __init__(self):
		self._styles = []
		self._text = ""
	
	def _tidy(self):
		toRemove = []
		for n, style in enumerate(self._styles):
			if style['start'] >= style['end']: toRemove.append(n)
		for n in reversed(toRemove): del self._styles[n]

	def add(self, tag, start, end):
		assert start < end
		assert end <= len(self._text)
		self._styles.append({'name': tag, 'start': start, 'end': end})

	def removeAll(self, tag):
		toRemove = list(m for m, style in enumerate(self._styles) if style['name'] == tag)
		for m in reversed(toRemove): del self._styles[m]
	
	def getRanges(self, tag):
		ranges = []
		for style in self._styles:
			if style['name'] == tag: ranges.append([style['start'], style['end']])
		return ranges
	
	def getText(self):
		return self._text
	
	def insert(self, text, offset):
		assert offset <= len(self._text)
		self._text = self._text[:offset] + text + self._text[offset:]
		for n, style in enumerate(self._styles):
			if style['start'] >= offset: style['start'] += len(text)
			if style['end'] > offset: style['end'] += len(text)

	def delete(self, start, end):
		assert end <= len(self._text)
		assert start <= end
		self._text = self._text[:start] + self._text[end:]
		removed = end - start
		toRemove = []
		for n, style in enumerate(self._styles):
			if style['start'] > start: style['start'] = max(start, style['start'] - removed)
			if style['end'] > start: style['end'] = max(start, style['end'] - removed)
			if style['start'] == style['end']: toRemove.append(n)
		for n in reversed(toRemove): del self._styles[n]
