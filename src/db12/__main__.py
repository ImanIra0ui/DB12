
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
import argparse
import json
from pkg_resources import get_distribution, DistributionNotFound

from db12 import single_dirac_benchmark
from db12 import multiple_dirac_benchmark
from db12 import wholenode_dirac_benchmark
from db12 import jobslot_dirac_benchmark

try:
    VERSION = get_distribution("db12").version
except DistributionNotFound:
    pass

def dump_as_json(filename, output):
    '''Function to save result to a json file'''
    with open(filename, 'w') as outfile:
        json.dump(output, outfile)

def single_dirac_benchmark_cli(args):
    #pylint: disable=unused-argument
    '''Function that calls single_dirac_benchmark and prints
    its results and returns them'''
    result = single_dirac_benchmark()["NORM"]
    print(result)
    return result

def jobslot_dirac_benchmark_cli(args):
    '''Function that calls jobslot_dirac_benchmark and prints
    its results and returns them'''
    result = jobslot_dirac_benchmark(args.iterations, args.extra_iteration)
    print(
        result["copies"], result["sum"],
        result["arithmetic_mean"],
        result["geometric_mean"],
        result["median"],
    )
    print(" ".join([str(j) for j in result["raw"]]))
    return result

def multiple_dirac_benchmark_cli(args):
    '''Function that calls multiple_dirac_benchmark and prints
    its results and returns them'''
    result = multiple_dirac_benchmark(int(args.copy), args.iterations, args.extra_iteration)
    print(
        result["copies"],
        result["sum"],
        result["arithmetic_mean"],
        result["geometric_mean"],
        result["median"],
    )
    print(" ".join([str(k) for k in result["raw"]]))
    return result

def wholenode_dirac_benchmark_cli(args):
    '''Function that calls wholenode_dirac_benchmark and prints
    its results and returns them'''
    result = wholenode_dirac_benchmark(args.iterations, args.extra_iteration)
    print(
        result["copies"],
        result["sum"],
        result["arithmetic_mean"],
        result["geometric_mean"],
        result["median"],
    )
    print(" ".join([str(j) for j in result["raw"]]))
    return result

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

    iterations = 1

    parser = argparse.ArgumentParser(description=help_string)
    #pylint: disable=line-too-long
    parser.add_argument("--iterations", nargs='?', type=int, help="number of iterations to perform", default=iterations)
    parser.add_argument("--extra-iteration", help="whether an extra iteration is needed", action='store_true')
    parser.add_argument("--json", help="generate json files", action='store_true')
    parser.add_argument("copy", help="number of copies", nargs='?', const='', default='')
    parser.add_argument('--version', action='version', version=VERSION, default='')

    subparsers = parser.add_subparsers(dest='parser')
    parser_single = subparsers.add_parser('single')
    parser_single.set_defaults(func=single_dirac_benchmark_cli)

    parser_wholenode = subparsers.add_parser('wholenode')
    parser_wholenode.set_defaults(func=wholenode_dirac_benchmark_cli)

    parser_jobslot = subparsers.add_parser('jobslot')
    parser_jobslot.set_defaults(func=jobslot_dirac_benchmark_cli)

    parser_multiple = subparsers.add_parser('multiple')
    parser_multiple.set_defaults(func=multiple_dirac_benchmark_cli)

    args = parser.parse_args()

    args.func(args)

#
# If we run as a command
#
if __name__ == "__main__":
    main()
