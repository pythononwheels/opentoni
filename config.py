#
#
# pow settings file
# 
import simplejson as json
import opentoni.encoders
import os
import logging

server_settings = {
    "base_url"          :   "http://localhost",
    "port"              :   8080,
    "debug"             :   True,
    "https"             :   False,
    "template_path"     :   os.path.join(os.path.dirname(__file__), "views"),
    "static_url_prefix" :   "/static/",
    "static_path"       :   os.path.join(os.path.dirname(__file__), "static"),
    "login_url"         :   "/login",
    "xsrf_cookies"      :   False,
    #"log_function"      :   you can give your own log function here.
    "cookie_secret"     :   "1827fe5e-c2b1-40fc-9930-21b83aaf6550"
}

templates = {
    "template_path"     :   server_settings["template_path"],
    "handler_path"      :   os.path.join(os.path.dirname(__file__), "handlers"),
    "model_path"        :   os.path.join(os.path.dirname(__file__), "models"),
    "stubs_path"        :   os.path.join(os.path.dirname(__file__), "stubs"),
    "views_path"        :   os.path.join(os.path.dirname(__file__), "views")
}

myapp = {
    "app_name"          :   "opentoni",
    "default_format"    :   "json",
    "supported_formats" :   ["json", "csv", "xml", "html"],
    "encoder"           :   {
            "json"  :   json,
            "csv"   :   opentoni.encoders.JsonToCsv(),
            "xml"   :   opentoni.encoders.JsonToXml()
    },
    "page_size"         :   5,
    "enable_authentication"     :   False,   # False, simple or custom
    "sql_auto_schema"   :   True,
    "logfile"           :   os.path.join(os.path.dirname(__file__),"pow.log"),
    "logformat"         :   logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'),
    "id_pattern"        :   "[0-9\-a-zA-Z]+",       # the regex used to math IDs in URLs (uuid in this case)
    "list_separator"    :   ",",
    "date_format"       :   "%Y-%m-%dT%H:%M:%S",
    "internal_fields"   :   ["created_at", "last_updated", "id"]        # these cannot be changed in the scaffolded views
    #"environment"       :   "development"       # set the current environment (also see the db section)
}

db_base_path = r"c:\khz\devel\opentoni"
database = {
    "sql"   : {
        "type"      :   "sqlite",
        "dbname"    :   r"c:\khz\devel\opentoni\db.sqlite",   # better leave the r to enable absolute paths with backslashes 
        "host"      :   None,       
        "port"      :   None,   
        "user"      :   None,
        "passwd"    :   None,
        "enabled"   :   True          # switch currently unused
    },
    "tinydb" : {
        "dbname"    :   r"c:\khz\devel\opentoni\tiny.db",   # better leave the r to enable absolute paths with backslashes 
        "host"      :   None,       
        "port"      :   None,   
        "user"      :   None,
        "passwd"    :   None,
        "enabled"   :   False       # switch currently unused
    },
    "mongodb" : {
        "dbname"    :   "testdb",  
        "host"      :   "localhost",       
        "port"      :   27017,   
        "user"      :   None,
        "passwd"    :   None,
        "enabled"   :   False       # switch currently unused
    },
    "elastic" : {
        "dbname"    :   "testdb",   # == elasticsearch index 
        "hosts"     :   ["localhost"],       
        "port"      :   9200,   
        "user"      :   None,
        "passwd"    :   None,
        "enabled"   :   False       # switch currently unused
    }
}

beta_settings = {
    # Beta settings are erxperimental. You can find details for each Beta setting
    # on www.pythononwheels.org/beta
    
    # Name          :    Enabled ?
    "dot_format"    :   True
}

#from handlers.very_raw_own_handler import VeryRawOwnHandler
routes = [
            #(r'.*', VeryRawOwnHandler)
        ]

