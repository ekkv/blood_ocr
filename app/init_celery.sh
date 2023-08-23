#!/bin/bash

python load_model.py init

celery -A tasks worker -l Info -P eventlet