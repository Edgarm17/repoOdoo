from odoo import models, fields, api
from odoo.exceptions import ValidationError
from datetime import datetime, timedelta
import re
import logging

class batalla(models.Model):
    _name = 'joc.batalla'
    name = fields.Char()
    jugador1 = fields.Many2Many('')