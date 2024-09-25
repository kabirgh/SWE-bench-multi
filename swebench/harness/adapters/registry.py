from swebench.harness.adapters.adapter import Adapter, tap_log_parser
from swebench.harness.adapters.cplusplus_adapter import (
    CPlusPlusAdapter,
    jq_log_parser,
    redis_log_parser,
)
from swebench.harness.adapters.go_adapter import GoAdapter
from swebench.harness.adapters.java_adapter import JavaMavenAdapter
from swebench.harness.adapters.python_adapter import PythonAdapter
from swebench.harness.adapters.javascript_adapter import (
    JEST_JSON_JQ_TRANSFORM,
    JavaScriptAdapter,
    jest_json_log_parser,
    jest_log_parser,
    karma_log_parser,
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
                test=[TEST_PYTEST],
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
                test=[TEST_PYTEST],
                log_parser=MAP_REPO_TO_PARSER["scikit-learn/scikit-learn"],
            )
            for k in ["1.3", "1.4"]
        },
    },
    "caddyserver/caddy": {
        "6411": GoAdapter(
            version="1.23",
            install=["go mod tidy"],
            test=['go test -v . -run "TestReplacerNew*"'],
        ),
        "6345": GoAdapter(
            version="1.23",
            # compile the test binary, which downloads relevant packages. faster than go mod tidy
            install=["go test -c ./caddytest/integration"],
            test=["go test -v ./caddytest/integration"],
        ),
        "6115": GoAdapter(
            version="1.23",
            install=["go test -c ./modules/caddyhttp/reverseproxy"],
            test=["go test -v ./modules/caddyhttp/reverseproxy"],
        ),
        "6051": GoAdapter(
            version="1.23",
            install=["go test -c ./caddyconfig/caddyfile"],
            test=["go test -v ./caddyconfig/caddyfile"],
        ),
        "5404": GoAdapter(
            version="1.20",
            install=["go test -c ./caddyconfig/caddyfile"],
            test=["go test -v ./caddyconfig/caddyfile"],
        ),
    },
    "babel/babel": {
        "14532": JavaScriptAdapter(
            version="20",
            test=["yarn jest babel-generator --verbose"],
            install=["make bootstrap"],
            build=["make build"],
            log_parser=jest_log_parser,
        ),
        "13928": JavaScriptAdapter(
            version="20",
            test=['yarn jest babel-parser -t "arrow" --verbose'],
            install=["make bootstrap"],
            build=["make build"],
            log_parser=jest_log_parser,
        ),
        "15649": JavaScriptAdapter(
            version="20",
            test=["yarn jest packages/babel-traverse/test/scope.js --verbose"],
            install=["make bootstrap"],
            build=["make build"],
            log_parser=jest_log_parser,
        ),
        "15445": JavaScriptAdapter(
            version="20",
            test=[
                'yarn jest packages/babel-generator/test/index.js -t "generation " --verbose'
            ],
            install=["make bootstrap"],
            build=["make build"],
            log_parser=jest_log_parser,
        ),
        "16130": JavaScriptAdapter(
            version="20",
            test=["yarn jest babel-helpers --verbose"],
            install=["make bootstrap"],
            build=["make build"],
            log_parser=jest_log_parser,
        ),
    },
    "redis/redis": {
        "13115": CPlusPlusAdapter(
            install=["make distclean", "make"],
            build=["make"],
            test=["TERM=dumb ./runtest --durable --single unit/scripting"],
            log_parser=redis_log_parser,
        ),
        "12472": CPlusPlusAdapter(
            install=["make distclean", "make"],
            build=["make"],
            test=[
                'TERM=dumb ./runtest --durable --single unit/acl --only "/.*ACL GETUSER.*"'
            ],
            log_parser=redis_log_parser,
        ),
        "12272": CPlusPlusAdapter(
            install=["make distclean", "make"],
            build=["make"],
            test=[
                'TERM=dumb ./runtest --durable --single unit/type/string --only "/.*(GETRANGE|SETRANGE).*"'
            ],
            log_parser=redis_log_parser,
        ),
        "11734": CPlusPlusAdapter(
            install=["make distclean", "make"],
            build=["make"],
            test=["TERM=dumb ./runtest --durable --single unit/bitops"],
            log_parser=redis_log_parser,
        ),
        "10764": CPlusPlusAdapter(
            install=["make distclean", "make"],
            build=["make"],
            test=[
                'TERM=dumb ./runtest --durable --single unit/type/zset --only "BZMPOP"'
            ],
            log_parser=redis_log_parser,
        ),
    },
    "tokio-rs/tokio": {
        "6724": RustAdapter(
            version="1.81",
            # install only as much as needed to run the tests
            install=["cargo test --test io_write_all_buf --no-fail-fast --no-run"],
            # no build step, cargo test will build the relevant packages
            test=["cargo test --test io_write_all_buf --no-fail-fast"],
        ),
        "6838": RustAdapter(
            version="1.81",
            install=["cargo test --test uds_stream --no-fail-fast --no-run"],
            test=["cargo test --test uds_stream --no-fail-fast"],
        ),
        "6752": RustAdapter(
            version="1.81",
            install=["cargo test --test time_delay_queue --no-fail-fast --no-run"],
            test=["cargo test --test time_delay_queue --no-fail-fast"],
        ),
        "4867": RustAdapter(
            version="1.81",
            install=["cargo test --test sync_broadcast --no-fail-fast --no-run"],
            test=["cargo test --test sync_broadcast --no-fail-fast"],
        ),
        "4898": RustAdapter(
            version="1.81",
            install=[
                'RUSTFLAGS="--cfg tokio_unstable" cargo test --features full --test rt_metrics --no-run'
            ],
            test=[
                'RUSTFLAGS="--cfg tokio_unstable" cargo test --features full --test rt_metrics'
            ],
        ),
    },
    "hashicorp/terraform": {
        "35611": GoAdapter(
            version="1.23",
            install=["go test -c ./internal/terraform"],
            test=[
                'go test -v ./internal/terraform -run "^TestContext2Apply_provisioner"'
            ],
        ),
        "35543": GoAdapter(
            version="1.23",
            install=["go test -c ./internal/terraform"],
            test=['go test -v ./internal/terraform -run "^TestContext2Plan_import"'],
        ),
        "34900": GoAdapter(
            version="1.22",
            install=["go test -c ./internal/terraform"],
            test=[
                'go test -v ./internal/terraform -run "(^TestContext2Apply|^TestContext2Plan).*[Ss]ensitive"'
            ],
        ),
        "34580": GoAdapter(
            version="1.21",
            install=["go test -c ./internal/command"],
            test=['go test -v ./internal/command -run "^TestFmt"'],
        ),
        "34814": GoAdapter(
            version="1.22",
            install=["go test -c ./internal/builtin/provisioners/remote-exec"],
            test=["go test -v ./internal/builtin/provisioners/remote-exec"],
        ),
    },
    "vuejs/core": {
        "11899": JavaScriptAdapter(
            version="20",
            test=[
                "pnpm run test packages/compiler-sfc/__tests__/compileStyle.spec.ts --no-watch --reporter=verbose"
            ],
            pre_install=["corepack enable pnpm"],
            install=["pnpm i"],
            build=["pnpm run build compiler-sfc"],
            log_parser=vitest_log_parser,
        ),
        "11870": JavaScriptAdapter(
            version="20",
            test=[
                "pnpm run test packages/runtime-core/__tests__/helpers/renderList.spec.ts --no-watch --reporter=verbose"
            ],
            pre_install=["corepack enable pnpm"],
            install=["pnpm i"],
            log_parser=vitest_log_parser,
        ),
        "11739": JavaScriptAdapter(
            version="20",
            test=[
                'pnpm run test packages/runtime-core/__tests__/hydration.spec.ts --no-watch --reporter=verbose -t "mismatch handling"'
            ],
            pre_install=["corepack enable pnpm"],
            install=["pnpm i"],
            log_parser=vitest_log_parser,
        ),
        "11915": JavaScriptAdapter(
            version="20",
            test=[
                'pnpm run test packages/compiler-core/__tests__/parse.spec.ts --no-watch --reporter=verbose -t "Element"'
            ],
            pre_install=["corepack enable pnpm"],
            install=["pnpm i"],
            log_parser=vitest_log_parser,
        ),
        "11589": JavaScriptAdapter(
            version="20",
            test=[
                "pnpm run test packages/runtime-core/__tests__/apiWatch.spec.ts --no-watch --reporter=verbose"
            ],
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
                test=["make check"],
                log_parser=jq_log_parser,
            )
            for k in ["2839", "2650", "2235", "2658", "2750"]
        }
    },
    "facebook/docusaurus": {
        "10309": JavaScriptAdapter(
            version="20",
            test=[
                "yarn test packages/docusaurus-plugin-content-docs/src/client/__tests__/docsClientUtils.test.ts --verbose"
            ],
            install=["yarn install"],
            log_parser=jest_log_parser,
        ),
        "10130": JavaScriptAdapter(
            version="20",
            test=[
                "yarn test packages/docusaurus/src/server/__tests__/brokenLinks.test.ts --verbose"
            ],
            install=["yarn install"],
            log_parser=jest_log_parser,
        ),
        "9897": JavaScriptAdapter(
            version="20",
            test=[
                "yarn test packages/docusaurus-utils/src/__tests__/markdownUtils.test.ts --verbose"
            ],
            install=["yarn install"],
            log_parser=jest_log_parser,
        ),
        "9183": JavaScriptAdapter(
            version="20",
            test=[
                "yarn test packages/docusaurus-theme-classic/src/__tests__/options.test.ts --verbose"
            ],
            install=["yarn install"],
            log_parser=jest_log_parser,
        ),
        "8927": JavaScriptAdapter(
            version="20",
            test=[
                "yarn test packages/docusaurus-utils/src/__tests__/markdownLinks.test.ts --verbose"
            ],
            install=["yarn install"],
            log_parser=jest_log_parser,
        ),
    },
    "prometheus/prometheus": {
        "14861": GoAdapter(
            version="1.23",
            install=["go test -c ./promql"],
            test=['go test -v ./promql -run "^TestEngine"'],
        ),
        "13845": GoAdapter(
            version="1.23",
            install=["go test -c ./promql ./model/labels"],
            test=[
                'go test -v ./promql ./model/labels -run "^(TestRangeQuery|TestLabels)"'
            ],
        ),
        "14655": GoAdapter(
            version="1.23",
            install=["go test -c ./promql"],
            test=['go test -v ./promql -run "^TestEvaluations"'],
        ),
        "12874": GoAdapter(
            version="1.23",
            install=["go test -c ./tsdb"],
            test=['go test -v ./tsdb -run "^TestHead"'],
        ),
        "11859": GoAdapter(
            version="1.23",
            install=["go test -c ./tsdb"],
            test=['go test -v ./tsdb -run "^TestSnapshot"'],
        ),
    },
    "immutable-js/immutable-js": {
        "2006": JavaScriptAdapter(
            version="20",
            install=["npm install"],
            build=["npm run build"],
            test=["npx jest __tests__/Range.ts --verbose"],
            log_parser=jest_log_parser,
        ),
        "2005": JavaScriptAdapter(
            version="20",
            install=["npm install"],
            build=["npm run build"],
            test=[
                f"npx jest __tests__/OrderedMap.ts __tests__/OrderedSet.ts --silent --json | {JEST_JSON_JQ_TRANSFORM}"
            ],
            log_parser=jest_json_log_parser,
        ),
    },
    "mrdoob/three.js": {
        "27395": JavaScriptAdapter(
            version="20",
            # --ignore-scripts is used to avoid downloading chrome for puppeteer
            install=["npm install --ignore-scripts"],
            test=["npx qunit test/unit/src/math/Sphere.tests.js"],
            log_parser=tap_log_parser,
        ),
        "26589": JavaScriptAdapter(
            version="20",
            install=["npm install --ignore-scripts"],
            test=[
                "npx qunit test/unit/src/objects/Line.tests.js test/unit/src/objects/Mesh.tests.js test/unit/src/objects/Points.tests.js"
            ],
            log_parser=tap_log_parser,
        ),
        "25687": JavaScriptAdapter(
            version="20",
            install=["npm install --ignore-scripts"],
            test=[
                'npx qunit test/unit/src/core/Object3D.tests.js -f "/json|clone|copy/i"'
            ],
            log_parser=tap_log_parser,
        ),
    },
    "preactjs/preact": {
        "4152": JavaScriptAdapter(
            version="20",
            install=["npm install"],
            test=[
                'COVERAGE=false BABEL_NO_MODULES=true npx karma start karma.conf.js --single-run --grep="test/browser/components.test.js"'
            ],
            log_parser=karma_log_parser,
        ),
        "4316": JavaScriptAdapter(
            version="20",
            install=["npm install"],
            test=[
                'COVERAGE=false BABEL_NO_MODULES=true npx karma start karma.conf.js --single-run --grep="test/browser/events.test.js"'
            ],
            log_parser=karma_log_parser,
        ),
        "4245": JavaScriptAdapter(
            version="20",
            install=["npm install"],
            test=[
                'COVERAGE=false BABEL_NO_MODULES=true npx karma start karma.conf.js --single-run --grep="hooks/test/browser/useId.test.js"'
            ],
            log_parser=karma_log_parser,
        ),
        "4182": JavaScriptAdapter(
            version="20",
            install=["npm install"],
            test=[
                'COVERAGE=false BABEL_NO_MODULES=true npx karma start karma.conf.js --single-run --grep="hooks/test/browser/errorBoundary.test.js"'
            ],
            log_parser=karma_log_parser,
        ),
        "4436": JavaScriptAdapter(
            version="20",
            install=["npm install"],
            test=[
                'COVERAGE=false BABEL_NO_MODULES=true npx karma start karma.conf.js --single-run --grep="test/browser/refs.test.js"'
            ],
            log_parser=karma_log_parser,
        ),
    },
    "google/gson": {
        "2158": JavaMavenAdapter(
            version="11",
            # Download dependencies, compile test classes, and run test without printing to console (much)
            install=[
                "mvn test -B -pl gson -Dtest=com.google.gson.functional.PrimitiveTest -q"
            ],
            test=[
                # FAIL_TO_PASS
                "mvn test -B -pl gson -Dtest=com.google.gson.functional.PrimitiveTest#testByteSerialization",
                "mvn test -B -pl gson -Dtest=com.google.gson.functional.PrimitiveTest#testShortSerialization",
                "mvn test -B -pl gson -Dtest=com.google.gson.functional.PrimitiveTest#testIntSerialization",
                "mvn test -B -pl gson -Dtest=com.google.gson.functional.PrimitiveTest#testLongSerialization",
                "mvn test -B -pl gson -Dtest=com.google.gson.functional.PrimitiveTest#testFloatSerialization",
                "mvn test -B -pl gson -Dtest=com.google.gson.functional.PrimitiveTest#testDoubleSerialization",
                # PASS_TO_PASS
                "mvn test -B -pl gson -Dtest=com.google.gson.functional.PrimitiveTest#testPrimitiveIntegerAutoboxedSerialization",
                "mvn test -B -pl gson -Dtest=com.google.gson.functional.PrimitiveTest#testPrimitiveIntegerAutoboxedInASingleElementArraySerialization",
                "mvn test -B -pl gson -Dtest=com.google.gson.functional.PrimitiveTest#testReallyLongValuesSerialization",
                "mvn test -B -pl gson -Dtest=com.google.gson.functional.PrimitiveTest#testPrimitiveLongAutoboxedSerialization",
            ],
        ),
        "2024": JavaMavenAdapter(
            version="11",
            install=[
                "mvn test -B -pl gson -Dtest=com.google.gson.functional.FieldNamingTest,com.google.gson.functional.NamingPolicyTest -q",
            ],
            test=[
                # FAIL_TO_PASS
                "mvn test -B -pl gson -Dtest=com.google.gson.functional.FieldNamingTest#testUpperCaseWithUnderscores",
                "mvn test -B -pl gson -Dtest=com.google.gson.functional.NamingPolicyTest#testGsonWithUpperCaseUnderscorePolicySerialization",
                "mvn test -B -pl gson -Dtest=com.google.gson.functional.NamingPolicyTest#testGsonWithUpperCaseUnderscorePolicyDeserialiation",
            ],
        ),
        "2479": JavaMavenAdapter(
            version="11",
            install=[
                "mvn test -B -pl gson -Dtest=com.google.gson.GsonBuilderTest -q",
            ],
            test=[
                # FAIL_TO_PASS
                "mvn test -B -pl gson -Dtest=com.google.gson.GsonBuilderTest#testRegisterTypeAdapterForObjectAndJsonElements",
                "mvn test -B -pl gson -Dtest=com.google.gson.GsonBuilderTest#testRegisterTypeHierarchyAdapterJsonElements",
                # PASS_TO_PASS
                "mvn test -B -pl gson -Dtest=com.google.gson.GsonBuilderTest#testModificationAfterCreate",
            ],
        ),
        "2134": JavaMavenAdapter(
            version="11",
            install=[
                "mvn test -B -pl gson -Dtest=com.google.gson.internal.bind.util.ISO8601UtilsTest -q",
            ],
            test=[
                # FAIL_TO_PASS
                "mvn test -B -pl gson -Dtest=com.google.gson.internal.bind.util.ISO8601UtilsTest#testDateParseInvalidDay",
                "mvn test -B -pl gson -Dtest=com.google.gson.internal.bind.util.ISO8601UtilsTest#testDateParseInvalidMonth",
                # PASS_TO_PASS
                "mvn test -B -pl gson -Dtest=com.google.gson.internal.bind.util.ISO8601UtilsTest#testDateParseWithDefaultTimezone",
            ],
        ),
        "1495": JavaMavenAdapter(
            version="11",
            # Test file doesn't exist yet, so let the test command download and run dependencies
            install=[],
            test=[
                # FAIL_TO_PASS
                "mvn test -B -pl gson -Dtest=com.google.gson.functional.EnumWithObfuscatedTest",
            ],
        ),
    },
}
