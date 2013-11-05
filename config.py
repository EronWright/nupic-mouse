
mouse_config = {
    'min_probability': 0.20,
    'serialization': {
        'path': '/tmp/mouse1'
    },
}

maze_config = {

    'layout':"""
    0 1 0 1;
    1 1 1 1;
    1 0 1 0
    """,
    'initial_location':(0,1),
    'cheese':"""
    0 0 0 2;
    1 0 0 0;
    0 0 9 0
    """,
}
