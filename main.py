#!/usr/bin/env python

import webapp2
import sys
import logging
sys.path.insert(0, 'libs')

from pymessenger.bot import Bot

import base64
import datetime
from itertools import islice
from textwrap import dedent
import time
import json

from google.appengine.api.logservice import logservice

#template jinja2
import jinja2
import os
from google.appengine.api import users

#file storage
from google.appengine.api import app_identity
import cloudstorage as gcs


#template_env=jinja2.Environment(loader=jinja2.FileSystemLoader(os.getcwd()))

bot = Bot('EAAEKyIZBFuIsBAEJmP44XLZCAmm9M7eYZAC6ZAIR8rc9RvKt3Vx9BfaqCt2o9zm5B25ngbuZAFqWBakZA7x9X9kMEhGcxarvleAZBRNlQoxo2jKIUqZAdQklI3588Eun4SMqQksFTvQjnPgllPYxR2ZCKsLT7sTK35XcB6A96237xIQZDZD')

class MainHandler(webapp2.RequestHandler):
    def get(self):
        bucket_name = os.environ.get('BUCKET_NAME', app_identity.get_default_gcs_bucket_name())
        template_content=self.read_file("/"+bucket_name+"/templates/index.html")
        template=jinja2.Template(template_content)
        user=users.get_current_user()
        login_url=users.create_login_url(self.request.path)
        logout_url=users.create_logout_url(self.request.path)

        context={
            'title':'timebotpy',
            'user':user,
            'login_url':login_url,
            'login_out':logout_url
        }
        self.response.out.write(template.render(context))

    def read_file(self, filename):
        gcs_file = gcs.open(filename)
        content=gcs_file.read()
        gcs_file.close()
        return content

class FileStorage(webapp2.RequestHandler):
    def get(self):
        bucket_name = os.environ.get('BUCKET_NAME',app_identity.get_default_gcs_bucket_name())

        self.response.headers['Content-Type'] = 'text/plain'
        self.response.write('Demo GCS Application running from Version: '
                            + os.environ['CURRENT_VERSION_ID'] + '\n')
        self.response.write('Using bucket name: ' + bucket_name + '\n\n')

        #self.create_file("/"+bucket_name+"/test.txt")

    def create_file(self, filename):
        """Create a file.

        The retry_params specified in the open call will override the default
        retry params for this particular file handle.

        Args:
          filename: filename.
        """
        self.response.write('Creating file %s\n' % filename)

        write_retry_params = gcs.RetryParams(backoff_factor=1.1)
        gcs_file = gcs.open(filename,
                            'w',
                            content_type='text/plain',
                            options={'x-goog-meta-foo': 'foo',
                                     'x-goog-meta-bar': 'bar'},
                            retry_params=write_retry_params)
        gcs_file.write('abcde\n')
        gcs_file.write('f' * 1024 * 4 + '\n')
        gcs_file.close()


class FBWebhook(webapp2.RequestHandler):
    def get(self):
        if (self.request.get("hub.verify_token") == 'EAAEKyIZBFuIsBAEJ'):
            return self.response.write(self.request.get("hub.challenge"))
        return self.response.write('Error, wrong validation token')

    def post(self):

        logging.debug(str(self.request.body))
        data=json.loads(str(self.request.body))

        sender_id=data["entry"][0]["messaging"][0]["sender"]["id"]
        recipient_id=data["entry"][0]["messaging"][0]["recipient"]["id"]

        has_msg="message" in data["entry"][0]["messaging"][0]
        if has_msg:
            has_text="text" in data["entry"][0]["messaging"][0]["message"]
        else:
            has_text=False

        #app fb id: 1779221859017160

        if has_msg:
            if has_text:
                #logging.debug(res_ai)
                text=data["entry"][0]["messaging"][0]["message"]["text"]
                bot.send_text_message(sender_id,text)

        self.response.write("success")

def get_logs(offset=None):
    # Logs are read backwards from the given end time. This specifies to read
    # all logs up until now.
    end_time = time.time()

    logs = logservice.fetch(
        end_time=end_time,
        offset=offset,
        minimum_log_level=logservice.LOG_LEVEL_INFO,
        include_app_logs=True)

    return logs

def format_log_entry(entry):
    # Format any application logs that happened during this request.
    logs = []
    for log in entry.app_logs:
        date = datetime.datetime.fromtimestamp(
            log.time).strftime('%D %T UTC')
        logs.append('Date: {}, Message: {}'.format(
            date, log.message))

    # Format the request log and include the application logs.
    date = datetime.datetime.fromtimestamp(
        entry.end_time).strftime('%D %T UTC')

    output = dedent("""
        Date: {}
        IP: {}
        Method: {}
        Resource: {}
        Logs:
    """.format(date, entry.ip, entry.method, entry.resource))

    output += '\n'.join(logs)

    return output

class LogsHandler(webapp2.RequestHandler):
    def get(self):
        offset = self.request.get('offset', None)

        if offset:
            offset = base64.urlsafe_b64decode(str(offset))

        # Get the logs given the specified offset.
        logs = get_logs(offset=offset)

        # Output the first 10 logs.
        log = None
        for log in islice(logs, 10):
            self.response.write(
                '<pre>{}</pre>'.format(format_log_entry(log)))

            offset = log.offset

        if not log:
            self.response.write('No log entries found.')

        # Add a link to view more log entries.
        elif offset:
            self.response.write(
                '<a href="/?offset={}"">More</a'.format(
                    base64.urlsafe_b64encode(offset)))

app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/fbwebhook',FBWebhook),
    ('/logs',LogsHandler),
    ('/filestorage',FileStorage)
], debug=True)
