# -*- coding: utf-8 -*-
# (c) 2017 Diagram Software S.L.
# (c) 2017 Consultoría Informática Studio 73 S.L.
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from odoo import api, models, fields, _


class L10nEsAeatSii(models.Model):
    _name = 'l10n.es.aeat.sii'

    name = fields.Char(string="Name")
    state = fields.Selection([
        ('draft', 'Draft'),
        ('active', 'Active')
    ], string="State", default="draft")
    file = fields.Binary(string="File", required=True)
    folder = fields.Char(string="Folder Name", required=True)
    date_start = fields.Date(string="Start Date")
    date_end = fields.Date(string="End Date")
    public_key = fields.Char(string="Public Key", readonly=True)
    private_key = fields.Char(string="Private Key", readonly=True)
    company_id = fields.Many2one(
        comodel_name="res.company",
        string="Compañía",
        required=True,
        default=lambda self: self.env.user.company_id.id
    )

    def load_password_wizard(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': _('Insert Password'),
            'res_model': 'l10n.es.aeat.sii.password',
            'view_mode': 'form',
            'views': [(False, 'form')],
            'target': 'new',
        }

    def action_active(self):
        self.ensure_one()
        other_configs = self.search([('id', '!=', self.id),
                                     ('company_id', '=', self.company_id.id)])
        for config_id in other_configs:
            config_id.state = 'draft'
        self.state = 'active'
