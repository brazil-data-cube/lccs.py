#
# This file is part of Land Cover Classification System Web Service.
# Copyright (C) 2020-2021 INPE.
#
# Land Cover Classification System Web Service is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.
#
"""Python API client wrapper for LCCS-WS."""
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

        return mysld.as_sld()
