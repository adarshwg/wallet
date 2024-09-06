import re
import unittest
from unittest.mock import patch, MagicMock
import authentication
from authentication import Authentication
from Errors import UserNotFoundException, InvalidPasswordException


