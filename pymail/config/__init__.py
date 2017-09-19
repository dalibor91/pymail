from importlib import import_module

def context_config(context):
        return import_module("config.%s" % context).config
