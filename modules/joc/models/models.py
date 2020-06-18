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
    ferro = fields.Integer(default=30, readonly=True)
    madera = fields.Integer(default=100, readonly=True)
    pedra = fields.Integer(default=60, readonly=True)
    nivell = fields.Integer(default=1, readonly=True)
    experiencia = fields.Text(string="Experiencia jugador", compute="get_experiencia")
    #CLAUS ALIENES

    atacants = fields.One2many('joc.atacants','jugador')
    atacantk = fields.One2many(related='atacants')
    defenses = fields.One2many('joc.defenses','jugador')
    defensak = fields.One2many(related='defenses')
    mines = fields.One2many('joc.mines','jugador')
    minesk = fields.One2many(related='mines')
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

    #CRON
    @api.model
    def update_resources(self):
        jugadors = self.env['res.partner'].search([('es_jugador', '=', True)])
        print('Recursos actualitzats')
        for r in jugadors:
            r.gold += 1
            for m in r.mines:
                print(m.mina.name)

                if m.mina.name == "Mina de Pedra":
                    r.pedra += 1
                elif m.mina.name == "Mina de Ferro":
                    r.ferro += 1
                elif m.mina.name == "Recolector de fusta":
                    r.madera += 1


    #MÈTODES

    # @api.model
    # def create(self,vals_list):
    #     res = super(jugador, self).create(vals_list)
    #
    #     #CODI PER A CREAR UNA MINA DE OR PER DEFECTE AL CREAR EL JUGADOR
    #     mina_or_default = self.env['joc.mina'].create({'name': 'Mina or', 'temps_produccio': 60, 'cost': 0.0, 'materials_produits':0})
    #     self.env['joc.mines'].create({'mina': mina_or_default.id, 'jugador': self._context.get('active_id'), 'temps': 60})
    #
    #     return res

    # @api.model
    # def default_get(self,fields):
    #     res = super(jugador, self).default_get(fields)
    #     mines = []
    #     mina_or_default = self.env['joc.mina'].create({'name': 'Mina or', 'temps_produccio': 60, 'cost': 0.0, 'materials_produits': 0})
    #     mina = (0,0,{
    #         'mina': mina_or_default.id,
    #         'temps': 60
    #     })
    #
    #     mines.append(mina)
    #     res.update({
    #         'mines': mines
    #     })
    #
    #     return res

# class venta_monedes(models.Model):
#     _name = 'sale.order'
#     _inherit = 'sale.order'
#
#     name = fields.Selection([('1','Pack low'),('2','Pack medium'),('3','Pack pro')])
#     start = fields.Datetime(default=lambda self: fields.Datetime.now())
#     end = fields.Datetime(compute='_get_end')
#
#     finished = fields.Boolean()
#
#     @api.depends('start')
#     def _get_end(self):
#         for s in self:
#             start = fields.Datetime.from_string(self.start)
#             start = start + timedelta(days=30)
#             s.end = fields.Datetime.to_string(start)
#             if (s.end < fields.Datetime.now()):
#                 s.write({'finished': True})

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
    cost = fields.Integer()
    nivell = fields.Integer()

class mines(models.Model):
    _name = 'joc.mines'

    #CLAUS ALIENES
    mina = fields.Many2one('joc.mina')
    jugador = fields.Many2one('res.partner', ondelete='cascade')
    temps = fields.Integer(string="Temps de producció")





class mina(models.Model):

    _name = 'joc.mina'
    name = fields.Char()
    temps_produccio = fields.Integer()
    cost = fields.Float()
    materials_produits = fields.Integer(default=0)



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
        if self.cantitat * self.atacant.cost > self.jugador.gold:
            raise ValidationError('No hi ha suficient or!')
        else:

            self.jugador.gold -= self.atacant.cost * self.cantitat
            self.env['joc.atacants'].create({'cantitat':self.cantitat,
                                            'atacant':self.atacant.id,
                                            'jugador':self.jugador.id})
            return {}

class defenses_wizard(models.TransientModel):
    _name="joc.defenses_wizard"

    state = fields.Selection([('1','Material'),('2','Cantitat'),('3','Confirmar')], default='1')

    cantitat = fields.Integer()
    defensa = fields.Many2one('joc.defensa')
    cost_material = fields.Integer(string="Cost per unitat", compute="get_cost", readonly=True)


    @api.depends('cost_material')
    def get_cost(self):
        self.cost_material = self.defensa.cost

    def _jugador_actual(self):
        return self.env['res.partner'].browse(self._context.get('active_id'))  # El context conté, entre altre coses,
        # el active_id del model que està obert.

    jugador = fields.Many2one('res.partner', default=_jugador_actual)

    @api.onchange('defensa','cantitat')
    def _onchange(self):

        self.cost_total = self.defensa.cost * self.cantitat



    material_disponible = fields.Integer(string='Material disponible', store=True, readonly=True, compute="get_material_jugador")

    @api.depends('defensa')
    def get_material_jugador(self):
        if self.defensa.name == "Muro madera":
            self.material_disponible = self.jugador.madera
        elif self.defensa.name == "Muro pedra":
            self.material_disponible = self.jugador.pedra
        elif self.defensa.name == "Muro ferro":
            self.material_disponible = self.jugador.ferro



    cost_total = fields.Integer(string="Cost total", readonly=True, store=True)



    def avant(self):


        if self.state == '1':
            if self.defensa.name != "Muro madera" and self.defensa.name != "Muro pedra" and self.defensa.name != "Muro ferro":
                raise ValidationError('Deus elegir un tipus de defensa!')
            else:
                self.state = '2'
        elif self.state == '2':
            if (self.cantitat * self.cost_material) > self.material_disponible:
                raise ValidationError('No tens suficient material')
            elif self.cantitat == 0:
                raise ValidationError('Deus elegir una cantitat')
            else:
                self.cost_total = self.cost_material* self.cantitat
                self.state = '3'


        return {
            'type': 'ir.actions.act_window',
            'res_model': self._name,
            'res_id': self.id,
            'view_mode': 'form',
            'target': 'new',
        }

    def arrere(self):
        if self.state == '2':
            self.state = '1'
        elif self.state == '3':
            self.state = '2'


        return {
            'type': 'ir.actions.act_window',
            'res_model': self._name,
            'res_id': self.id,
            'view_mode': 'form',
            'target': 'new',
        }

    @api.multi
    def create_defensa(self):

        if self.defensa.name == "Muro madera":
            self.jugador.madera -= self.cost_total
        elif self.defensa.name == "Muro pedra":
            self.jugador.pedra -= self.cost_total
        elif self.defensa.name == "Muro ferro":
            self.jugador.ferro -= self.cost_total
        self.env['joc.defenses'].create({'cantitat': self.cantitat,
                                         'defensa': self.defensa.id,
                                         'jugador': self.jugador.id})
        return {}


class mina_wizard(models.TransientModel):
    _name="joc.mina_wizard"

    mina = fields.Many2one('joc.mina')

    def _jugador_actual(self):
        return self.env['res.partner'].browse(self._context.get('active_id'))  # El context conté, entre altre coses,
        # el active_id del model que està obert.

    jugador = fields.Many2one('res.partner', default=_jugador_actual, readonly=True)

    @api.onchange('mina')
    def _onchange(self):
        self.temps = self.mina.temps_produccio


    temps = fields.Integer(readonly=True)
    or_disponible = fields.Float(string='Or disponible', store=True, readonly=True, related='jugador.gold')



    @api.model
    def action_wizard_mines(self):
        action = self.env.ref('joc.action_wizard_mines').read()[0]
        return action

    @api.multi
    def create_mina(self):
        # _logger.info(self.or_disponible)
        if self.mina.cost > self.jugador.gold:
            raise ValidationError('No hi ha suficient or!')
        else:

            self.jugador.gold -= self.mina.cost
            self.temps = self.mina.temps_produccio
            self.env['joc.mines'].create({'mina':self.mina.id, 'jugador':self.jugador.id, 'temps':self.temps})
            return {}


# # VENTES
#
# class venta_monedes(models.Model):
#     _name = 'sale.order'
#     _inherit = 'sale.order'




