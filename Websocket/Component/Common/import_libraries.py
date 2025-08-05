# -*- coding: utf-8 -*-
import asyncio
import base64
import cv2
import datetime
import json
import logging
import logging.handlers
import math
import os
import re
import socket
import subprocess
import shutil
import sys
import time
import websockets
import yaml

from cv2 import VideoCapture
from logging import DEBUG, INFO
from websockets import ClientConnection