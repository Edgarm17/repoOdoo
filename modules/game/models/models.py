# -*- coding: utf-8 -*-

from odoo import models, fields, api


class game(models.Model):

     _name = 'game.game'
     name = fields.Char()
     value = fields.Integer()


