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

    es_jugador = fields.Boolean()
    data_creacio = fields.Datetime(default=lambda self: fields.Datetime.now())
    atac = fields.Float(string="Atac jugador", compute="get_atac")
    defensa = fields.Float(string="Defensa jugador", compute="get_def")
    gold = fields.Float(default=100, readonly=True)
    ferro = fields.Float(default=100, readonly=True)
    madera = fields.Float(default=100, readonly=True)
    pedra = fields.Float(default=100, readonly=True)
    nivell = fields.Integer(default=1, readonly=True)
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
    cantitat = fields.Integer()
    #CLAUS ALIENES

    atacant = fields.Many2one('joc.atacant')
    jugador = fields.Many2one('res.partner',ondelete='cascade')

class atacant(models.Model):
    _name = 'joc.atacant'
    name = fields.Char()
    image = fields.Binary()
    atac = fields.Float()
    vida = fields.Float()
    cost = fields.Float()


class defenses(models.Model):
    _name = 'joc.defenses'
    cantitat = fields.Integer()

    #CLAUS ALIENES

    defensa = fields.Many2one('joc.defensa')
    jugador = fields.Many2one('res.partner',ondelete='cascade')

class defensa(models.Model):
    _name = 'joc.defensa'
    name = fields.Char()
    image = fields.Binary()
    vida = fields.Float()
    cost = fields.Float()
    nivell = fields.Integer()

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

#WIZARDS

class atacants_wizard(models.TransientModel):
    _name="joc.atacants_wizard"

    cantitat = fields.Integer()
    atacant = fields.Many2one('joc.atacant')

    def _jugador_actual(self):
        return self.env['res.partner'].browse(self._context.get('active_id'))  # El context conté, entre altre coses,
        # el active_id del model que està obert.

    jugador = fields.Many2one('res.partner', default=_jugador_actual)

    @api.onchange('atacant','cantitat')
    def _onchange(self):
        self.or_disponible = self.jugador.gold - self.atacant.cost * self.cantitat



    or_disponible = fields.Float(string='Or disponible', store=True, readonly=True)



    @api.model
    def action_wizard_atacants(self):
        action = self.env.ref('joc.action_wizard_atacants').read()[0]
        return action

    @api.multi
    def create_atacants(self):
        # _logger.info(self.or_disponible)
        # if self.or_disponible < 0:
        #     raise ValidationError('No hi ha suficient or!')
        # else:
        self.jugador.gold -= self.atacant.cost * self.cantitat
        self.env['joc.atacants'].create({'cantitat':self.cantitat,
                                        'atacant':self.atacant.id,
                                        'jugador':self.jugador.id})
        return {}