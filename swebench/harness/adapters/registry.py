from swebench.harness.adapters.adapter import Adapter
from swebench.harness.adapters.go_adapter import GoAdapter
from swebench.harness.adapters.python_adapter import PythonAdapter
from swebench.harness.adapters.javascript_adapter import (
    JavaScriptAdapter,
    jest_log_parser,
)
from swebench.harness.constants import TEST_PYTEST
from swebench.harness.log_parsers import MAP_REPO_TO_PARSER

ADAPTERS: dict[str, dict[str, Adapter]] = {
    "scikit-learn/scikit-learn": {
        **{
            k: PythonAdapter(
                python="3.6",
                packages="numpy scipy cython pytest pandas matplotlib",
                install="python -m pip install -v --no-use-pep517 --no-build-isolation -e .",
                pip_packages=["cython", "numpy==1.19.2", "setuptools", "scipy==1.5.2"],
                test_cmd=TEST_PYTEST,
                log_parser=MAP_REPO_TO_PARSER["scikit-learn/scikit-learn"],
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
                log_parser=MAP_REPO_TO_PARSER["scikit-learn/scikit-learn"],
            )
            for k in ["1.3", "1.4"]
        },
    },
    "caddyserver/caddy": {
        "6411": GoAdapter(
            version="1.23.0",
            install=["go mod download"],
            test_cmd='go test -v . -run "TestReplacerNew*"',
        ),
        "6345": GoAdapter(
            version="1.23.0",
            install=["go mod download"],
            test_cmd="go test -v ./caddytest/integration/...",
        ),
        "6115": GoAdapter(
            version="1.23.0",
            install=["go mod download"],
            test_cmd="go test -v ./modules/caddyhttp/reverseproxy/...",
        ),
        "6051": GoAdapter(
            version="1.23.0",
            install=["go mod download"],
            test_cmd="go test -v ./caddyconfig/caddyfile/...",
        ),
        "5404": GoAdapter(
            version="1.20.14",
            install=["go mod download"],
            test_cmd="go test -v ./caddyconfig/caddyfile/...",
        ),
    },
    "babel/babel": {
        "14532": JavaScriptAdapter(
            version="20",
            test_cmd="yarn jest babel-generator --verbose",
            pre_test_commands=["make build"],  # Need to rebuild before testing
            install=[
                "make bootstrap",
                "make build",
            ],
            log_parser=jest_log_parser,
        ),
        "13928": JavaScriptAdapter(
            version="20",
            test_cmd='yarn jest babel-parser -t "arrow" --verbose',
            pre_test_commands=["make build"],  # Need to rebuild before testing
            install=[
                "make bootstrap",
                "make build",
            ],
            log_parser=jest_log_parser,
        ),
        "15649": JavaScriptAdapter(
            version="20",
            test_cmd="yarn jest packages/babel-traverse/test/scope.js --verbose",
            pre_test_commands=["make build"],  # Need to rebuild before testing
            install=[
                "make bootstrap",
                "make build",
            ],
            log_parser=jest_log_parser,
        ),
        "15445": JavaScriptAdapter(
            version="20",
            test_cmd='yarn jest packages/babel-generator/test/index.js -t "generation " --verbose',
            pre_test_commands=["make build"],  # Need to rebuild before testing
            install=[
                "make bootstrap",
                "make build",
            ],
            log_parser=jest_log_parser,
        ),
        "16130": JavaScriptAdapter(
            version="20",
            test_cmd="yarn jest babel-helpers --verbose",
            pre_test_commands=["make build"],  # Need to rebuild before testing
            install=[
                "make bootstrap",
                "make build",
            ],
            log_parser=jest_log_parser,
        ),
    },
}
