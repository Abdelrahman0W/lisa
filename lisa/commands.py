import functools
from argparse import Namespace
from typing import Iterable, Optional, cast

import lisa.runner
from lisa import notifier
from lisa.parameter_parser.runbook import load_runbook
from lisa.testselector import select_testcases
from lisa.testsuite import LisaTestRuntimeData, TestStatus
from lisa.util import LisaException, constants
from lisa.util.logger import get_logger

_get_init_logger = functools.partial(get_logger, "init")


async def run(args: Namespace) -> int:
    runbook = load_runbook(args.runbook, args.variables)

    if runbook.notifier:
        notifier.initialize(runbooks=runbook.notifier)

    try:
        runner = lisa.runner.LisaRunner(verbosity=2)
        results = runner.play(runbook)
        # results = await lisa.runner.run(runbook)
    finally:
        notifier.finalize()

    return sum(1 for x in results if x.status == TestStatus.FAILED)


# check runbook
async def check(args: Namespace) -> int:
    load_runbook(args.runbook, args.variables)
    return 0


async def list_start(args: Namespace) -> int:
    runbook = load_runbook(args.runbook, args.variables)
    list_all = cast(Optional[bool], args.list_all)
    log = _get_init_logger("list")
    if args.type == constants.LIST_CASE:
        if list_all:
            cases: Iterable[LisaTestRuntimeData] = select_testcases()
        else:
            cases = select_testcases(runbook.testcase)
        for case_data in cases:
            log.info(
                f"test: {case_data.name}, case: {case_data.metadata.case.name}, "
                f"area: {case_data.suite.area}, "
                f"category: {case_data.suite.category}, "
                f"tags: {','.join(case_data.suite.tags)}, "
                f"priority: {case_data.priority}"
            )
    else:
        raise LisaException(f"unknown list type '{args.type}'")
    log.info("list information here")
    return 0
