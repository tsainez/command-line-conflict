import pytest
from command_line_conflict.utils.profiler import profile, profiler

class TestProfilerDecorator:

    def setup_method(self):
        # Reset the profiler metrics buffer before each test
        profiler.metrics_buffer.clear()
        # Ensure enabled is False initially to not leak state
        profiler.enabled = False
        # Prevent auto-flushing during tests which clears the buffer
        profiler.last_flush_time = float('inf')

    def test_profile_decorator_when_enabled(self):
        """Test that the @profile decorator records metrics when profiler is enabled."""
        profiler.enabled = True

        @profile
        def sample_func(a, b):
            return a + b

        result = sample_func(2, 3)

        assert result == 5
        assert len(profiler.metrics_buffer) == 1

        # Check metric format
        metric = profiler.metrics_buffer[0]
        assert len(metric) == 6
        # The 4th index is function name
        assert metric[4] == "sample_func"

    def test_profile_decorator_when_disabled(self):
        """Test that the @profile decorator does not record metrics when disabled."""
        profiler.enabled = False

        @profile
        def sample_func(a, b):
            return a * b

        result = sample_func(4, 5)

        assert result == 20
        assert len(profiler.metrics_buffer) == 0

    def test_profile_decorator_preserves_metadata(self):
        """Test that @profile uses functools.wraps properly."""

        @profile
        def my_documented_func():
            """This is a docstring."""
            pass

        assert my_documented_func.__name__ == "my_documented_func"
        assert my_documented_func.__doc__ == "This is a docstring."

    def test_profile_decorator_handles_kwargs(self):
        """Test that the @profile decorator passes kwargs correctly."""
        profiler.enabled = True

        @profile
        def sample_func(a, b=10):
            return a + b

        result = sample_func(2, b=5)

        assert result == 7
        assert len(profiler.metrics_buffer) == 1
        assert profiler.metrics_buffer[0][4] == "sample_func"
