# -*- coding: utf-8 -*-

from odoo import models, fields, api


class game(models.Model):
    _name = 'joc.joc'
    name = fields.Char()


class jugador(models.Model): #Clientes de odoo
    _name = 'joc.jugador'
    name = fields.Char()
    image = fields.Binary()
    atac = fields.Float()
    defensa = fields.Float()
    gold = fields.Float()
    ferro = fields.Float()
    madera = fields.Float()
    pedra = fields.Float()
    nivell = fields.Float()

    #CLAUS ALIENES

    atacants = fields.One2many('joc.atacants','jugador')
    defenses = fields.One2many('joc.defenses','jugador')
    mines = fields.One2many('joc.mines','jugador')
    event = fields.Many2many('joc.event','jugador')

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
    nivell = fields.Float()

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