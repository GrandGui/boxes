# Copyright (C) 2013-2014 Florian Festi
#
#   This program is free software: you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation, either version 3 of the License, or
#   (at your option) any later version.
#
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
#
#   You should have received a copy of the GNU General Public License
#   along with this program.  If not, see <http://www.gnu.org/licenses/>.

from boxes import *

class StackableABox(Boxes):
    """An improvement of simple Box with stackable and modular grooves."""

    description = "This box is kept as simple as ABox with grooves in every direction. The grooves are repeated to create a modular pattern"

    ui_group = "Box"
    ui_name = "Stackable A Box"

    def __init__(self) -> None:
        Boxes.__init__(self)
        self.addSettingsArgs(edges.FingerJointSettings)
        self.addSettingsArgs(edges.ModGroovedSettings)

        self.argparser.add_argument(
            "--M_x",action="store",type=int,default=1,
            help="Number of module in x dimension"
        )
        self.argparser.add_argument(
            "--M_y",action="store",type=int,default=1,
            help="Number of module in y dimension"
        )
        self.argparser.add_argument(
            "--M_h",action="store",type=int,default=1,
            help="Number of module in h dimension"
       )
        self.argparser.add_argument(
            "--top_edge",
            action="store",
            type=ArgparseEdgeType("FhseaA"),
            choices=list("FhseaA"),
            default="a",
            help="edge type for top edge",
        )

        self.argparser.add_argument(
            "--bottom_edge",
            action="store",
            type=ArgparseEdgeType("FhseaA"),
            choices=list("FhseaA"),
            default="A",
            help="edge type for bottom edge",
        )

        self.buildArgParser("outside")

    def render(self):
        M = self.ModGrooved_module
        x, y, h = self.M_x * M, self.M_y * M, self.M_h * M
        t = self.thickness

        top = self.edges.get(self.top_edge, self.edges["e"])
        bot = self.edges.get(self.bottom_edge, self.edges["F"])

        sideedge = "F" # if self.vertical_edges == "finger joints" else "h"

        if self.outside:
            self.x = x = self.adjustSize(x, sideedge, sideedge)
            self.y = y = self.adjustSize(y)
            self.h = h = self.adjustSize(h, bot, top)

        with self.saved_context():
            self.rectangularWall(x, h, [bot, sideedge, top, sideedge],
                                 ignore_widths=[1, 6], move="up",label="Front Wall")
            self.rectangularWall(x, h, [bot, sideedge, top, sideedge],
                                 ignore_widths=[1, 6], move="up",label="Back Wall")

            if self.bottom_edge != "e":
                self.rectangularWall(x, y, "ffff", move="up",label="Bottom Panel")

        self.rectangularWall(x, h, [bot, sideedge, top, sideedge],
                             ignore_widths=[1, 6], move="right only",label="Back Wall")
        self.rectangularWall(y, h, [bot, "f", top, "f"],
                             ignore_widths=[1, 6], move="up",label="Left Wall")
        self.rectangularWall(y, h, [bot, "f", top, "f"],
                             ignore_widths=[1, 6], move="up",label="Right Wall")