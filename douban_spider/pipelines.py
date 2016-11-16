# -*- coding: utf-8 -*-

import MySQLdb
import uuid
from spiders import user_settings

class DoubanSpiderPipeline(object):

	def __init__(self):
		self.connection = MySQLdb.connect(user_settings.MYSQL['host'],
			user_settings.MYSQL['username'],
			user_settings.MYSQL['password'],
			user_settings.MYSQL['database'],
			use_unicode=True,charset='UTF8')
		self.cursor = self.connection.cursor(MySQLdb.cursors.DictCursor)

	def process_item(self, item, spider):
		uid = ''.join(str(uuid.uuid4()).split('-'))
		sql = """INSERT INTO movie("""\
		"""uid,"""\
		"""name,"""\
		"""score,"""\
		"""type,"""\
		"""summary,"""\
		"""release_time,"""\
		"""actors,"""\
		"""src_url) """\
		"""VALUES(%s,%s,%s,%s,%s,%s,%s,%s)"""
		value = (uid,item['name'],
			item['score'],
			item['types'],
			item['summary'],
			item['release_time'],
			item['actors'],
			item['src_url'])
		try:
			self.cursor.execute(sql,value)
			self.connection.commit()
		except MySQLdb.Error, e:
			print "Error %d: %s,%s" % (e.args[0], e.args[1], item['src_url'])
		
		return item
