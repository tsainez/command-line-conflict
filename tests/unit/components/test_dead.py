from command_line_conflict.components.dead import Dead


def test_dead_initialization():
    dead = Dead()
    assert hasattr(dead, "timer")
    assert dead.timer == 0.0


def test_dead_initialization_with_timer():
    dead = Dead(timer=5.0)
    assert dead.timer == 5.0
