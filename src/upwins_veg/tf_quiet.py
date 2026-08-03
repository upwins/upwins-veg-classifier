"""Silence TensorFlow's benign CUDA/XLA startup and autotuning chatter.

Importing TensorFlow on a GPU box prints a wall of messages that look alarming
and are not. The ones this module exists to hide:

``E ... Unable to register cuFFT/cuDNN/cuBLAS factory: ... already been registered``
    Two copies of the CUDA plugin libraries are loaded in one process, each
    registering the same factory. In the devcontainer that is because the
    ``nvcr.io/nvidia/tensorflow`` base image already ships NVIDIA's TensorFlow
    build while ``requirements.txt`` pins stock ``tensorflow==2.17.0``, so pip
    installs the PyPI wheel over it along with the ``nvidia-*`` CUDA wheels.
    Harmless -- TensorFlow and the GPU both work -- but it is an environment
    duplication, not pure noise. Fixing it at the source means not reinstalling
    TensorFlow in the container; until then, it is silenced here.

``I ... could not open file to read NUMA node`` / ``kernel may have been built without NUMA support``
    The container does not expose ``/sys/bus/pci/devices/*/numa_node``.
    TensorFlow says so and carries on against node 0. Cosmetic.

``W ... gpu_timer.cc: Skipping the delay kernel, measurement accuracy will be reduced``
    XLA skipped a timing technique it uses when autotuning kernels, so its
    *measurements* are less precise and it may pick a slightly slower kernel.
    It never changes numerical results. Printed many times during training and
    prediction, which is why it is the noisiest of the group.

``WARNING: All log messages before absl::InitializeLog() is called ...``
    Ordering artifact, and the reason the obvious fix does not work on its own.

Why ``TF_CPP_MIN_LOG_LEVEL`` alone is not enough
------------------------------------------------
The env var gates TensorFlow's logging sink, and it must be set before
TensorFlow is imported. But the cuFFT/cuDNN/cuBLAS errors and the NUMA notices
are written *straight to file descriptor 2* by absl before ``absl::InitializeLog``
has configured that sink -- the "All log messages before absl::InitializeLog()"
line says so explicitly. No env var and no ``contextlib.redirect_stderr`` can
catch them, because both operate above the file descriptor. Redirecting fd 2
itself is what works.

Under Jupyter this cuts cleanly: ``sys.stderr`` is an IPython stream object, not
fd 2, so redirecting the descriptor suppresses only the C++ layer's output.
Python tracebacks and anything written through ``sys.stderr`` still reach you.

The trade-off
-------------
``TF_CPP_MIN_LOG_LEVEL='3'`` filters INFO, WARNING *and* ERROR, so it hides
genuine TensorFlow errors too. If something later fails in a way you cannot
explain, re-run with the noise turned back on before concluding anything::

    tf = import_tensorflow(log_level='0')
"""

import contextlib
import os
import sys

__all__ = ['quiet_stderr', 'import_tensorflow']


@contextlib.contextmanager
def quiet_stderr():
    """Discard anything written to the *file descriptor* stderr inside the block.

    Use this around TensorFlow calls that emit C++ chatter of their own -- most
    usefully ``model.fit`` and ``model.predict``, which is where the repeated
    ``gpu_timer`` warnings come from::

        with quiet_stderr():
            history = model.fit(...)

    Python-level output is unaffected: in Jupyter ``sys.stderr`` is not fd 2, so
    tracebacks still display. The descriptor is restored even if the block
    raises.
    """
    sys.stderr.flush()
    saved_fd = os.dup(2)
    devnull_fd = os.open(os.devnull, os.O_WRONLY)
    try:
        os.dup2(devnull_fd, 2)
        yield
    finally:
        # Restore first, so anything printed while unwinding an exception is
        # visible rather than going to /dev/null.
        os.dup2(saved_fd, 2)
        os.close(devnull_fd)
        os.close(saved_fd)


def import_tensorflow(log_level='3'):
    """Import TensorFlow quietly and return the module.

    Drop-in replacement for ``import tensorflow as tf``::

        from upwins_veg.tf_quiet import import_tensorflow
        tf = import_tensorflow()

    ``log_level`` is ``TF_CPP_MIN_LOG_LEVEL``: ``'0'`` everything, ``'1'`` filters
    INFO, ``'2'`` filters INFO+WARNING, ``'3'`` filters INFO+WARNING+ERROR.
    Default ``'3'``, since the cuFFT/cuDNN/cuBLAS lines are logged at ERROR and
    ``'2'`` therefore lets them through. Pass ``'0'`` to see everything again
    while debugging.

    If TensorFlow has already been imported in this kernel, the env var can no
    longer take effect -- it is read once, at TensorFlow's initialization. The
    already-imported module is returned and a note is printed, because silently
    doing nothing here looks like the helper failed. Restart the kernel if you
    need the setting applied.
    """
    already_imported = 'tensorflow' in sys.modules
    os.environ['TF_CPP_MIN_LOG_LEVEL'] = log_level

    with quiet_stderr():
        import tensorflow as tf

    if already_imported:
        print('tf_quiet: TensorFlow was already imported in this kernel, so '
              "TF_CPP_MIN_LOG_LEVEL='" + log_level + "' cannot take effect. "
              'Restart the kernel to apply it.')

    # absl's Python logger is separate from the C++ sink above and keeps its own
    # threshold; without this, Python-side absl warnings still print.
    try:
        import absl.logging
        absl.logging.set_verbosity(absl.logging.ERROR)
    except ImportError:
        pass

    return tf
