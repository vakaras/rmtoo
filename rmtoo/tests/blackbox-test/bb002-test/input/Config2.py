import os

class Config:

    basedir = "tests/blackbox-test/bb002-test/"
    result_is = os.environ["rmtoo_test_dir"]

    stakeholders = ["development", "management", "users", "customers"]

    inventors = ["flonatel", ]

    reqs_spec = \
        {
           "directory": basedir + "input/reqs",
           "commit_interval": ["a92e470b9bdc87673530bbe9cc8a57afe6d832e2", 
                               "a92e470b9bdc87673530bbe9cc8a57afe6d832e2"],
           "default_language": "en_GB",
        }

    topic_specs = \
        {
          "ts_common": [basedir + "input/topics", "ReqsDocument"],
        }

    analytics_specs = \
        {
           "stop_on_errors": False,
           "topics": "ts_common",
        }
    
    output_specs = \
        [ 
          ["prios", 
           ["ts_common", result_is + "/reqsprios.tex", 
            {"start_date": "2011-05-10" }]],

          ["graph",
           ["ts_common", result_is + "/req-graph1.dot"]],

          ["graph2",
           ["ts_common", result_is + "/req-graph2.dot"]],

          ["stats_reqs_cnt", 
           ["ts_common", result_is + "/stats_reqs_cnt.csv"]],

          ["latex2", 
           ["ts_common", result_is + "/reqtopics.tex"]],

          ["html", 
           ["ts_common", 
            result_is + "/html", basedir + "input/header.html",
            basedir + "input/footer.html"]],

          ["xml_ganttproject_2",
           ["ts_common", result_is + "/gantt2.xml", 1]],
        ]
