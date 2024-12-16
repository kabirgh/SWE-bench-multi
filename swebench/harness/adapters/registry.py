from swebench.harness.adapters.adapter import Adapter, tap_log_parser
from swebench.harness.adapters.cplusplus_adapter import (
    CPlusPlusAdapter,
    doctest_log_parser,
    jq_log_parser,
    micropython_test_log_parser,
    redis_log_parser,
    systemd_test_log_parser,
)
from swebench.harness.adapters.go_adapter import GoAdapter
from swebench.harness.adapters.java_adapter import (
    JavaAdapter,
    JavaMavenAdapter,
    ant_log_parser,
    gradle_custom_log_parser,
    make_lombok_pre_install_script,
    make_lucene_pre_install_script,
)
from swebench.harness.adapters.python_adapter import PythonAdapter
from swebench.harness.adapters.javascript_adapter import (
    JEST_JSON_JQ_TRANSFORM,
    JavaScriptAdapter,
    jest_json_log_parser,
    jest_log_parser,
    karma_log_parser,
    vitest_log_parser,
)
from swebench.harness.adapters.ruby_adapter import (
    RSPEC_JQ_TRANSFORM,
    RubyAdapter,
    cucumber_log_parser,
    minitest_log_parser,
    rspec_transformed_json_log_parser,
    ruby_unit_log_parser,
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
        "6370": GoAdapter(
            version="1.23",
            install=["go test -c ./cmd"],
            test=["go test -v ./cmd"],
        ),
        "6350": GoAdapter(
            version="1.23",
            install=['go test -c ./caddytest/integration -run "TestCaddyfileAdapt*"'],
            test=['go test -v ./caddytest/integration -run "TestCaddyfileAdapt*"'],
        ),
        "6288": GoAdapter(
            version="1.23",
            install=['go test -c ./caddytest/integration -run "TestCaddyfileAdapt*"'],
            test=['go test -v ./caddytest/integration -run "TestCaddyfileAdapt*"'],
        ),
        "5995": GoAdapter(
            version="1.23",
            install=['go test -c ./caddytest/integration -run "^TestUriReplace"'],
            test=['go test -v ./caddytest/integration -run "^TestUriReplace"'],
        ),
        "4943": GoAdapter(
            version="1.18",
            install=["go test -c ./modules/logging"],
            test=["go test -v ./modules/logging"],
        ),
        "5626": GoAdapter(
            version="1.19",
            install=['go test -c ./caddyconfig/httpcaddyfile -run "Test.*Import"'],
            test=['go test -v ./caddyconfig/httpcaddyfile -run "Test.*Import"'],
        ),
        "5761": GoAdapter(
            version="1.23",
            install=['go test -c ./caddyconfig/caddyfile -run "TestLexer.*"'],
            test=['go test -v ./caddyconfig/caddyfile -run "TestLexer.*"'],
        ),
        "5870": GoAdapter(
            version="1.23",
            install=['go test -c . -run "TestUnsyncedConfigAccess"'],
            test=['go test -v . -run "TestUnsyncedConfigAccess"'],
        ),
        "4774": GoAdapter(
            version="1.18",
            install=['go test -c ./caddytest/integration -run "TestCaddyfileAdapt*"'],
            test=['go test -v ./caddytest/integration -run "TestCaddyfileAdapt*"'],
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
            build=["make distclean", "make"],
            test=["TERM=dumb ./runtest --durable --single unit/scripting"],
            log_parser=redis_log_parser,
        ),
        "12472": CPlusPlusAdapter(
            build=["make distclean", "make"],
            test=[
                'TERM=dumb ./runtest --durable --single unit/acl --only "/.*ACL GETUSER.*"'
            ],
            log_parser=redis_log_parser,
        ),
        "12272": CPlusPlusAdapter(
            build=["make distclean", "make"],
            test=[
                'TERM=dumb ./runtest --durable --single unit/type/string --only "/.*(GETRANGE|SETRANGE).*"'
            ],
            log_parser=redis_log_parser,
        ),
        "11734": CPlusPlusAdapter(
            build=["make distclean", "make"],
            test=["TERM=dumb ./runtest --durable --single unit/bitops"],
            log_parser=redis_log_parser,
        ),
        "10764": CPlusPlusAdapter(
            build=["make distclean", "make"],
            test=[
                'TERM=dumb ./runtest --durable --single unit/type/zset --only "BZMPOP"'
            ],
            log_parser=redis_log_parser,
        ),
        "10095": CPlusPlusAdapter(
            build=["make distclean", "make"],
            test=[
                'TERM=dumb ./runtest --durable --single unit/type/list --only "/.*(LPOP|RPOP)"'
            ],
            log_parser=redis_log_parser,
        ),
        "9733": CPlusPlusAdapter(
            build=["make distclean", "make"],
            test=["TERM=dumb ./runtest --durable --single unit/introspection-2"],
            log_parser=redis_log_parser,
        ),
        "10068": CPlusPlusAdapter(
            build=["make distclean", "make"],
            test=[
                'TERM=dumb ./runtest --durable --single unit/type/stream --only "/*XTRIM*"'
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
        "6603": RustAdapter(
            version="1.81",
            install=["cargo test --test sync_mpsc --no-fail-fast --no-run"],
            test=["cargo test --test sync_mpsc --no-fail-fast"],
        ),
        "6551": RustAdapter(
            version="1.81",
            install=[
                'RUSTFLAGS="--cfg tokio_unstable" cargo test --features full --test rt_metrics --no-fail-fast --no-run'
            ],
            test=[
                'RUSTFLAGS="--cfg tokio_unstable" cargo test --features full --test rt_metrics --no-fail-fast'
            ],
        ),
        "4384": RustAdapter(
            version="1.81",
            test=[
                "RUSTFLAGS=-Awarnings cargo test --package tokio --test net_types_unwind --features full --no-fail-fast"
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
                    "make -j$(nproc)",
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
            install=["yarn install"],
            test=[
                "yarn test packages/docusaurus-plugin-content-docs/src/client/__tests__/docsClientUtils.test.ts --verbose"
            ],
            log_parser=jest_log_parser,
        ),
        "10130": JavaScriptAdapter(
            version="20",
            install=["yarn install"],
            test=[
                "yarn test packages/docusaurus/src/server/__tests__/brokenLinks.test.ts --verbose"
            ],
            log_parser=jest_log_parser,
        ),
        "9897": JavaScriptAdapter(
            version="20",
            install=["yarn install"],
            test=[
                "yarn test packages/docusaurus-utils/src/__tests__/markdownUtils.test.ts --verbose"
            ],
            log_parser=jest_log_parser,
        ),
        "9183": JavaScriptAdapter(
            version="20",
            install=["yarn install"],
            test=[
                "yarn test packages/docusaurus-theme-classic/src/__tests__/options.test.ts --verbose"
            ],
            log_parser=jest_log_parser,
        ),
        "8927": JavaScriptAdapter(
            version="20",
            install=["yarn install"],
            test=[
                "yarn test packages/docusaurus-utils/src/__tests__/markdownLinks.test.ts --verbose"
            ],
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
        "10720": GoAdapter(
            version="1.23",
            install=["go test -c ./promql"],
            test=['go test -v ./promql -run "^TestEvaluations"'],
        ),
        "10633": GoAdapter(
            version="1.23",
            install=["go test -c ./discovery/puppetdb"],
            test=[
                'go test -v ./discovery/puppetdb -run "TestPuppetDBRefreshWithParameters"'
            ],
        ),
        "9248": GoAdapter(
            version="1.23",
            install=["go test -c ./promql"],
            test=['go test -v ./promql -run "^TestEvaluations"'],
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
            test=[
                # FAIL_TO_PASS
                "mvnd test -B -T 1C -pl gson -Dtest=com.google.gson.functional.PrimitiveTest#testByteSerialization",
                "mvnd test -B -T 1C -pl gson -Dtest=com.google.gson.functional.PrimitiveTest#testShortSerialization",
                "mvnd test -B -T 1C -pl gson -Dtest=com.google.gson.functional.PrimitiveTest#testIntSerialization",
                "mvnd test -B -T 1C -pl gson -Dtest=com.google.gson.functional.PrimitiveTest#testLongSerialization",
                "mvnd test -B -T 1C -pl gson -Dtest=com.google.gson.functional.PrimitiveTest#testFloatSerialization",
                "mvnd test -B -T 1C -pl gson -Dtest=com.google.gson.functional.PrimitiveTest#testDoubleSerialization",
                # PASS_TO_PASS
                "mvnd test -B -T 1C -pl gson -Dtest=com.google.gson.functional.PrimitiveTest#testPrimitiveIntegerAutoboxedSerialization",
                "mvnd test -B -T 1C -pl gson -Dtest=com.google.gson.functional.PrimitiveTest#testPrimitiveIntegerAutoboxedInASingleElementArraySerialization",
                "mvnd test -B -T 1C -pl gson -Dtest=com.google.gson.functional.PrimitiveTest#testReallyLongValuesSerialization",
                "mvnd test -B -T 1C -pl gson -Dtest=com.google.gson.functional.PrimitiveTest#testPrimitiveLongAutoboxedSerialization",
            ],
        ),
        "2024": JavaMavenAdapter(
            version="11",
            test=[
                # FAIL_TO_PASS
                "mvnd test -B -T 1C -pl gson -Dtest=com.google.gson.functional.FieldNamingTest#testUpperCaseWithUnderscores",
                "mvnd test -B -T 1C -pl gson -Dtest=com.google.gson.functional.NamingPolicyTest#testGsonWithUpperCaseUnderscorePolicySerialization",
                "mvnd test -B -T 1C -pl gson -Dtest=com.google.gson.functional.NamingPolicyTest#testGsonWithUpperCaseUnderscorePolicyDeserialiation",
            ],
        ),
        "2479": JavaMavenAdapter(
            version="11",
            test=[
                # FAIL_TO_PASS
                "mvnd test -B -T 1C -pl gson -Dtest=com.google.gson.GsonBuilderTest#testRegisterTypeAdapterForObjectAndJsonElements",
                "mvnd test -B -T 1C -pl gson -Dtest=com.google.gson.GsonBuilderTest#testRegisterTypeHierarchyAdapterJsonElements",
                # PASS_TO_PASS
                "mvnd test -B -T 1C -pl gson -Dtest=com.google.gson.GsonBuilderTest#testModificationAfterCreate",
            ],
        ),
        "2134": JavaMavenAdapter(
            version="11",
            test=[
                # FAIL_TO_PASS
                "mvnd test -B -T 1C -pl gson -Dtest=com.google.gson.internal.bind.util.ISO8601UtilsTest#testDateParseInvalidDay",
                "mvnd test -B -T 1C -pl gson -Dtest=com.google.gson.internal.bind.util.ISO8601UtilsTest#testDateParseInvalidMonth",
                # PASS_TO_PASS
                "mvnd test -B -T 1C -pl gson -Dtest=com.google.gson.internal.bind.util.ISO8601UtilsTest#testDateParseWithDefaultTimezone",
            ],
        ),
        "2061": JavaMavenAdapter(
            version="11",
            test=[
                # FAIL_TO_PASS
                "mvnd test -B -T 1C -pl gson -Dtest=com.google.gson.stream.JsonReaderTest#testHasNextEndOfDocument",
                "mvnd test -B -T 1C -pl gson -Dtest=com.google.gson.internal.bind.JsonTreeReaderTest#testHasNext_endOfDocument",
                # PASS_TO_PASS
                "mvnd test -B -T 1C -pl gson -Dtest=com.google.gson.stream.JsonReaderTest#testReadEmptyObject",
                "mvnd test -B -T 1C -pl gson -Dtest=com.google.gson.stream.JsonReaderTest#testReadEmptyArray",
                "mvnd test -B -T 1C -pl gson -Dtest=com.google.gson.internal.bind.JsonTreeReaderTest#testSkipValue_emptyJsonObject",
                "mvnd test -B -T 1C -pl gson -Dtest=com.google.gson.internal.bind.JsonTreeReaderTest#testSkipValue_filledJsonObject",
            ],
        ),
        "2311": JavaMavenAdapter(
            version="11",
            test=[
                # FAIL_TO_PASS
                "mvnd test -B -T 1C -pl gson -Dtest=com.google.gson.JsonPrimitiveTest#testEqualsIntegerAndBigInteger",
                # PASS_TO_PASS
                "mvnd test -B -T 1C -pl gson -Dtest=com.google.gson.JsonPrimitiveTest#testLongEqualsBigInteger",
                "mvnd test -B -T 1C -pl gson -Dtest=com.google.gson.JsonPrimitiveTest#testEqualsAcrossTypes",
            ],
        ),
        "1100": JavaMavenAdapter(
            version="11",
            test=[
                # FAIL_TO_PASS
                "mvnd test -B -T 1C -pl gson -Dtest=com.google.gson.DefaultDateTypeAdapterTest#testNullValue",
                # PASS_TO_PASS
                "mvnd test -B -T 1C -pl gson -Dtest=com.google.gson.DefaultDateTypeAdapterTest#testDatePattern",
                "mvnd test -B -T 1C -pl gson -Dtest=com.google.gson.DefaultDateTypeAdapterTest#testInvalidDatePattern",
            ],
        ),
        "1093": JavaMavenAdapter(
            version="11",
            test=[
                # FAIL_TO_PASS
                "mvnd test -B -T 1C -pl gson -Dtest=com.google.gson.stream.JsonWriterTest#testNonFiniteDoublesWhenLenient",
                # PASS_TO_PASS
                "mvnd test -B -T 1C -pl gson -Dtest=com.google.gson.stream.JsonWriterTest#testNonFiniteBoxedDoublesWhenLenient",
                "mvnd test -B -T 1C -pl gson -Dtest=com.google.gson.stream.JsonWriterTest#testNonFiniteDoubles",
                "mvnd test -B -T 1C -pl gson -Dtest=com.google.gson.stream.JsonWriterTest#testNonFiniteBoxedDoubles",
                "mvnd test -B -T 1C -pl gson -Dtest=com.google.gson.stream.JsonWriterTest#testDoubles",
            ],
        ),
        "1014": JavaMavenAdapter(
            version="11",
            test=[
                # FAIL_TO_PASS
                "mvnd test -B -T 1C -pl gson -Dtest=com.google.gson.internal.bind.JsonTreeReaderTest#testSkipValue_emptyJsonObject",
                "mvnd test -B -T 1C -pl gson -Dtest=com.google.gson.internal.bind.JsonTreeReaderTest#testSkipValue_filledJsonObject",
            ],
        ),
    },
    "apache/druid": {
        "15402": JavaMavenAdapter(
            version="11",
            test=[
                # FAIL_TO_PASS
                "mvnd test -B -T 1C -pl processing -Dtest=org.apache.druid.query.groupby.GroupByQueryQueryToolChestTest#testCacheStrategy",
                # PASS_TO_PASS
                "mvnd test -B -T 1C -pl processing -Dtest=org.apache.druid.query.groupby.GroupByQueryQueryToolChestTest#testResultLevelCacheKeyWithSubTotalsSpec",
                "mvnd test -B -T 1C -pl processing -Dtest=org.apache.druid.query.groupby.GroupByQueryQueryToolChestTest#testMultiColumnCacheStrategy",
            ],
        ),
        "14092": JavaMavenAdapter(
            version="11",
            install=[
                "mvnd clean install -B -pl processing,cloud/aws-common,cloud/gcp-common -DskipTests -am",
            ],
            test=[
                # FAIL_TO_PASS
                "mvnd test -B -T 1C -pl server -Dtest=org.apache.druid.discovery.DruidLeaderClientTest#test503ResponseFromServerAndCacheRefresh",
                # PASS_TO_PASS
                "mvnd test -B -T 1C -pl server -Dtest=org.apache.druid.discovery.DruidLeaderClientTest#testServerFailureAndRedirect",
            ],
        ),
        "14136": JavaMavenAdapter(
            version="11",
            test=[
                # FAIL_TO_PASS
                "mvnd test -B -T 1C -pl processing -Dtest=org.apache.druid.timeline.VersionedIntervalTimelineTest#testOverlapSecondContainsFirstZeroLengthInterval",
                "mvnd test -B -T 1C -pl processing -Dtest=org.apache.druid.timeline.VersionedIntervalTimelineTest#testOverlapSecondContainsFirstZeroLengthInterval2",
                "mvnd test -B -T 1C -pl processing -Dtest=org.apache.druid.timeline.VersionedIntervalTimelineTest#testOverlapSecondContainsFirstZeroLengthInterval3",
                "mvnd test -B -T 1C -pl processing -Dtest=org.apache.druid.timeline.VersionedIntervalTimelineTest#testOverlapSecondContainsFirstZeroLengthInterval4",
                # PASS_TO_PASS
                "mvnd test -B -T 1C -pl processing -Dtest=org.apache.druid.timeline.VersionedIntervalTimelineTest#testOverlapFirstContainsSecond",
                "mvnd test -B -T 1C -pl processing -Dtest=org.apache.druid.timeline.VersionedIntervalTimelineTest#testOverlapSecondContainsFirst",
            ],
        ),
        "13704": JavaMavenAdapter(
            version="11",
            install=[
                # Update the pom.xml to use the correct version of the resource bundle. See https://github.com/apache/druid/pull/14054
                r"sed -i 's/<resourceBundle>org.apache.apache.resources:apache-jar-resource-bundle:1.5-SNAPSHOT<\/resourceBundle>/<resourceBundle>org.apache.apache.resources:apache-jar-resource-bundle:1.5<\/resourceBundle>/' pom.xml",
                "mvnd clean install -B -pl processing -DskipTests -am",
            ],
            test=[
                # FAIL_TO_PASS
                "mvnd test -B -pl processing -Dtest=org.apache.druid.query.aggregation.post.ArithmeticPostAggregatorTest#testPow",
                # PASS_TO_PASS
                "mvnd test -B -pl processing -Dtest=org.apache.druid.query.aggregation.post.ArithmeticPostAggregatorTest#testDiv",
                "mvnd test -B -pl processing -Dtest=org.apache.druid.query.aggregation.post.ArithmeticPostAggregatorTest#testQuotient",
            ],
        ),
        "16875": JavaMavenAdapter(
            version="11",
            install=[
                "mvnd clean install -B -pl server -DskipTests -am",
            ],
            test=[
                # FAIL_TO_PASS
                "mvnd test -B -pl server -Dtest=org.apache.druid.server.metrics.WorkerTaskCountStatsMonitorTest#testMonitorWithPeon",
                # PASS_TO_PASS
                "mvnd test -B -pl server -Dtest=org.apache.druid.server.metrics.WorkerTaskCountStatsMonitorTest#testMonitorWithNulls",
                "mvnd test -B -pl server -Dtest=org.apache.druid.server.metrics.WorkerTaskCountStatsMonitorTest#testMonitorIndexer",
            ],
        ),
    },
    "uutils/coreutils": {
        "6690": RustAdapter(
            version="1.81",
            install=[
                "cargo test --no-run -- test_cp_cp test_cp_same_file test_cp_multiple_files test_cp_single_file test_cp_no_file",
            ],
            test=[
                "cargo test --no-fail-fast -- test_cp_cp test_cp_same_file test_cp_multiple_files test_cp_single_file test_cp_no_file",
            ],
        ),
        "6731": RustAdapter(
            version="1.81",
            install=["cargo test backslash --no-run"],
            test=["cargo test backslash --no-fail-fast"],
        ),
        "6575": RustAdapter(
            version="1.81",
            install=["cargo test cksum --no-run"],
            test=["cargo test cksum --no-fail-fast"],
        ),
        "6682": RustAdapter(
            version="1.81",
            install=["cargo test mkdir --no-run"],
            test=["cargo test mkdir --no-fail-fast"],
        ),
        "6377": RustAdapter(
            version="1.81",
            install=["cargo test test_env --no-run"],
            test=["cargo test test_env --no-fail-fast"],
        ),
    },
    "nushell/nushell": {
        "13246": RustAdapter(
            version="1.77",
            install=["cargo test -p nu-command --no-run --test main find::"],
            build=["cargo build"],
            test=["cargo test -p nu-command --no-fail-fast --test main find::"],
        ),
        "12950": RustAdapter(
            version="1.77",
            install=["cargo test external_arguments --no-run"],
            test=["cargo test external_arguments --no-fail-fast"],
        ),
        "12901": RustAdapter(
            version="1.77",
            install=["cargo test --no-run shell::env"],
            test=["cargo test --no-fail-fast shell::env"],
        ),
        "13831": RustAdapter(
            version="1.79",
            install=["cargo test -p nu-command --no-run split_column"],
            build=["cargo build"],
            test=["cargo test -p nu-command --no-fail-fast split_column"],
        ),
        "13605": RustAdapter(
            version="1.78",
            install=["cargo test -p nu-command --no-run ls::"],
            build=["cargo build"],
            test=["cargo test -p nu-command --no-fail-fast ls::"],
        ),
    },
    "projectlombok/lombok": {
        "3602": JavaAdapter(
            version="11",
            pre_install=make_lombok_pre_install_script(
                ["lombok.bytecode.TestPostCompiler"]
            ),
            install=["ant deps"],
            test=["ant test.instance"],
            log_parser=ant_log_parser,
        ),
        **{
            k: JavaAdapter(
                version="11",
                pre_install=make_lombok_pre_install_script(
                    ["lombok.transform.TestWithDelombok"]
                ),
                install=["ant deps"],
                # Note: PASS_TO_PASS only contains the tests relevant to the
                # instance, not all tests that pass
                test=["ant test.instance"],
                log_parser=ant_log_parser,
            )
            for k in ["3312", "3697", "3326", "3674"]
        },
    },
    "apache/lucene": {
        "13494": JavaAdapter(
            version="21",
            pre_install=make_lucene_pre_install_script(),
            # No install script, download dependencies and compile in the test phase
            test=[
                "./gradlew test --tests org.apache.lucene.facet.TestStringValueFacetCounts",
            ],
            log_parser=gradle_custom_log_parser,
        ),
        "13704": JavaAdapter(
            version="21",
            pre_install=make_lucene_pre_install_script(),
            test=[
                "./gradlew test --tests org.apache.lucene.search.TestLatLonDocValuesQueries",
            ],
            log_parser=gradle_custom_log_parser,
        ),
        "13301": JavaAdapter(
            version="21",
            pre_install=make_lucene_pre_install_script(),
            test=[
                "./gradlew test --tests TestXYPoint.testEqualsAndHashCode -Dtests.seed=3ABEFE4D876DD310 -Dtests.nightly=true -Dtests.locale=es-419 -Dtests.timezone=Asia/Ulaanbaatar -Dtests.asserts=true -Dtests.file.encoding=UTF-8",
            ],
            log_parser=gradle_custom_log_parser,
        ),
        "12626": JavaAdapter(
            version="21",
            pre_install=make_lucene_pre_install_script(),
            test=["./gradlew test --tests org.apache.lucene.index.TestIndexWriter"],
            log_parser=gradle_custom_log_parser,
        ),
        "12212": JavaAdapter(
            version="17",
            pre_install=make_lucene_pre_install_script(),
            test=["./gradlew test --tests org.apache.lucene.facet.TestDrillSideways"],
            log_parser=gradle_custom_log_parser,
        ),
    },
    "nlohmann/json": {
        "4237": CPlusPlusAdapter(
            build=[
                "mkdir -p build",
                "cd build",
                "cmake ..",
                "make test-udt_cpp11",
                "cd ..",
            ],
            test=["./build/tests/test-udt_cpp11 -s -r=xml"],
            log_parser=doctest_log_parser,
        ),
    },
    "gohugoio/hugo": {
        "12768": GoAdapter(
            version="1.23",
            test=["go test -v ./markup/goldmark/blockquotes/..."],
        ),
        "12579": GoAdapter(
            version="1.23",
            test=['go test -v ./resources/page -run "^TestGroupBy"'],
        ),
        "12562": GoAdapter(
            version="1.23",
            test=['go test -v ./hugolib/... -run "^TestGetPage[^/]"'],
        ),
        "12448": GoAdapter(
            version="1.23",
            test=['go test -v ./hugolib/... -run "^TestRebuild"'],
        ),
        "12343": GoAdapter(
            version="1.23",
            test=['go test -v ./resources/page/... -run "^Test.*Permalink"'],
        ),
        "12204": GoAdapter(
            version="1.23",
            test=['go test -v ./tpl/tplimpl -run "^TestEmbedded"'],
        ),
        "12171": GoAdapter(
            version="1.23",
            test=['go test -v ./hugolib -run "^Test.*Pages"'],
        ),
    },
    "systemd/systemd": {
        "34480": CPlusPlusAdapter(
            build=[
                "meson setup build",
                "ninja -C build test-seccomp",
            ],
            test=["meson test -C build -v test-seccomp"],
            log_parser=systemd_test_log_parser,
        )
    },
    "micropython/micropython": {
        "15898": CPlusPlusAdapter(
            pre_install=["python -m venv .venv", "source .venv/bin/activate"],
            build=[
                "source ./tools/ci.sh",
                "ci_unix_build_helper VARIANT=standard",
                "gcc -shared -o tests/ports/unix/ffi_lib.so tests/ports/unix/ffi_lib.c",
            ],
            test=[
                "cd tests",
                "MICROPY_CPYTHON3=python3 MICROPY_MICROPYTHON=../ports/unix/build-standard/micropython ./run-tests.py -i string_format",
            ],
            log_parser=micropython_test_log_parser,
            clone_submodules=False,
        ),
        "13569": CPlusPlusAdapter(
            pre_install=["python -m venv .venv", "source .venv/bin/activate"],
            build=[
                "source ./tools/ci.sh",
                "ci_unix_build_helper VARIANT=standard",
                "gcc -shared -o tests/ports/unix/ffi_lib.so tests/ports/unix/ffi_lib.c",
            ],
            test=[
                "cd tests",
                "MICROPY_CPYTHON3=python3 MICROPY_MICROPYTHON=../ports/unix/build-standard/micropython ./run-tests.py -i try",
            ],
            log_parser=micropython_test_log_parser,
            clone_submodules=False,
        ),
        "13039": CPlusPlusAdapter(
            pre_install=["python -m venv .venv", "source .venv/bin/activate"],
            build=[
                "source ./tools/ci.sh",
                "ci_unix_build_helper VARIANT=standard",
                "gcc -shared -o tests/unix/ffi_lib.so tests/unix/ffi_lib.c",
            ],
            test=[
                "cd tests",
                "MICROPY_CPYTHON3=python3 MICROPY_MICROPYTHON=../ports/unix/build-standard/micropython ./run-tests.py -i slice",
            ],
            log_parser=micropython_test_log_parser,
            clone_submodules=False,
        ),
        "12158": CPlusPlusAdapter(
            pre_install=["python -m venv .venv", "source .venv/bin/activate"],
            build=[
                "source ./tools/ci.sh",
                "ci_unix_build_helper VARIANT=standard",
                "gcc -shared -o tests/unix/ffi_lib.so tests/unix/ffi_lib.c",
            ],
            test=[
                "cd tests",
                "MICROPY_CPYTHON3=python3 MICROPY_MICROPYTHON=../ports/unix/build-standard/micropython ./run-tests.py -d thread",
            ],
            log_parser=micropython_test_log_parser,
            clone_submodules=False,
        ),
        "10095": CPlusPlusAdapter(
            pre_install=[
                "python -m venv .venv",
                "source .venv/bin/activate",
                # https://github.com/micropython/micropython/issues/10951
                "sed -i 's/uint mp_import_stat/mp_import_stat_t mp_import_stat/' mpy-cross/main.c",
            ],
            build=["source ./tools/ci.sh", "ci_unix_build_helper VARIANT=standard"],
            test=[
                "cd tests",
                "MICROPY_CPYTHON3=python3 MICROPY_MICROPYTHON=../ports/unix/build-standard/micropython ./run-tests.py -i basics/fun",
            ],
            log_parser=micropython_test_log_parser,
            clone_submodules=False,
        ),
    },
    "gin-gonic/gin": {
        "4003": GoAdapter(
            version="1.23",
            install=["go test -c ."],
            test=['go test . -v -run "TestMethodNotAllowedNoRoute"'],
        ),
        "3820": GoAdapter(
            version="1.23",
            install=["go test -c ./binding"],
            test=['go test -v ./binding -run "^TestMapping"'],
        ),
        "3741": GoAdapter(
            version="1.23",
            install=["go test -c ."],
            test=['go test -v . -run "^TestColor"'],
        ),
        "2755": GoAdapter(
            version="1.23",
            install=["go test -c ."],
            test=['go test -v . -run "^TestTree"'],
        ),
        "3227": GoAdapter(
            version="1.23",
            install=["go test -c ."],
            test=['go test -v . -run "^TestRedirect"'],
        ),
        "2121": GoAdapter(
            version="1.23",
            install=["go test -c ./..."],
            test=['go test -v ./... -run "^Test.*Reader"'],
        ),
        "1957": GoAdapter(
            version="1.23",
            install=["go test -c ."],
            test=['go test -v . -run "^TestContext.*Bind"'],
        ),
        "1805": GoAdapter(
            version="1.23",
            install=["go test -c ."],
            test=['go test -v . -run "^Test.*Router"'],
        ),
    },
    "jekyll/jekyll": {
        "9141": RubyAdapter(
            version="3.3",
            install=["script/bootstrap"],
            test=['bundle exec ruby -I test test/test_site.rb -v -n "/static files/"'],
            log_parser=minitest_log_parser,
        ),
        "8761": RubyAdapter(
            version="3.3",
            install=["script/bootstrap"],
            test=[
                "bundle exec cucumber --publish-quiet --format progress --no-color features/post_data.feature:6 features/post_data.feature:30"
            ],
            log_parser=cucumber_log_parser,
        ),
        "8047": RubyAdapter(
            version="3.3",
            # Remove a gem that is causing installation to fail
            pre_install=[
                "sed -i '/^[[:space:]]*install_if.*mingw/,/^[[:space:]]*end/d' Gemfile"
            ],
            install=["script/bootstrap", "bundle add webrick"],
            test=[
                'bundle exec ruby -I test test/test_filters.rb -v -n "/where_exp filter/"'
            ],
            log_parser=minitest_log_parser,
        ),
        "8167": RubyAdapter(
            version="3.3",
            install=["script/bootstrap", "bundle add webrick"],
            test=[
                'bundle exec ruby -I test test/test_utils.rb -v -n "/Utils.slugify/"'
            ],
            log_parser=minitest_log_parser,
        ),
        "8771": RubyAdapter(
            version="3.3",
            install=["script/bootstrap"],
            test=[
                "bundle exec cucumber --publish-quiet --format progress --no-color features/incremental_rebuild.feature:27 features/incremental_rebuild.feature:70"
            ],
            log_parser=cucumber_log_parser,
        ),
    },
    "fluent/fluentd": {
        "4598": RubyAdapter(
            version="3.3",
            install=["bundle install"],
            test=[
                "bundle exec ruby test/plugin_helper/test_http_server_helper.rb -v -n '/mount/'"
            ],
            log_parser=ruby_unit_log_parser,
        ),
        "4311": RubyAdapter(
            version="3.3",
            install=["bundle install"],
            test=[
                "bundle exec ruby test/config/test_system_config.rb -v -n '/rotate_age/'"
            ],
            log_parser=ruby_unit_log_parser,
        ),
        "4655": RubyAdapter(
            version="3.3",
            install=["bundle install"],
            test=["bundle exec ruby test/plugin/test_in_http.rb -v -n '/test_add/'"],
            log_parser=ruby_unit_log_parser,
        ),
        "4030": RubyAdapter(
            version="3.3",
            install=["bundle install"],
            test=["bundle exec ruby test/plugin/out_forward/test_ack_handler.rb -v"],
            log_parser=ruby_unit_log_parser,
        ),
        "3917": RubyAdapter(
            version="3.3",
            install=["bundle install"],
            test=["bundle exec ruby test/test_config.rb -v"],
            log_parser=ruby_unit_log_parser,
        ),
        "3640": RubyAdapter(
            version="3.3",
            install=["bundle install"],
            test=[
                "bundle exec ruby test/plugin_helper/test_retry_state.rb -v -n '/exponential backoff/'"
            ],
            log_parser=ruby_unit_log_parser,
        ),
        "3641": RubyAdapter(
            version="3.3",
            install=["bundle install"],
            test=["bundle exec ruby test/test_supervisor.rb -v"],
            log_parser=ruby_unit_log_parser,
        ),
        "3616": RubyAdapter(
            version="3.3",
            install=["bundle install"],
            test=[
                "bundle exec ruby test/plugin/test_in_http.rb -v -n '/test_application/'"
            ],
            log_parser=ruby_unit_log_parser,
        ),
        "3631": RubyAdapter(
            version="3.3",
            install=["bundle install"],
            test=[
                "bundle exec ruby test/test_event_router.rb -v -n '/handle_emits_error/'"
            ],
            log_parser=ruby_unit_log_parser,
        ),
        "3466": RubyAdapter(
            version="3.3",
            install=["bundle install"],
            test=[
                "bundle exec ruby test/plugin/test_in_tail.rb -v -n '/test_should_replace_target_info/'"
            ],
            log_parser=ruby_unit_log_parser,
        ),
        "3328": RubyAdapter(
            version="3.3",
            install=["bundle install"],
            test=[
                "bundle exec ruby test/plugin/test_in_tail.rb -v -n '/test_ENOENT_error_after_setup_watcher/'"
            ],
            log_parser=ruby_unit_log_parser,
        ),
        "3608": RubyAdapter(
            version="3.3",
            install=["bundle install"],
            test=[
                "bundle exec ruby test/plugin/test_output_as_buffered_retries.rb -v -n '/retry_max_times/'"
            ],
            log_parser=ruby_unit_log_parser,
        ),
    },
    "fastlane/fastlane": {
        "21857": RubyAdapter(
            version="3.3",
            install=["bundle install --jobs=$(nproc)"],
            test=[
                f"FASTLANE_SKIP_UPDATE_CHECK=1 bundle exec rspec ./fastlane/spec/lane_manager_base_spec.rb --no-color --format json | {RSPEC_JQ_TRANSFORM}",
            ],
            log_parser=rspec_transformed_json_log_parser,
        ),
        "20958": RubyAdapter(
            version="3.3",
            install=["bundle install --jobs=$(nproc)"],
            test=[
                f"FASTLANE_SKIP_UPDATE_CHECK=1 bundle exec rspec ./fastlane/spec/actions_specs/import_from_git_spec.rb --no-color --format json | {RSPEC_JQ_TRANSFORM}",
            ],
            log_parser=rspec_transformed_json_log_parser,
        ),
        "20642": RubyAdapter(
            version="3.3",
            install=["bundle install --jobs=$(nproc)"],
            test=[
                f"FASTLANE_SKIP_UPDATE_CHECK=1 bundle exec rspec ./frameit/spec/device_spec.rb --no-color --format json | {RSPEC_JQ_TRANSFORM}",
            ],
            log_parser=rspec_transformed_json_log_parser,
        ),
        "19765": RubyAdapter(
            version="3.3",
            install=["bundle install --jobs=$(nproc)"],
            test=[
                f"FASTLANE_SKIP_UPDATE_CHECK=1 bundle exec rspec ./fastlane/spec/actions_specs/download_dsyms_spec.rb --no-color --format json | {RSPEC_JQ_TRANSFORM}",
            ],
            log_parser=rspec_transformed_json_log_parser,
        ),
        "20975": RubyAdapter(
            version="3.3",
            install=["bundle install --jobs=$(nproc)"],
            test=[
                f"FASTLANE_SKIP_UPDATE_CHECK=1 bundle exec rspec ./match/spec/storage/s3_storage_spec.rb --no-color --format json | {RSPEC_JQ_TRANSFORM}",
            ],
            log_parser=rspec_transformed_json_log_parser,
        ),
        "19304": RubyAdapter(
            version="3.3",
            install=["bundle install --jobs=$(nproc)"],
            test=[
                f"FASTLANE_SKIP_UPDATE_CHECK=1 bundle exec rspec ./fastlane/spec/actions_specs/zip_spec.rb --no-color --format json | {RSPEC_JQ_TRANSFORM}",
            ],
            log_parser=rspec_transformed_json_log_parser,
        ),
        "19207": RubyAdapter(
            version="3.3",
            install=["bundle install --jobs=$(nproc)"],
            test=[
                f"FASTLANE_SKIP_UPDATE_CHECK=1 bundle exec rspec ./fastlane/spec/actions_specs/zip_spec.rb --no-color --format json | {RSPEC_JQ_TRANSFORM}",
            ],
            log_parser=rspec_transformed_json_log_parser,
        ),
    },
    "tokio-rs/axum": {
        "2096": RustAdapter(
            version="1.81",
            test=[
                "RUSTFLAGS=-Awarnings cargo test --package axum --lib -- routing::tests::fallback"
            ],
        ),
    },
}
