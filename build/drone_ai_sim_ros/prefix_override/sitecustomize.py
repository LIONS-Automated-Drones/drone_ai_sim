import sys
if sys.prefix == '/usr':
    sys.real_prefix = sys.prefix
    sys.prefix = sys.exec_prefix = '/home/raytech/repos/drone_ai_sim/install/drone_ai_sim_ros'
