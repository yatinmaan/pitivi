# -*- coding: utf-8 -*-
# Pitivi video editor
# Copyright (C) 2020 Andrew Hazel, Thomas Braccia, Troy Ogden, Robert Kirkpatrick
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2.1 of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this program; if not, see <http://www.gnu.org/licenses/>.
"""Tests for the pitivi.clip_properties.color module."""
# pylint: disable=protected-access
from unittest import mock

from gi.repository import GES

from pitivi.clipproperties import ClipProperties
from tests import common
from tests.test_undo_timeline import BaseTestUndoTimeline


class ColorPropertiesTest(BaseTestUndoTimeline):
    """Tests for the ColorProperties class."""

    def test_create_hard_coded(self):
        """Exercise creation of a color test clip."""
        # Wait until the project creates a layer in the timeline.
        common.create_main_loop().run(until_empty=True)

        from pitivi.timeline.timeline import TimelineContainer
        timeline_container = TimelineContainer(self.app, editor_state=self.app.gui.editor.editor_state)
        timeline_container.set_project(self.project)
        self.app.gui.editor.timeline_ui = timeline_container

        clipproperties = ClipProperties(self.app)
        clipproperties.new_project_loaded_cb(None, self.project)
        self.project.pipeline.get_position = mock.Mock(return_value=0)

        clipproperties.create_color_clip_cb(None)
        clips = self.layer.get_clips()
        pattern = clips[0].get_vpattern()
        self.assertEqual(pattern, GES.VideoTestPattern.SOLID_COLOR)

        self.action_log.undo()
        self.assertListEqual(self.layer.get_clips(), [])

        self.action_log.redo()
        self.assertListEqual(self.layer.get_clips(), clips)

    def test_color_change(self):
        """Exercise the changing of colors for color clip."""
        # Wait until the project creates a layer in the timeline.
        common.create_main_loop().run(until_empty=True)

        from pitivi.timeline.timeline import TimelineContainer
        timeline_container = TimelineContainer(self.app, editor_state=self.app.gui.editor.editor_state)
        timeline_container.set_project(self.project)
        self.app.gui.editor.timeline_ui = timeline_container

        clipproperties = ClipProperties(self.app)
        clipproperties.new_project_loaded_cb(None, self.project)
        self.project.pipeline.get_position = mock.Mock(return_value=0)

        clipproperties.create_color_clip_cb(None)

        color_expander = clipproperties.color_expander
        color_picker_mock = mock.Mock()
        color_picker_mock.calculate_argb.return_value = 1 << 24 | 2 << 16 | 3 << 8 | 4
        color_expander._color_picker_value_changed_cb(color_picker_mock)
        color = color_expander.source.get_child_property("foreground-color")[1]
        self.assertEqual(color, 0x1020304)
