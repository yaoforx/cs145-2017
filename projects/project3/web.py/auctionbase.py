#!/usr/bin/env python

import sys; sys.path.insert(0, 'lib') # this line is necessary for the rest
import os                             # of the imports to work!

import web
import sqlitedb
from jinja2 import Environment, FileSystemLoader
from datetime import datetime

###########################################################################################
##########################DO NOT CHANGE ANYTHING ABOVE THIS LINE!##########################
###########################################################################################

######################BEGIN HELPER METHODS######################

# helper method to convert times from database (which will return a string)
# into datetime objects. This will allow you to compare times correctly (using
# ==, !=, <, >, etc.) instead of lexicographically as strings.

# Sample use:
# current_time = string_to_time(sqlitedb.getTime())

def string_to_time(date_str):
    return datetime.strptime(date_str, '%Y-%m-%d %H:%M:%S')

# helper method to render a template in the templates/ directory
#
# `template_name': name of template file to render
#

# `**context': a dictionary of variable names mapped to values
# that is passed to Jinja2's templating engine
#
# See curr_time's `GET' method for sample usage
#
# WARNING: DO NOT CHANGE THIS METHOD
def render_template(template_name, **context):
    extensions = context.pop('extensions', [])
    globals = context.pop('globals', {})

    jinja_env = Environment(autoescape=True,
            loader=FileSystemLoader(os.path.join(os.path.dirname(__file__), 'templates')),
            extensions=extensions,
            )
    jinja_env.globals.update(globals)

    web.header('Content-Type','text/html; charset=utf-8', unique=True)

    return jinja_env.get_template(template_name).render(context)

#####################END HELPER METHODS#####################

urls = ('/currtime', 'curr_time',
        '/selecttime', 'select_time',
        '/add_bid','bidItem',
        '/search','search',
        '/view','view'
        # TODO: add additional URLs here
        # first parameter => URL, second parameter => class name
        )
class bidItem:
    def GET(self):
        return render_template('add_bid.html', message = "To bid item here")
    def POST(self):
        post_params = web.input()
        itemID = post_params["itemID"]
        userID = post_params["userID"]
        price = post_params["price"]
        result = sqlitedb.bidItem(itemID,userID,price)

        if result:
            return render_template('add_bid.html', message = "Just bid it!", getResult = result)
        else:
            return render_template('add_bid.html', message = "No match found", getResult = result)

class search:
    def GET(self):
        return render_template('search.html', message = "Searching for auction", search_result = None)

    def POST(self):
        post_param = web.input()

        itemID = post_param["itemID"]
        userID = post_param["userID"]
        category = ""
        description = ""
        minPrice = ""
        maxPrice = ""
        status = ""
        if 'category' in post_param:
            category = post_param["category"] 
        if "description" in post_param:
            description = post_param["description"]
        if "minPrice" in post_param:
            minPrice = post_param["minPrice"]
        if "maxPrice"in post_param:
            maxPrice = post_param["maxPrice"]
        if "status" in post_param:
            status = post_param["status"]

        result = sqlitedb.getAuction(itemID, userID, category, description, minPrice, maxPrice, status)


        if result[0]:
            return render_template('search.html', message = "Found match", search_result = result[1])
        else: 
            return render_template('search.html', message = "No match found", search_result = result[1])

class view:
    def GET(self):
        get_param = web.input()
        itemId = get_param["itemID"]
        result = sqlitedb.getInfo(itemId)

        return render_template('view.html', item_info = result[0],bidder_info = result[1],status = result[2],category = result[3])

class curr_time:
    # A simple GET request, to '/currtime'
    #
    # Notice that we pass in `current_time' to our `render_template' call
    # in order to have its value displayed on the web page
    def GET(self):
        current_time = sqlitedb.getTime()
        return render_template('curr_time.html', time = current_time)

class select_time:
    # Aanother GET request, this time to the URL '/selecttime'
    def GET(self):
        return render_template('select_time.html')

    # A POST request
    #
    # You can fetch the parameters passed to the URL
    # by calling `web.input()' for **both** POST requests
    # and GET requests
    def POST(self):
        post_params = web.input()
        MM = post_params['MM']
        dd = post_params['dd']
        yyyy = post_params['yyyy']
        HH = post_params['HH']
        mm = post_params['mm']
        ss = post_params['ss'];
        enter_name = post_params['entername']


        selected_time = '%s-%s-%s %s:%s:%s' % (yyyy, MM, dd, HH, mm, ss)
        update_message = '(Hello, %s. Previously selected time was: %s.)' % (enter_name, selected_time)
        # TODO: save the selected time as the current time in the database

        # Here, we assign `update_message' to `message', which means
        # we'll refer to it in our template as `message'
        return render_template('select_time.html', message = update_message)

###########################################################################################
##########################DO NOT CHANGE ANYTHING BELOW THIS LINE!##########################
###########################################################################################

if __name__ == '__main__':
    web.internalerror = web.debugerror
    app = web.application(urls, globals())
    app.add_processor(web.loadhook(sqlitedb.enforceForeignKey))
    app.run()
