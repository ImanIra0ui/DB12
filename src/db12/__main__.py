
""" DIRAC Benchmark 2012 by Ricardo Graciani, and wrapper functions to
    run multiple copies in parallel by Andrew McNab.
    This file (dirac_benchmark.py) is intended to be the ultimate upstream
    shared by different users of the DIRAC Benchmark 2012 (DB12). The
    canonical version can be found at https://github.com/DIRACGrid/DB12
    This script can either be imported or run from the command line:
    ./dirac_benchmark.py NUMBER
    where NUMBER gives the number of benchmark processes to run in parallel.
    Run  ./dirac_benchmark.py help  to see more options.
"""
from __future__ import print_function
from __future__ import division
from __future__ import absolute_import
import sys
import argparse
from pkg_resources import get_distribution, DistributionNotFound

from db12 import single_dirac_benchmark
from db12 import multiple_dirac_benchmark
from db12 import wholenode_dirac_benchmark
from db12 import jobslot_dirac_benchmark

try:
    VERSION = get_distribution("package-name").version
except DistributionNotFound:
    pass

def main():
    """Main function"""
    help_string = """dirac_benchmark.py [--iterations ITERATIONS] [--extra-iteration]
                  [COPIES|single|wholenode|jobslot|version|help] 
Uses the functions within dirac_benchmark.py to run the DB12 benchmark from the 
command line.
By default one benchmarking iteration is run, in addition to the initial 
iteration which DB12 runs and ignores to avoid ramp-up effects at the start.
The number of benchmarking iterations can be increased using the --iterations
option. Additional iterations which are also ignored can be added with the 
--extra-iteration option  to avoid tail effects. In this case copies which
finish early run additional iterations until all the measurements finish.
The COPIES (ie an integer) argument causes multiple copies of the benchmark to
be run in parallel. The tokens "wholenode", "jobslot" and "single" can be 
given instead to use $MACHINEFEATURES/total_cpu, $JOBFEATURES/allocated_cpu, 
or 1 as the number of copies respectively. If $MACHINEFEATURES/total_cpu is
not available, then the number of (logical) processors visible to the 
operating system is used.
Unless the token "single" is used, the script prints the following results to
two lines on stdout:
COPIES SUM ARITHMETIC-MEAN GEOMETRIC-MEAN MEDIAN
RAW-RESULTS
The tokens "version" and "help" print information about the script.
The source code of dirac_benchmark.py provides examples of how the functions
within dirac_benchmark.py can be used by other Python programs.
dirac_benchmark.py is distributed from  https://github.com/DIRACGrid/DB12
"""

    copies = None
    iterations = 1
    extra_iteration = False

    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument("--iterations", action="store_true")
    parser.add_argument("--extra-iteration", action="store_true")
    parser.add_argument("--help", action="store_true")
    parser.add_argument("a", nargs='?', const='', default='')

    args = parser.parse_args()
    if args.iterations:
        iterations = int(args[13:])
    elif args.extra_iteration:
        extra_iteration = True
    elif args.help or args.a == "help":
        print(help_string)
        sys.exit(0)
    elif not args.a.startswith("--"):
        copies = args

    if copies == "version":
        print(VERSION)
        sys.exit(0)

    if copies is None or copies == "single":
        print(single_dirac_benchmark()["NORM"])
        sys.exit(0)

    if copies == "wholenode":
        result = wholenode_dirac_benchmark(
            iterations_num=iterations, extra_iter=extra_iteration
        )
        print(
            result["copies"],
            result["sum"],
            result["arithmetic_mean"],
            result["geometric_mean"],
            result["median"],
        )
        print(" ".join([str(j) for j in result["raw"]]))
        sys.exit(0)

    if copies == "jobslot":
        result = jobslot_dirac_benchmark(
            iterations_num=iterations, extra_iter=extra_iteration
        )
        print(
            result["copies"],
            result["sum"],
            result["arithmetic_mean"],
            result["geometric_mean"],
            result["median"],
        )
        print(" ".join([str(j) for j in result["raw"]]))
        sys.exit(0)

    result = multiple_dirac_benchmark(
        copies=int(copies), iterations_num=iterations, extra_iter=extra_iteration
    )
    print(
        result["copies"],
        result["sum"],
        result["arithmetic_mean"],
        result["geometric_mean"],
        result["median"],
    )
    print(" ".join([str(k) for k in result["raw"]]))
    sys.exit(0)

#
# If we run as a command
#
if __name__ == "__main__":
    main()
