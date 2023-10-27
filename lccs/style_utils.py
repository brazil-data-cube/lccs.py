#
# This file is part of Python Client Library for the LCCS-WS.
# Copyright (C) 2022 INPE.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <https://www.gnu.org/licenses/gpl-3.0.html>.
#
"""Python API client wrapper for LCCS-WS."""
from lxml.etree import tostring
import sld
import os


class SldGenerator:
    """Class to create and manipulated styles."""

    @classmethod
    def create_sld(cls, options: dict, rules: list, layer_name='', userstyletitle=None, featuretypestylename=None):
        """Create the rules for style."""
        # set the default values
        options.setdefault('stroke', '#232323')
        options.setdefault('stroke-width', '0.5')
        options.setdefault('point_size', '8')
        options.setdefault('point_type', 'circle')
        options.setdefault('property_name', 'class_id')
        options.setdefault('comparator', '==')

        mysld = sld.StyledLayerDescriptor()
        nl = mysld.create_namedlayer(layer_name)
        us_style = nl.create_userstyle()
        if userstyletitle is not None:
            us_style.Title = str(userstyletitle)
        fts = us_style.create_featuretypestyle()
        if featuretypestylename is not None:
            us_style.Name = str(featuretypestylename)

        for i in rules:
            rule = fts.create_rule(title=i['rule_label'], symbolizer=sld.PointSymbolizer)
            rule.PointSymbolizer.Graphic.Mark.Fill.CssParameters[0].Value = i['fill_color']
            rule.PointSymbolizer.Graphic.Size = options['point_size']
            rule.PointSymbolizer.Graphic.Mark.WellKnownName = options['point_type']

            rule.Filter = rule.create_filter(propname=options['property_name'], comparitor=options['comparator'],
                                             value=f"{i['property_literal']}")

        mysld.normalize()

        localschema_backup_path = './StyledLayerDescriptor-backup.xsd'
        os.remove(localschema_backup_path)

        return tostring(mysld._node, pretty_print=False, encoding="utf-8")
