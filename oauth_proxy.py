import urllib
import re

from twitter import SIGNIN_URL, TwitterAuthenticationError
from google.appengine.api import urlfetch

def login_oauth(web_url, username, password):
  result = urlfetch.fetch(web_url)
  authenticity_token = ''
  oauth_token = ''
  groups = re.search(r'<input .*name="authenticity_token" .*value="(.*)"', result.content, re.IGNORECASE)
  if groups:
    authenticity_token = groups.group(1)
  groups = re.search(r'<input .*name="oauth_token" .*value="(.*)"', result.content, re.IGNORECASE)
  if groups:
    oauth_token = groups.group(1)
  if not authenticity_token or not oauth_token:
    raise urlfetch.Error
  str = urllib.urlencode({'authenticity_token': authenticity_token, 'oauth_token': oauth_token,
                          'session[username_or_email]': username, 'session[password]': password})
  result = urlfetch.fetch(SIGNIN_URL, str, urlfetch.POST)
  if 'Invalid user name or password' in result.content:
    raise TwitterAuthenticationError
  groups = re.search(r'<code>(.*)</code>', result.content, re.IGNORECASE)
  if groups:
    oauth_pin = groups.group(1)
    return oauth_pin
  else:
    raise urlfetch.Error
