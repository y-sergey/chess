python3 -m cProfile -o myLog.profile main_c_profile.py
gprof2dot -f pstats myLog.profile -o callingGraph_1.dot