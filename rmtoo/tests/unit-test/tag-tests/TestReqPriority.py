#
# rmtoo
#   Free and Open Source Requirements Management Tool
#
# Unit test for ReqPriority
#
# (c) 2010-2011 by flonatel
#
# For licencing details see COPYING
#

from rmtoo.modules.ReqPriority import ReqPriority
from rmtoo.lib.Requirement import Requirement
from rmtoo.lib.RMTException import RMTException
from rmtoo.tests.lib.ReqTag import create_parameters
from rmtoo.lib.storagebackend.RecordEntry import RecordEntry

class TestReqPriority:

    def test_positive_01(self):
        "Requirement Tag Priority - no tag given"
        config, req = create_parameters()

        rt = ReqPriority(config)
        name, value = rt.rewrite("Priority-test", req)
        assert(name == "Factor")
        assert(value == 0.0)

    def test_positive_02(self):
        "Requirement Tag Priority - tag given one stakeholder"
        config, req = create_parameters()
        config.set_value('requirements.stakeholders',
                         ["marketing", "security"])
        req["Priority"] = RecordEntry("Priority", "marketing:7")

        rt = ReqPriority(config)
        name, value = rt.rewrite("Priority-test", req)
        assert(name == "Factor")
        assert(value == 0.7)

    def test_positive_03(self):
        "Requirement Tag Priority - tag given two stakeholders"
        config, req = create_parameters()
        config.set_value('requirements.stakeholders',
                         ["marketing", "security"])
        req["Priority"] = RecordEntry("Priority", "marketing:7 security:3")

        rt = ReqPriority(config)
        name, value = rt.rewrite("Priority-test", req)
        assert(name == "Factor")
        assert(value == 0.5)

    def test_negative_01(self):
        "Requirement Tag Priority - faulty priority declaration ':'"
        config, req = create_parameters()
        config.set_value('requirements.stakeholders',
                         ["marketing", "security"])
        req["Priority"] = RecordEntry("Priority", "marketing:")

        rt = ReqPriority(config)
        try:
            name, value = rt.rewrite("Priority-test", req)
            assert(False)
        except RMTException, rmte:
            assert(rmte.id() == 12)

    def test_negative_02(self):
        "Requirement Tag Priority - invalid stakeholder"
        config, req = create_parameters()
        config.set_value('requirements.stakeholders',
                         ["marketing", "security"])
        req["Priority"] = RecordEntry("Priority", "nixda:3")

        rt = ReqPriority(config)
        try:
            name, value = rt.rewrite("Priority-test", req)
            assert(False)
        except RMTException, rmte:
            assert(rmte.id() == 13)

    def test_negative_03(self):
        "Requirement Tag Priority - stakeholder voted more than once"
        config, req = create_parameters()
        config.set_value('requirements.stakeholders',
                         ["marketing", "security"])
        req["Priority"] = RecordEntry("Priority",
                                      "security:3 marketing:7 security:4")

        rt = ReqPriority(config)
        try:
            name, value = rt.rewrite("Priority-test", req)
            assert(False)
        except RMTException, rmte:
            assert(rmte.id() == 14)

    def test_negative_04(self):
        "Requirement Tag Priority - invalid priority (too big)"
        config, req = create_parameters()
        config.set_value('requirements.stakeholders',
                         ["marketing", "security"])
        req["Priority"] = RecordEntry("Priority", "security:30")

        rt = ReqPriority(config)
        try:
            name, value = rt.rewrite("Priority-test", req)
            assert(False)
        except RMTException, rmte:
            assert(rmte.id() == 15)

    def test_negative_05(self):
        "Requirement Tag Priority - invalid priority (too small)"
        config, req = create_parameters()
        config.set_value('requirements.stakeholders',
                         ["marketing", "security"])
        req["Priority"] = RecordEntry("Priority", "security:-10")

        rt = ReqPriority(config)
        try:
            name, value = rt.rewrite("Priority-test", req)
            assert(False)
        except RMTException, rmte:
            assert(rmte.id() == 15)
