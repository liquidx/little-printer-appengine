# Copyright 2012 Alastair Tse
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#  http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import json
import jinja2
import logging
import os
import webapp2

def get_jinja2_template(path):
  template_dir = os.path.dirname(__file__)
  jinja_environment = jinja2.Environment(loader=jinja2.FileSystemLoader([template_dir]))
  return jinja_environment.get_template(path)

def get_publication_content(number):
  publications_dir = os.path.join(os.path.dirname(__file__), 'publications')
  publication_filename = '%03d.txt' % number
  return open(os.path.join(publications_dir, publication_filename)).read().decode('utf8')


# http://remote.bergcloud.com/developers/reference/metajson
class MetaJsonHandler(webapp2.RequestHandler):
  def get(self):
    value = {
      'owner_email': 'alastair@liquidx.net',
      'publication_api_version': '1.0',
      'name': 'Printing Me Softly',
      'description': 'Soft things fit for print.',
      'delivered_on': 'every day',
      'send_timezone_info': True, 
      'send_delivery_count': True,
    }

    self.response.add_header('Content-Type', 'application/json')
    self.response.out.write(json.dumps(value))

# http://remote.bergcloud.com/developers/reference/edition
class EditionHandler(webapp2.RequestHandler):
  def get(self):
    delivery_time = self.request.get('local_delivery_time')
    delivery_count = int(self.request.get('delivery_count', 0))

    # TODO: set an etag on the response.
    # self.response.add_header('ETag', '')
    values = {
      'title': u'Daily emoji',
      'emoji': get_publication_content(1),
      'caption': u'Table Flip',
      'edition': u'1',
    }
    template = get_jinja2_template('publication.html')
    self.response.out.write(template.render(values))


class SampleHandler(webapp2.RequestHandler):
  def get(self):
    values = {
      'title': u'Daily emoji',
      'emoji': get_publication_content(1),
      'caption': u'Table Flip',
      'edition': u'1',
    }
    template = get_jinja2_template('publication.html')
    self.response.out.write(template.render(values))


class ValidateConfigHandler(webapp2.RequestHandler):
  def post(self):
    pass # TODO

# http://remote.bergcloud.com/developers/reference/configure
class ConfigureHandler(webapp2.RequestHandler):
  def get(self):
    return_url = self.request.get('return_url')
    # TODO: then need to generate an auth token and pass
    #       this back to "return_url" as config[access_token]=xxx

urls = [
  ('^/meta.json$', MetaJsonHandler),
  ('^/edition/?$', EditionHandler),
  ('^/sample/?$', SampleHandler),
  ('^/validate_config/?$', ValidateConfigHandler),
  ('^/configure/?$', ConfigureHandler),
]

app = webapp2.WSGIApplication(urls, debug=True)
