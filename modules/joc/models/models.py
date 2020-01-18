# -*- coding: utf-8 -*-

from odoo import models, fields, api


class game(models.Model):
    _name = 'joc.joc'
    name = fields.Char()


class jugador(models.Model): #Clientes de odoo
    _name = 'joc.jugador'
    name = fields.Char()
    image = fields.Binary()
    raza = fields.Selection([('1', 'Hombres'), ('2', 'Elfos'), ('3', 'Enanos'), ('4', 'Orcos')])
    materiales = fields.One2many('joc.materiales', 'jugador')

class materiales(models.Model):#Materiales de un jugador
    _name = 'joc.materiales'
    material = fields.Many2one('joc.material')
    cantidad = fields.Float()
    jugador = fields.Many2one('joc.jugador')

class material(models.Model):#Material
    _name = 'joc.material'
    name = fields.Char()
    image = fields.Binary()

class atacantes(models.Model): #Atacantes
    _name = 'joc.atacantes'
    atacante = fields.Many2one('joc.atacante')
    cantidad = fields.Float()
    jugador = fields.Many2one('joc.jugador')

class atacante(models.Model): #Atacante
    _name = 'joc.atacante'
    name = fields.Char()
    image = fields.Binary()
    ataque = fields.Float()
    vida = fields.Float()
    coste = fields.Float()








