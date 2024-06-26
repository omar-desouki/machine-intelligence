import traceback
import threading, _thread, ctypes
import time, json, os, fnmatch
import argparse
from typing import Any, Callable, Dict, List, Tuple, Union
from queue import Queue

from helpers.globals import *
from helpers.utils import *

root = "testcases"

def get_test_cases(path: str, pattern: str) -> List[Dict[str, Any]]:
    test_cases = []
    for filename in os.listdir(path):
        if filename.startswith("__"): continue
        if not fnmatch.fnmatchcase(filename, pattern): continue
        filepath = os.path.join(path, filename)
        if os.path.isfile(filepath) and os.path.splitext(filepath)[1] == ".json":
            test_cases.append(json.load(open(filepath, 'r')))

    return test_cases

def read_problems() -> Tuple[str, List[Dict[Any, str]]]:
    data = json.load(open(os.path.join(root, "problems.json")))
    return data.get("name", ""), data.get("problems", [])

def raise_exception_in_thread(thread: threading.Thread, exception: Exception):
    tid = thread.ident
    ctypes.pythonapi.PyThreadState_SetAsyncExc(ctypes.c_long(tid), ctypes.py_object(exception))

def run_test(fn: Callable, input_args: Arguments, cmp: Callable, cmp_args: Arguments, timeout: 10) -> Union[Result, None]:
    def _call(queue: Queue):
        try:
            output = fn(*input_args.args, **input_args.kwargs)
            result = cmp(output, *cmp_args.args, **cmp_args.kwargs)
        except NotImplementedError as err:
            result = None
        except:
            result = Result(False, 0, traceback.format_exc())
        queue.put(result)
    queue = Queue()
    thread = threading.Thread(target=_call, args=(queue,), daemon=True)
    thread.start()
    start = time.time()
    try:
        thread.join(timeout)
    except KeyboardInterrupt:
        raise_exception_in_thread(thread, KeyboardInterrupt())
        raise
    elapsed = time.time() - start
    if queue.empty():
        if elapsed >= timeout:
            result = Result(False, 0, "Timeout")
        else:
            result = Result(False, 0, "Run Failed")
    else:
        result = queue.get()
    raise_exception_in_thread(thread, KeyboardInterrupt())
    del thread
    return result

def default_comparator(output, expected):
    success = output == expected
    grade = (1 if success else 0)
    message = ""
    if not success:
        message = f"Expected {expected} but got {output}"
    return Result(success, grade, message)

def approximate_comparator(output, expected):
    success = output == expected
    if not success:
        success = abs(output - expected)/(abs(output) + abs(expected)) < 1e-8
    grade = (1 if success else 0)
    message = ""
    if not success:
        message = f"Expected {expected} but got {output}"
    return Result(success, grade, message)

class Problem:
    def __init__(self, **kwargs) -> None:
        self.name = kwargs.get("name", "Unnamed Problem")
        self.testcases_path = kwargs.get("testcases_path", self.name)
        self.default_fn = lambda x: x
        if "function" in kwargs: self.default_fn = eval(kwargs["function"])
        self.default_cmp = default_comparator
        if "comparator" in kwargs: self.default_cmp = eval(kwargs["comparator"])
        self.weight = kwargs.get("weight", 1)
        self.default_timeout = kwargs.get("timeout", 1)
        self.grade = 0
        self.maximum_grade = 0
    
    def run(self, is_debug: bool = False, pattern: str = "*", time_scale: float = 1):
        print(f"Problem: {self.name}")
        test_cases = get_test_cases(os.path.join(root, self.testcases_path), pattern)
        self.grade = 0
        self.maximum_grade = 0
        for test_index, test_case in enumerate(test_cases):
            description = test_case.get("description", f"Test Case {test_index+1}")
            timeout = test_case.get("timeout", self.default_timeout)
            if is_debug:
                print(f"{test_index+1}: {description} :: time-limit is turned off in debug mode")
            else:
                print(f"{test_index+1}: {description} :: time-limit = {timeout*time_scale} sec")
            fn = self.default_fn
            if "function" in test_case: fn = eval(test_case["function"])
            input_args = test_case.get("input_args", [])
            input_kwargs = test_case.get("input_kwargs", {})
            fn_args = Arguments(
                [eval(arg) for arg in input_args], {key:eval(value) for key, value in input_kwargs.items()})
            cmp = self.default_cmp
            if "comparator" in test_case: cmp = eval(test_case["comparator"])
            cmp_args = Arguments(
                [eval(arg) for arg in test_case.get("comparison_args", [])],
                {key:eval(value) for key, value in test_case.get("comparison_kwargs", {}).items()})
            weight = test_case.get("weight", 1)
            maximum_grade = self.weight * weight * test_case.get("maximum_grade", 1)
            self.maximum_grade += maximum_grade
            result = run_test(fn, fn_args, cmp, cmp_args, (None if is_debug else timeout * time_scale))
            if result is None:
                print("Function is not implemented yet")
                continue
            grade = self.weight * weight * result.grade
            if result.success:
                print(f"Result: PASS {grade:g}/{maximum_grade:g}", end="")
                if result.message:
                    print(" -", result.message)
                else:
                    print()
            else:
                print(f"Result: FAIL {grade:g}/{maximum_grade:g} - {result.message}")
                if input_args:
                    print("Input positional arguments:")
                    for arg in input_args: print(f"- {arg}")
                if input_kwargs:
                    print(f"Input keyword arguments:")
                    for key, val in input_kwargs.items(): print(f"- {key}: {val}")
                print()
            self.grade += grade
        print(f"Total {self.grade:g}/{self.maximum_grade:g}")

def main(args: argparse.Namespace):
    time_scale = args.timescale
    if time_scale.lower() == "default":
        import speed_test
        time_scale = speed_test.get_time_limit_multiplier()
    else:
        time_scale = float(time_scale)

    name, problems = read_problems()
    set_solution_path(args.solution)
    problems = [Problem(**problem) for problem in problems]
    print(f"\n{name}\n")
    total_grade = 0
    maximum_grade = 0
    if args.question != "all":
        try:
            questions: str = args.question.replace("\\", "/")
            exclude = False
            if questions.startswith("~"):
                questions = questions[1:]
                exclude = True
            questions = [
                (question.split("/") if "/" in question else [question, "*"]) 
                for question in questions.split(",")
            ]
            selected = {int(index)-1: pattern for index, pattern in questions}
            if exclude:
                problems = [(problem, "*") for index, problem in enumerate(problems) if index not in selected]
            else:
                problems = [(problem, selected[index]) for index, problem in enumerate(problems) if index in selected]
        except:
            pass
    else:
        problems = [(problem, "*") for index, problem in enumerate(problems)]
    for problem, pattern in problems:
        problem.run(args.debug, pattern, time_scale)
        print()
        total_grade += problem.grade
        maximum_grade += problem.maximum_grade
    print(f"Problem Set Total {total_grade:g}/{maximum_grade:g}\n")
    exit(total_grade)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Automatically grades the solutions for the problem set")
    parser.add_argument("--question", "-q", default="all", help="choose the question(s) to include in the grading (or prefix with ~ to exclude). A question number can be followed by a slash / followed by a glob pattern to filter the testcases.")
    parser.add_argument("--debug", "-d", action="store_true", help="Disables timeout to enable debugging via the autograder")
    parser.add_argument("--timescale", "-t", type=str, default="default", help="A scaling factor for the timeout")
    parser.add_argument("--solution", "-s", default="")
    args = parser.parse_args()
    main(args)