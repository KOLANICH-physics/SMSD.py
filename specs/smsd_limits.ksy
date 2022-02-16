meta:
  id: smsd_limits
  title: Limits imposed by SMSD LAN protocol specs on the values of quantities and variables

instances:
  speed_max_max_limit:
    value: 15600
  speed_max_min_limit:
    value: 16
  speed_min_max_limit:
    value: 950
  speed_movement_min_limit:
    value: speed_max_min_limit - 1
