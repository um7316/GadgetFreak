#!/bin/bash

source ../bin/activate
uwsgi --socket :8001 --module GadgetFreak.wsgi
