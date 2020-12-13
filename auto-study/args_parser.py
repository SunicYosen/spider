import argparse

def args_sparse():
    parser = argparse.ArgumentParser()

    parser.add_argument('-c', "--chrome", action='store_true',
                        help="Show Chrome Window.")

    parser.add_argument('-l', "--login",  action='store_true',
                        help="Just Login.")

    parser.add_argument('-r', "--read",  action='store_true',
                        help="Read Articles.")

    parser.add_argument('-w', "--watch",  action='store_true',
                        help="Watch Videos.")

    parser.add_argument('-d', "--dexam",  action='store_true',
                        help="Daily Exam.")

    parser.add_argument('-x',"--wexam",  action='store_true',
                        help="Weekly Exam.")

    parser.add_argument('-v', "--sexam",  action='store_true',
                        help="Special Exam.")

    parser.add_argument('-s', "--score",  action='store_true',
                        help="Get Score.")

    parser.add_argument('-a', "--all",  action='store_true',
                        help="Read Articles & Watch Videos & Do Exams & Get Score.")
    
    args = parser.parse_args()

    return args
