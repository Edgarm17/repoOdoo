# -*- coding: utf-8 -*-

from odoo import models, fields, api


class game(models.Model):
    _name = 'joc.joc'
    name = fields.Char()


class jugador(models.Model):
    _name = 'joc.jugador'
    nombre = fields.Char()
    raza = fields.Selection([('1', 'Hombres'), ('2', 'Elfos'), ('3', 'Enanos'), ('4', 'Orcos')])
    bando = fields.Selection([('1', 'Luz'), ('2', 'Oscuridad')])
    imagen = fields.Binary()
    raws = fields.One2many('joc.materiales','jugador')



class materiales(models.Model):
    _name = 'joc.materiales'
    nombre = fields.Char()
    cantidad = fields.Float()
    jugador = fields.Many2one('joc.jugador')
    material = fields.Many2one('joc.material')


class material(models.Model):
    _name = 'joc.material'
    nombre = fields.Char()
    imagen = fields.Binary()



