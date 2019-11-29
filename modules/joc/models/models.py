# -*- coding: utf-8 -*-

from odoo import models, fields, api


class game(models.Model):
    _name = 'joc.joc'
    name = fields.Char()


class jugador(models.Model): #Clientes de odoo
    _name = 'joc.jugador'
    nombre = fields.Char()
    raza = fields.Selection([('1', 'Hombres'), ('2', 'Elfos'), ('3', 'Enanos'), ('4', 'Orcos')])
    bando = fields.Selection([('1', 'Luz'), ('2', 'Oscuridad')])
    imagen = fields.Binary()
    materiales = fields.One2many('joc.materiales','jugador')

class produccion(models.Model): #Tabla de produccion de recursos
    _name = 'joc.producion'
    nombre = fields.Char()
    recurso = fields.Many2one('joc.recurso') #El recurso que produce
    nivel = fields.Integer() #Cuánto consume en cada producción del recurso segun el nivel
    material = fields.Many2one('joc.material') # El material que gasta para producir
    produccion = fields.Float() #Número de producciones por unidad de tiempo

class coste(models.Model):
    _name = 'joc.coste'
    nombre = fields.Char()
    recurso = fields.Many2one('joc.recurso')
    nivel = fields.Integer() #Indica lo que consume en cada nivel
    material = fields.Many2one('joc.material') #Material del coste
    coste = fields.Float() #Coste

class recurso(models.Model):
    _name = 'joc.recurso'
    nombre = fields.Char()
    nivel = fields.Float()
    imagen = fields.Binary()
    producciones = fields.One2many('joc.produccion','recurso')
    coste = fields.One2many('joc.coste','recurso')

class material(models.Model):
    _name = 'joc.material'
    nombre = fields.Char()
    imagen = fields.Binary()
    cantidad = fields.Float()
    jugador = fields.Many2one('joc.jugador')








