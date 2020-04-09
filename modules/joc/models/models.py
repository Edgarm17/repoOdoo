# -*- coding: utf-8 -*-

from odoo import models, fields, api
from datetime import datetime, timedelta

class game(models.Model):
    _name = 'joc.joc'
    name = fields.Char()


class jugador(models.Model): #Clientes de odoo
    _name = 'joc.jugador'
    name = fields.Char()
    image = fields.Binary()

    data_creacio = fields.Datetime(default=lambda self: fields.Datetime.now())
    atac = fields.Float(string="Atac jugador", compute="get_atac")
    defensa = fields.Float()
    gold = fields.Float()
    ferro = fields.Float()
    madera = fields.Float()
    pedra = fields.Float()
    nivell = fields.Float()
    experiencia = fields.Text(string="Experiencia jugador", compute="get_experiencia")
    #CLAUS ALIENES

    atacants = fields.One2many('joc.atacants','jugador')
    atacantk = fields.One2many(related='atacants')
    defenses = fields.One2many('joc.defenses','jugador')
    mines = fields.One2many('joc.mines','jugador')
    event = fields.Many2many('joc.event','jugador')

    #FUNCIONS

    @api.depends('atac')
    def get_atac(self):
        for i in self:
            for r in i.atacants:
                i.atac += (r.atacant.atac * r.cantitat)

    @api.depends('experiencia')
    def get_experiencia(self):
        for i in self:
            data_actual = datetime.now()
            diferencia = data_actual - i.data_creacio
            i.experiencia = "Hores d'experiència: "+str(int(diferencia.seconds / 3600))+" h."

class atacants(models.Model):
    _name = 'joc.atacants'
    cantitat = fields.Float()
    #CLAUS ALIENES

    atacant = fields.Many2one('joc.atacant')
    jugador = fields.Many2one('joc.jugador')

class atacant(models.Model):
    _name = 'joc.atacant'
    name = fields.Char()
    image = fields.Binary()
    atac = fields.Float()
    vida = fields.Float()
    cost = fields.Float()


class defenses(models.Model):
    _name = 'joc.defenses'
    cantitat = fields.Float()

    #CLAUS ALIENES

    defensa = fields.Many2one('joc.defensa')
    jugador = fields.Many2one('joc.jugador')

class defensa(models.Model):
    _name = 'joc.defensa'
    name = fields.Char()
    image = fields.Binary()
    vida = fields.Float()
    cost = fields.Float()
    nivell = fields.Float()

class mines(models.Model):
    _name = 'joc.mines'
    tipus = fields.Selection([('1','Mina or'),('2','Mina pedra'),('3','Mina ferro')])
    temps_produccio = fields.Float()
    cost = fields.Float()
    materials_produits = fields.Float()

    #CLAUS ALIENES

    jugador = fields.Many2one('joc.jugador')

class event(models.Model):
    _name = 'joc.event'
    name = fields.Char()
    data_inicial = fields.Date()
    data_final = fields.Date()

    #CLAU ALIENA

    jugador = fields.Many2many('joc.jugador')