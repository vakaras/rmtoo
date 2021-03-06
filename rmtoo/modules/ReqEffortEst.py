#
# rmtoo
#   Free and Open Source Requirements Management Tool
#
# Requirement Management Toolset
#
# (c) 2010-2011 by flonatel
#
# For licencing details see COPYING
#

#
# The 'Effort estimation' must be one of
#   0, 1, 2, 3, 5, 8, 13, 21, 34
#

from rmtoo.lib.ReqTagGeneric import ReqTagGeneric
from rmtoo.lib.RMTException import RMTException

class ReqEffortEst(ReqTagGeneric):
    tag = "Effort estimation"
    ltype = set(["reqtag", ])

    valid_values = [0, 1, 2, 3, 5, 8, 13, 21, 34]

    def __init__(self, config):
        ReqTagGeneric.__init__(self, config)

    def rewrite(self, rid, req):
    	# This is optional
        tag, value = self.handle_optional_tag(req)
        if value == None:
            return tag, value

        v = int(value.get_content())

        if v not in self.valid_values:
            raise RMTException(4, "%s: effort estimation must be one of %s"
                               % (rid, self.valid_values))
        return tag, v

