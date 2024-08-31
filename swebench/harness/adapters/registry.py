from swebench.harness.adapters.go_adapter import GoAdapter
from swebench.harness.adapters.python_adapter import PythonAdapter
from swebench.harness.constants import TEST_PYTEST

ADAPTERS = {
    "scikit-learn/scikit-learn": {
        **{
            k: PythonAdapter(
                python="3.6",
                packages="numpy scipy cython pytest pandas matplotlib",
                install="python -m pip install -v --no-use-pep517 --no-build-isolation -e .",
                pip_packages=["cython", "numpy==1.19.2", "setuptools", "scipy==1.5.2"],
                test_cmd=TEST_PYTEST,
            )
            for k in ["0.20", "0.21", "0.22"]
        },
        **{
            k: PythonAdapter(
                python="3.9",
                packages="numpy scipy cython setuptools pytest pandas matplotlib joblib threadpoolctl",
                install="python -m pip install -v --no-use-pep517 --no-build-isolation -e .",
                pip_packages=["cython", "setuptools", "numpy", "scipy"],
                test_cmd=TEST_PYTEST,
            )
            for k in ["1.3", "1.4"]
        },
    },
    "caddyserver/caddy": {
        "6448": GoAdapter(
            install="go mod download",
            test_cmd="go test <file>",
        )
    },
}
