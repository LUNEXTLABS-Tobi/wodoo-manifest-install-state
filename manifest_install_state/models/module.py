from odoo import _, api, fields, models, SUPERUSER_ID
from pathlib import Path
from odoo.exceptions import UserError, RedirectWarning, ValidationError


class Module(models.Model):
    _inherit = "ir.module.module"

    should_be_installed = fields.Boolean(
        compute="_compute_shoule_be_installed", search="_search_should_be_installed"
    )
    should_be_uninstalled = fields.Boolean(
        compute="_compute_shoule_be_installed", search="_search_should_be_uninstalled"
    )

    @api.model
    def _get_MANIFEST(self):
        candidates = [
            "/opt/src/MANIFEST",
            "/home/odoo/src/user/MANIFEST",
        ]
        for candi in candidates:
            candi = Path(candi)
            if candi.exists():
                break
        else:
            return {}
        return eval(candi.read_text())

    def _compute_shoule_be_installed(self):
        manifest = self._get_MANIFEST()
        install = set(manifest.get("install", []))
        uninstall = set(manifest.get("install", []))
        for rec in self:
            rec.should_be_installed = rec.name in install
            rec.should_be_uninstalled = rec.name in uninstall

    def _search_should_be_installed(self, operator, value):
        if operator == "=":
            if value:
                ids = self.search([]).filtered(lambda x: x.should_be_installed).ids
                return [('id', 'in', ids)]
        raise NotImplementedError(f"{operator=}")

    def _search_should_be_uninstalled(self, operator, value):
        if operator == "=":
            if value:
                ids = self.search([]).filtered(lambda x: x.should_be_uninstalled).ids
                return [('id', 'in', ids)]
        raise NotImplementedError(f"{operator=}")