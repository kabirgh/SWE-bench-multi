from swebench.harness.adapters.adapter import Adapter
from swebench.harness.adapters.cplusplus_adapter import (
    CPlusPlusAdapter,
    jq_log_parser,
    redis_log_parser,
)
from swebench.harness.adapters.go_adapter import GoAdapter
from swebench.harness.adapters.python_adapter import PythonAdapter
from swebench.harness.adapters.javascript_adapter import (
    JavaScriptAdapter,
    jest_log_parser,
    vitest_log_parser,
)
from swebench.harness.adapters.rust_adapter import RustAdapter
from swebench.harness.constants import TEST_PYTEST
from swebench.harness.log_parsers import MAP_REPO_TO_PARSER

ADAPTERS: dict[str, dict[str, Adapter]] = {
    "scikit-learn/scikit-learn": {
        **{
            k: PythonAdapter(
                python="3.6",
                packages="numpy scipy cython pytest pandas matplotlib",
                install=[
                    "python -m pip install -v --no-use-pep517 --no-build-isolation -e ."
                ],
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
                install=[
                    "python -m pip install -v --no-use-pep517 --no-build-isolation -e ."
                ],
                pip_packages=["cython", "setuptools", "numpy", "scipy"],
                test_cmd=TEST_PYTEST,
                log_parser=MAP_REPO_TO_PARSER["scikit-learn/scikit-learn"],
            )
            for k in ["1.3", "1.4"]
        },
    },
    "caddyserver/caddy": {
        "6411": GoAdapter(
            version="1.23",
            install=["go mod tidy"],
            test_cmd='go test -v . -run "TestReplacerNew*"',
        ),
        "6345": GoAdapter(
            version="1.23",
            # compile the test binary, which downloads relevant packages. faster than go mod tidy
            install=["go test -c ./caddytest/integration/..."],
            test_cmd="go test -v ./caddytest/integration/...",
        ),
        "6115": GoAdapter(
            version="1.23",
            install=["go test -c ./modules/caddyhttp/reverseproxy/..."],
            test_cmd="go test -v ./modules/caddyhttp/reverseproxy/...",
        ),
        "6051": GoAdapter(
            version="1.23",
            install=["go test -c ./caddyconfig/caddyfile/..."],
            test_cmd="go test -v ./caddyconfig/caddyfile/...",
        ),
        "5404": GoAdapter(
            version="1.20",
            install=["go test -c ./caddyconfig/caddyfile/..."],
            test_cmd="go test -v ./caddyconfig/caddyfile/...",
        ),
    },
    "babel/babel": {
        "14532": JavaScriptAdapter(
            version="20",
            test_cmd="yarn jest babel-generator --verbose",
            install=["make bootstrap"],
            build=["make build"],
            log_parser=jest_log_parser,
        ),
        "13928": JavaScriptAdapter(
            version="20",
            test_cmd='yarn jest babel-parser -t "arrow" --verbose',
            install=["make bootstrap"],
            build=["make build"],
            log_parser=jest_log_parser,
        ),
        "15649": JavaScriptAdapter(
            version="20",
            test_cmd="yarn jest packages/babel-traverse/test/scope.js --verbose",
            install=["make bootstrap"],
            build=["make build"],
            log_parser=jest_log_parser,
        ),
        "15445": JavaScriptAdapter(
            version="20",
            test_cmd='yarn jest packages/babel-generator/test/index.js -t "generation " --verbose',
            install=["make bootstrap"],
            build=["make build"],
            log_parser=jest_log_parser,
        ),
        "16130": JavaScriptAdapter(
            version="20",
            test_cmd="yarn jest babel-helpers --verbose",
            install=["make bootstrap"],
            build=["make build"],
            log_parser=jest_log_parser,
        ),
    },
    "redis/redis": {
        "13115": CPlusPlusAdapter(
            install=["make distclean", "make"],
            build=["make"],
            test_cmd="TERM=dumb ./runtest --durable --single unit/scripting",
            log_parser=redis_log_parser,
        ),
        "12472": CPlusPlusAdapter(
            install=["make distclean", "make"],
            build=["make"],
            test_cmd='TERM=dumb ./runtest --durable --single unit/acl --only "/.*ACL GETUSER.*"',
            log_parser=redis_log_parser,
        ),
        "12272": CPlusPlusAdapter(
            install=["make distclean", "make"],
            build=["make"],
            test_cmd='TERM=dumb ./runtest --durable --single unit/type/string --only "/.*(GETRANGE|SETRANGE).*"',
            log_parser=redis_log_parser,
        ),
        "11734": CPlusPlusAdapter(
            install=["make distclean", "make"],
            build=["make"],
            test_cmd="TERM=dumb ./runtest --durable --single unit/bitops",
            log_parser=redis_log_parser,
        ),
        "10764": CPlusPlusAdapter(
            install=["make distclean", "make"],
            build=["make"],
            test_cmd='TERM=dumb ./runtest --durable --single unit/type/zset --only "BZMPOP"',
            log_parser=redis_log_parser,
        ),
    },
    "tokio-rs/tokio": {
        "6724": RustAdapter(
            version="1.81",
            # install only as much as needed to run the tests
            install=["cargo test --test io_write_all_buf --no-fail-fast --no-run"],
            # no build step, cargo test will build the relevant packages
            test_cmd="cargo test --test io_write_all_buf --no-fail-fast",
        ),
        "6838": RustAdapter(
            version="1.81",
            install=["cargo test --test uds_stream --no-fail-fast --no-run"],
            test_cmd="cargo test --test uds_stream --no-fail-fast",
        ),
        "6752": RustAdapter(
            version="1.81",
            install=["cargo test --test time_delay_queue --no-fail-fast --no-run"],
            test_cmd="cargo test --test time_delay_queue --no-fail-fast",
        ),
        "4867": RustAdapter(
            version="1.81",
            install=["cargo test --test sync_broadcast --no-fail-fast --no-run"],
            test_cmd="cargo test --test sync_broadcast --no-fail-fast",
        ),
        "4898": RustAdapter(
            version="1.81",
            install=[
                'RUSTFLAGS="--cfg tokio_unstable" cargo test --features full --test rt_metrics --no-run'
            ],
            test_cmd='RUSTFLAGS="--cfg tokio_unstable" cargo test --features full --test rt_metrics',
        ),
    },
    "hashicorp/terraform": {
        "35611": GoAdapter(
            version="1.23",
            install=["go mod tidy"],
            test_cmd='go test -v ./internal/terraform/... -run "^TestContext2Apply_provisioner"',
        ),
        "35543": GoAdapter(
            version="1.23",
            install=["go mod tidy"],
            test_cmd='go test -v ./internal/terraform/... -run "^TestContext2Plan_import"',
        ),
        "34900": GoAdapter(
            version="1.22",
            install=["go mod tidy"],
            test_cmd='go test -v ./internal/terraform/... -run "(^TestContext2Apply|^TestContext2Plan).*[Ss]ensitive"',
        ),
        "34580": GoAdapter(
            version="1.21",
            install=["go mod tidy"],
            test_cmd='go test -v ./internal/command/... -run "^TestFmt"',
        ),
        "34814": GoAdapter(
            version="1.22",
            install=["go mod tidy"],
            test_cmd="go test -v ./internal/builtin/provisioners/remote-exec/...",
        ),
    },
    "vuejs/core": {
        "11899": JavaScriptAdapter(
            version="20",
            test_cmd="pnpm run test packages/compiler-sfc/__tests__/compileStyle.spec.ts --no-watch --reporter=verbose",
            pre_install=["corepack enable pnpm"],
            install=["pnpm i"],
            build=["pnpm run build compiler-sfc"],
            log_parser=vitest_log_parser,
        ),
        "11870": JavaScriptAdapter(
            version="20",
            test_cmd="pnpm run test packages/runtime-core/__tests__/helpers/renderList.spec.ts --no-watch --reporter=verbose",
            pre_install=["corepack enable pnpm"],
            install=["pnpm i"],
            log_parser=vitest_log_parser,
        ),
        "11739": JavaScriptAdapter(
            version="20",
            test_cmd='pnpm run test packages/runtime-core/__tests__/hydration.spec.ts --no-watch --reporter=verbose -t "mismatch handling"',
            pre_install=["corepack enable pnpm"],
            install=["pnpm i"],
            log_parser=vitest_log_parser,
        ),
        "11915": JavaScriptAdapter(
            version="20",
            test_cmd='pnpm run test packages/compiler-core/__tests__/parse.spec.ts --no-watch --reporter=verbose -t "Element"',
            pre_install=["corepack enable pnpm"],
            install=["pnpm i"],
            log_parser=vitest_log_parser,
        ),
        "11589": JavaScriptAdapter(
            version="20",
            test_cmd="pnpm run test packages/runtime-core/__tests__/apiWatch.spec.ts --no-watch --reporter=verbose",
            pre_install=["corepack enable pnpm"],
            install=["pnpm i"],
            log_parser=vitest_log_parser,
        ),
    },
    "jqlang/jq": {
        **{
            k: CPlusPlusAdapter(
                build=[
                    "autoreconf -i",
                    "./configure --with-oniguruma=builtin",
                    "make clean",
                    "make -j8",
                ],
                test_cmd="make check",
                log_parser=jq_log_parser,
            )
            for k in ["2839", "2650", "2681", "2658", "2750"]
        }
    },
    "facebook/docusaurus": {
        "10309": JavaScriptAdapter(
            version="20",
            test_cmd="yarn test packages/docusaurus-plugin-content-docs/src/client/__tests__/docsClientUtils.test.ts --verbose",
            install=["yarn install"],
            log_parser=jest_log_parser,
        ),
        "10130": JavaScriptAdapter(
            version="20",
            test_cmd="yarn test packages/docusaurus/src/server/__tests__/brokenLinks.test.ts --verbose",
            install=["yarn install"],
            log_parser=jest_log_parser,
        ),
        "9897": JavaScriptAdapter(
            version="20",
            test_cmd="yarn test packages/docusaurus-utils/src/__tests__/markdownUtils.test.ts --verbose",
            install=["yarn install"],
            log_parser=jest_log_parser,
        ),
        "9183": JavaScriptAdapter(
            version="20",
            test_cmd="yarn test packages/docusaurus-theme-classic/src/__tests__/options.test.ts --verbose",
            install=["yarn install"],
            log_parser=jest_log_parser,
        ),
        "8927": JavaScriptAdapter(
            version="20",
            test_cmd="yarn test packages/docusaurus-utils/src/__tests__/markdownLinks.test.ts --verbose",
            install=["yarn install"],
            log_parser=jest_log_parser,
        ),
    },
}
