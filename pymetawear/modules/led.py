#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
:mod:`led`
==================

Created by hbldh <henrik.blidh@nedomkull.com>
Created on 2016-04-16

"""

from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals
from __future__ import absolute_import

from ctypes import byref

from pymetawear import libmetawear
from pymetawear.exceptions import PyMetaWearException
from pymetawear.modules.base import PyMetaWearModule
from pymetawear.mbientlab.metawear.peripheral import Led


class LEDModule(PyMetaWearModule):

    def __init__(self, board, debug=False):
        super(LEDModule, self).__init__(board, debug)

    def __str__(self):
        return "{0}".format(self.module_name)

    def __repr__(self):
        return str(self)

    @property
    def module_name(self):
        return "LED"

    @property
    def sensor_name(self):
        return 'LED'

    def notifications(self, callback=None):
        """Subscribe or unsubscribe to switch notifications.

        No subscriptions possible for LED module.

        """
        raise PyMetaWearException(
            "No notifications available for LED module.")

    def load_preset_pattern(self, preset_name, **kwargs):
        """Loads a preset configuration.

        :param str preset_name: One of the strings `blink`, `pulse` or `solid`.
        :return: The preset pattern.
        :rtype: :py:class:`pymetawear.mbientlab.metawear.peripheral.Led.Pattern`

        """
        preset = self._get_preset(preset_name.lower())
        pattern = Led.Pattern(**kwargs)
        libmetawear.mbl_mw_led_load_preset_pattern(byref(pattern), preset)
        return pattern

    def write_pattern(self, pattern, color):
        """Writes the led pattern to the board.

        :param pattern:
        :param str color: `g`, `b` or 'r'

        """
        color = self._get_color(color.lower())
        libmetawear.mbl_mw_led_write_pattern(byref(pattern), color)

    def play(self):
        """Executes any stored LED pattern."""
        libmetawear.mbl_mw_led_play(self.board)

    def autoplay(self):
        """Plays any programmed patterns, and immediately plays
        any patterns programmed later.
        """
        libmetawear.mbl_mw_led_autoplay(self.board)

    def pause(self):
        """Pause any playing LED pattern."""
        libmetawear.mbl_mw_led_pause(self.board)

    def stop(self):
        """Stop any playing LED pattern."""
        libmetawear.mbl_mw_led_stop(self.board)

    def stop_and_clear(self):
        """Stop any playing LED pattern. and clears
        all pattern cofigurations.
        """
        libmetawear.mbl_mw_led_stop_and_clear(self.board)

    def _get_color(self, s):
        return {
            'g': Led.COLOR_GREEN,
            'r': Led.COLOR_RED,
            'b': Led.COLOR_BLUE
        }.get(s, Led.COLOR_GREEN)

    def _get_preset(self, s):
        return {
            'blink': Led.PRESET_BLINK,
            'pulse': Led.PRESET_PULSE,
            'solid': Led.PRESET_SOLID
        }.get(s, Led.PRESET_BLINK)
