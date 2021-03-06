#
# rmtoo
#   Free and Open Source Requirements Management Tool
#
#  xml ganttproject2 output class
#
# This is a second version of xml ganttproject output.
# This must be seen as alpha software, because there are some base
# problems which might make the use of this output module sensless:
# * How to sort things? ganttproject has a fixed order of tasks. The
#   requirements for rmtoo are unsorted.
# * Where to get the start date from?
# * Sub-tasks are done in the way, that each (sub-)topic opens up a
#   new level.  The last (innermost) level are the requirements of the
#   appropriate (sub)-topic.
#
# (c) 2010-2011 by flonatel
#
# For licencing details see COPYING
#

from xml.dom.minidom import Document
from rmtoo.lib.Requirement import Requirement
from rmtoo.lib.LaTeXMarkup import LaTeXMarkup
from rmtoo.lib.RequirementStatus import RequirementStatusNotDone, \
    RequirementStatusAssigned, RequirementStatusFinished
from rmtoo.lib.configuration.Cfg import Cfg


class xml_ganttproject_2:

    def __init__(self, topic_set, params):
        self.topic_set = topic_set
        cfg = Cfg(params)
        self.output_filename = cfg.get_value('output_filename')
        self.effort_factor = cfg.get_value_default('effort_factor', 1)
        self.req_ids = {}
        self.next_id = 1

    # Create Makefile Dependencies
    def cmad(self, reqscont, ofile):
        ofile.write("%s: ${REQS}\n\t${CALL_RMTOO}\n" % (self.output_filename))

    def set_topics(self, topics):
        self.topic_set = topics.get(self.topic_name)

    # Get an id: if the req is not there a new id will be generated.
    def get_req_id(self, name):
        if name in self.req_ids:
            return self.req_ids[name]
        self.req_ids[name] = self.next_id
        self.next_id += 1
        return self.req_ids[name]

    def output_req(self, req, reqset, doc, sobj):
        # There is the need for a unique numeric id
        xml_task = doc.createElement("task")
        xml_task.setAttribute("name", req.id)
        xml_task.setAttribute("id", str(self.get_req_id(req.id)))
        if req.is_val_av_and_not_null("Effort estimation"):
            # The Effort Estimation is only rounded: ganntproject can
            # only handle integers as duration
            xml_task.setAttribute(
                "duration",
                str(int(req.get_value("Effort estimation")
                        * self.effort_factor + 1)))

        # The Status (a la complete) must be given in percent.
        # Currently rmtoo supports only two states: not done (~0) or
        # finished (~100)
        if req.is_val_av_and_not_null("Status"):
            v = "0"
            if isinstance(req.get_status(), RequirementStatusFinished):
                v = "100"
            elif isinstance(req.get_status(), RequirementStatusAssigned):
                v = "50"
            xml_task.setAttribute("complete", v)

        # Notes
        # Add the description and if available also the rationale and
        # note.
        notes = "== Description ==\n"
        notes += LaTeXMarkup.replace_txt(req.get_value("Description")
                                         .get_content())

        if req.is_val_av_and_not_null("Rationale"):
            notes += "\n\n== Rationale ==\n"
            notes += LaTeXMarkup.replace_txt(
                req.get_value("Rationale").get_content())

        if req.is_val_av_and_not_null("Note"):
            notes += "\n\n== Note ==\n"
            notes += LaTeXMarkup.replace_txt(req.get_value("Note")
                                             .get_content())

        xml_note = doc.createElement("notes")
        xml_text = doc.createCDATASection(notes)
        xml_note.appendChild(xml_text)
        xml_task.appendChild(xml_note)

        # Dependencies
        for node in req.outgoing:
            xml_depend = doc.createElement("depend")
            xml_depend.setAttribute("id", str(self.get_req_id(node.id)))
            # There are some default attrs
            xml_depend.setAttribute("type", "2")
            xml_depend.setAttribute("difference", "0")
            xml_depend.setAttribute("hardness", "Strong")
            xml_task.appendChild(xml_depend)

        sobj.appendChild(xml_task)

    # Run through all the topics
    # (Deep first search / output)
    def output_reqset(self, reqset, doc, sobj):
        self.output_topic(self.topic_set.get_master(), reqset, doc, sobj)

    # First output all the requirements in this topic - then all the
    # subtopics. 
    def output_topic(self, topic, reqset, doc, sobj):
        # Add a new level (task)
        xml_task = doc.createElement("task")
        xml_task.setAttribute("name", topic.name)
        xml_task.setAttribute("id", str(self.get_req_id(
                    "TOPIC-" + topic.name)))

        # Run through all the requirements and output them
        for req in sorted(topic.reqs, key=lambda r: r.id):
            self.output_req(req, reqset, doc, xml_task)
        # After this have a look at the (sub-)topics
        for st in sorted(topic.outgoing, key=lambda t: t.name):
            self.output_topic(st, reqset, doc, xml_task)

        # Add the xml_task to the current document
        sobj.appendChild(xml_task)

    def output(self, reqscont):
        # Create the minidom document
        doc = Document()

        xml_project = doc.createElement("project")
        doc.appendChild(xml_project)

        # This is needed: if not given, on the left side there is
        # nothing displayed. 
        xml_taskdisplaycolumns = doc.createElement("taskdisplaycolumns")
        xml_project.appendChild(xml_taskdisplaycolumns)
        for s in [["tpd3", 125] , ["tpd4", 25], ["tpd5", 25]]:
            xml_tpd = doc.createElement("displaycolumn")
            xml_tpd.setAttribute("property-id", s[0])
            xml_tpd.setAttribute("width", str(s[1]))
            xml_taskdisplaycolumns.appendChild(xml_tpd)

        # Output all the 'tasks' (i.e. requirements)
        self.output_reqset(reqscont.continuum_latest(), doc, xml_project)

        fd = file(self.output_filename, "w")
        fd.write(doc.toprettyxml())
        fd.close()

