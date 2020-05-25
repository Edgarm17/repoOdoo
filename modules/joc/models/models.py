# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import ValidationError
from datetime import datetime, timedelta
import re
import logging

_logger = logging.getLogger(__name__)

class game(models.Model):
    _name = 'joc.joc'
    name = fields.Char()


class jugador(models.Model): #Clientes de odoo
    _name = 'res.partner'
    _inherit = 'res.partner'
    # name = fields.Char( required=True)
    image = fields.Binary()
    correu = fields.Char(string='Correu')

    data_creacio = fields.Datetime(default=lambda self: fields.Datetime.now())
    atac = fields.Float(string="Atac jugador", compute="get_atac")
    defensa = fields.Float(string="Defensa jugador", compute="get_def")
    gold = fields.Float(default=100, readonly=True)
    ferro = fields.Float(default=100, readonly=True)
    madera = fields.Float(default=100, readonly=True)
    pedra = fields.Float(default=100, readonly=True)
    nivell = fields.Float(default=1, readonly=True)
    experiencia = fields.Text(string="Experiencia jugador", compute="get_experiencia")
    #CLAUS ALIENES

    atacants = fields.One2many('joc.atacants','jugador')
    atacantk = fields.One2many(related='atacants')
    defenses = fields.One2many('joc.defenses','jugador')
    defensak = fields.One2many(related='defenses')
    mines = fields.One2many('joc.mines','jugador')
    evento = fields.Many2many('joc.evento','jugador')

    #FUNCIONS

    @api.depends('atac')
    def get_atac(self):
        for i in self:
            for r in i.atacants:
                i.atac += (r.atacant.atac * r.cantitat)

    @api.depends('defensa')
    def get_def(self):
        for i in self:
            for r in i.defenses:
                i.defensa += (r.defensa.vida * r.cantitat)

    @api.depends('experiencia')
    def get_experiencia(self):
        for i in self:
            data_actual = datetime.now()
            diferencia = data_actual - i.data_creacio
            i.experiencia = "Hores d'experiència: "+str(int(diferencia.seconds / 3600))+" h."

    #RESTRICCIONS

    @api.constrains('correu')
    def _check_correu(self):
        regex = re.compile('^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$', re.IGNORECASE)
        for s in self:
            if regex.match(s.correu):
                _logger.info('El correu es correcte')
            else:
                raise ValidationError('El correu no es vàlid!')

    _sql_constraints = [('correu_uniq','unique(correu)','Ja existeix un jugador amb aquest correu!')]

class atacants(models.Model):
    _name = 'joc.atacants'
    cantitat = fields.Float()
    #CLAUS ALIENES

    atacant = fields.Many2one('joc.atacant')
    jugador = fields.Many2one('res.partner')

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
    jugador = fields.Many2one('res.partner')

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

    jugador = fields.Many2one('res.partner')

class evento(models.Model):
    _name = 'joc.evento'
    name = fields.Char()
    data_inicial = fields.Date()
    data_final = fields.Date()

    #CLAU ALIENA

    jugador = fields.Many2many('res.partner')