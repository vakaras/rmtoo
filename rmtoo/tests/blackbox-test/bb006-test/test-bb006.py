#
# Blackbox rmtoo tests
#
# (c) 2010 by flonatel
#
# For licencing details see COPYING
#

import os

from rmtoo.lib.RmtooMain import main
from rmtoo.tests.lib.BBHelper import prepare_result_is_dir, compare_results, \
    cleanup_std_log, delete_result_is_dir, extract_container_files, \
    unify_output_dir, check_file_results

mdir = "tests/blackbox-test/bb006-test"

class TestBB006:

    def test_pos_001(self):
        "BB Basic with one requirement - check makefile dependencies"

        def myexit(n):
            pass

        mout, merr = prepare_result_is_dir()
        main(["-f", mdir + "/input/Config1.py", "-m", "..", "-c",
              os.path.join(os.environ["rmtoo_test_dir"], "makefile_deps")],
             mout, merr, exitfun=myexit)
        cleanup_std_log(mout, merr)
        unify_output_dir("makefile_deps")
        check_file_results(mdir)
        delete_result_is_dir()
