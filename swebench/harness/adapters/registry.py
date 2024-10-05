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
from swebench.harness.adapters.rust_adapter import RustAdapter
from swebench.harness.constants import TEST_PYTEST
from swebench.harness.log_parsers import MAP_REPO_TO_PARSER

# List of common packages extracted from yarn.lock across all the docusaurus PRs in the registry.
# Removed platform-specific packages as well as others causing errors while building.
DOCUSAURUS_ENV_SCRIPT_LIST = [
    "yarn global add @algolia/events@4.0.1 @apideck/better-ajv-errors@0.3.6 @babel/plugin-syntax-async-generators@7.8.4 @babel/plugin-syntax-bigint@7.8.3 @babel/plugin-syntax-class-properties@7.12.13 @babel/plugin-syntax-class-static-block@7.14.5 @babel/plugin-syntax-dynamic-import@7.8.3 @babel/plugin-syntax-export-namespace-from@7.8.3 @babel/plugin-syntax-import-meta@7.10.4 @babel/plugin-syntax-json-strings@7.8.3 @babel/plugin-syntax-logical-assignment-operators@7.10.4 @babel/plugin-syntax-nullish-coalescing-operator@7.8.3 @babel/plugin-syntax-numeric-separator@7.10.4 @babel/plugin-syntax-object-rest-spread@7.8.3 @babel/plugin-syntax-optional-catch-binding@7.8.3 @babel/plugin-syntax-optional-chaining@7.8.3 @babel/plugin-syntax-private-property-in-object@7.14.5 @babel/plugin-syntax-top-level-await@7.14.5 @babel/regjsgen@0.8.0 @bcoe/v8-coverage@0.2.3 @colors/colors@1.5.0 @cspell/dict-csharp@4.0.2 @cspell/dict-en-common-misspellings@1.0.2 @cspell/dict-en-gb@1.1.33 @cspell/dict-gaming-terms@1.0.4 @cspell/dict-git@2.0.0 @cspell/dict-haskell@4.0.1 @cspell/dict-html-symbol-entities@4.0.0 @cspell/dict-r@2.0.1 @cspell/dict-rust@4.0.1 @cspell/dict-svelte@1.0.2 @cspell/dict-swift@2.0.1 @cspell/dict-vue@3.0.0 @discoveryjs/json-ext@0.5.7 @docusaurus/responsive-loader@1.7.0 @gar/promisify@1.1.3 @hapi/hoek@9.3.0 @hapi/topo@5.1.0 @humanwhocodes/module-importer@1.0.1 @humanwhocodes/object-schema@1.2.1 @hutson/parse-repository-url@3.0.2 @isaacs/string-locale-compare@1.1.0 @istanbuljs/load-nyc-config@1.1.0 @istanbuljs/schema@0.1.3 @jest/create-cache-key-function@27.5.1 @jest/types@27.5.1 @leichtgewicht/ip-codec@2.0.4 @nodelib/fs.scandir@2.1.5 @nodelib/fs.stat@2.0.5 @nodelib/fs.walk@1.2.8 @npmcli/fs@1.1.1 @npmcli/fs@2.1.2 @npmcli/move-file@1.1.2 @npmcli/move-file@2.0.1 @npmcli/node-gyp@2.0.0 @npmcli/promise-spawn@3.0.0 @npmcli/run-script@4.1.7 @octokit/openapi-types@12.11.0 @octokit/openapi-types@14.0.0 @octokit/plugin-enterprise-rest@6.0.1 @octokit/plugin-paginate-rest@3.1.0 @octokit/plugin-request-log@1.0.4 @octokit/plugin-rest-endpoint-methods@6.8.1 @octokit/request-error@3.0.3 @octokit/rest@19.0.3 @octokit/types@6.41.0 @octokit/types@8.2.1 @parcel/watcher@2.0.4 @philpl/buble@0.19.7 @pnpm/network.ca-file@1.0.2 @polka/url@1.0.0-next.21 @rollup/plugin-babel@5.3.1 @rollup/plugin-node-resolve@11.2.1 @rollup/plugin-replace@2.4.2 @rollup/pluginutils@3.1.0 @sideway/address@4.1.4 @sideway/formula@3.0.1 @sideway/pinpoint@2.0.0 @surma/rollup-plugin-off-main-thread@2.2.3 @swc/core@1.2.197 @szmarczak/http-timer@5.0.1 @testing-library/react-hooks@8.0.1 @tootallnate/once@1.1.2 @tootallnate/once@2.0.0 @trysound/sax@0.2.0 @types/acorn@4.0.6 @types/babel__generator@7.6.4 @types/babel__template@7.4.1 @types/body-parser@1.19.2 @types/bonjour@3.5.10 @types/buble@0.20.1 @types/clean-css@4.2.6 @types/color-name@1.1.1 @types/configstore@6.0.0 @types/connect@3.4.35 @types/dedent@0.7.0 @types/escape-html@1.0.2 @types/eslint-scope@3.7.4 @types/estree-jsx@1.0.0 @types/estree@0.0.39 @types/express@4.17.17 @types/file-loader@5.0.1 @types/fs-extra@9.0.13 @types/github-slugger@1.3.0 @types/graceful-fs@4.1.6 @types/gtag.js@0.0.12 @types/history@4.7.11 @types/html-minifier-terser@6.1.0 @types/html-minifier@4.0.2 @types/html-webpack-plugin@3.2.6 @types/http-cache-semantics@4.0.1 @types/istanbul-lib-coverage@2.0.4 @types/istanbul-lib-report@3.0.0 @types/istanbul-reports@3.0.1 @types/js-yaml@4.0.5 @types/jsdom@20.0.1 @types/json5@0.0.29 @types/micromatch@4.0.2 @types/mime@3.0.1 @types/minimatch@5.1.2 @types/minimatch@3.0.5 @types/minimist@1.2.2 @types/ms@0.7.31 @types/node@17.0.45 @types/normalize-package-data@2.4.1 @types/nprogress@0.2.0 @types/parse-json@4.0.0 @types/picomatch@2.3.0 @types/prismjs@1.26.0 @types/prop-types@15.7.5 @types/qs@6.9.7 @types/range-parser@1.2.4 @types/react-dev-utils@9.0.11 @types/react-router-dom@5.3.3 @types/react-router@5.1.20 @types/react-test-renderer@18.0.0 @types/relateurl@0.2.29 @types/resolve@1.17.1 @types/retry@0.12.0 @types/rtl-detect@1.0.0 @types/sax@1.2.4 @types/serve-handler@6.1.1 @types/serve-index@1.9.1 @types/sockjs@0.3.33 @types/source-list-map@0.1.2 @types/stack-utils@2.0.1 @types/stringify-object@3.3.1 @types/supports-color@8.1.1 @types/tapable@1.0.8 @types/tough-cookie@4.0.2 @types/trusted-types@2.0.3 @types/uglify-js@3.17.1 @types/webpack-bundle-analyzer@4.6.0 @types/webpack-dev-server@3.11.6 @types/webpack-sources@3.2.0 @types/webpack@4.41.33 @types/yargs-parser@21.0.0 @types/yargs@16.0.5 @xtuc/ieee754@1.2.0 @xtuc/long@4.2.2 @yarnpkg/lockfile@1.1.0 @zkochan/js-yaml@0.0.6 JSONStream@1.3.5 abab@2.0.6 abbrev@1.1.1 accepts@1.3.8 acorn-class-fields@0.2.1 acorn-dynamic-import@4.0.0 acorn-globals@7.0.1 acorn-jsx@5.3.2 acorn-walk@8.2.0 acorn@6.4.2 add-stream@1.0.0 address@1.2.2 agent-base@6.0.2 agentkeepalive@4.3.0 aggregate-error@3.1.0 ajv-formats@2.1.1 ajv-keywords@3.5.2 ajv-keywords@5.1.0 ajv@6.12.6 ajv@8.12.0 ansi-align@3.0.1 ansi-colors@4.1.3 ansi-escapes@4.3.2 ansi-html-community@0.0.8 ansi-regex@5.0.1 ansi-regex@6.0.1 ansi-styles@3.2.1 ansi-styles@4.3.0 ansi-styles@5.2.0 ansi-styles@6.2.1 any-promise@1.3.0 anymatch@3.1.3 aproba@2.0.0 are-we-there-yet@3.0.1 arg@5.0.2 argparse@1.0.10 argparse@2.0.1 array-differ@3.0.0 array-flatten@1.1.1 array-flatten@2.1.2 array-ify@1.0.0 array-includes@3.1.6 array-timsort@1.0.3 array-union@2.1.0 array.prototype.flat@1.3.1 array.prototype.flatmap@1.3.1 array.prototype.tosorted@1.1.1 arrify@1.0.1 arrify@2.0.1 ast-types-flow@0.0.7 astral-regex@2.0.0 async@3.2.4 asynckit@0.4.0 at-least-node@1.0.0 available-typed-arrays@1.0.5 babel-plugin-dynamic-import-node@2.3.3 babel-plugin-istanbul@6.1.1 babel-plugin-jest-hoist@29.5.0 babel-preset-current-node-syntax@1.0.1 babel-preset-jest@29.5.0 bail@2.0.2 balanced-match@1.0.2 balanced-match@2.0.0 base64-js@1.5.1 batch@0.6.1 before-after-hook@2.2.3 big-integer@1.6.51 big.js@5.2.2 binary-extensions@2.2.0 binary@0.3.0 bl@4.1.0 bluebird@3.4.7 boolbase@1.0.0 boxen@6.2.1 brace-expansion@1.1.11 brace-expansion@2.0.1 bser@2.1.1 buffer-crc32@0.2.13 buffer-from@1.1.2 buffer-indexof-polyfill@1.0.2 buffer@5.7.1 buffers@0.1.1 builtin-modules@3.3.0 builtins@1.0.3 builtins@5.0.1 byte-size@7.0.0 bytes@3.0.0 bytes@3.1.2 cacache@15.3.0 cacache@16.1.3 cacheable-lookup@7.0.0 call-bind@1.0.2 callsites@3.1.0 camel-case@4.1.2 camelcase-keys@6.2.2 camelcase@5.3.1 camelcase@6.3.0 camelcase@7.0.1 caniuse-api@3.0.0 ccount@2.0.1 chainsaw@0.1.0 chalk@4.1.0 chalk@5.2.0 chalk@2.4.2 chalk@4.1.2 char-regex@1.0.2 character-entities-html4@2.1.0 character-entities-legacy@3.0.0 character-entities@2.0.2 character-reference-invalid@2.0.1 chardet@0.7.0 cheerio-select@2.1.0 cheerio@1.0.0-rc.12 chokidar@3.5.3 chownr@1.1.4 chownr@2.0.0 chrome-trace-event@1.0.3 ci-info@2.0.0 ci-info@3.8.0 clean-css@5.3.2 clean-stack@2.2.0 clear-module@4.1.2 cli-boxes@3.0.0 cli-cursor@3.1.0 cli-highlight@2.1.11 cli-spinners@2.6.1 cli-table3@0.6.3 cli-truncate@2.1.0 cli-truncate@3.1.0 cli-width@3.0.0 cliui@7.0.4 cliui@8.0.1 clone-deep@4.0.1 clone@1.0.4 cmd-shim@5.0.0 co@4.6.0 color-convert@1.9.3 color-convert@2.0.1 color-name@1.1.3 color-name@1.1.4 color-string@1.9.1 color-support@1.1.3 color@4.2.3 colord@2.9.3 columnify@1.6.0 combine-promises@1.1.0 combined-stream@1.0.8 comma-separated-tokens@2.0.3 command-exists-promise@2.0.2 commander@7.2.0 commander@2.20.3 commander@5.1.0 commander@8.3.0 comment-json@4.2.3 comment-parser@1.3.1 common-ancestor-path@1.0.1 common-tags@1.8.2 compare-func@2.0.0 compressible@2.0.18 compression@1.7.4 concat-map@0.0.1 concat-stream@2.0.0 config-chain@1.1.12 config-chain@1.1.13 configstore@6.0.0 confusing-browser-globals@1.0.11 connect-history-api-fallback@2.0.0 consola@2.15.3 console-control-strings@1.1.0 consolidated-events@2.0.2 content-disposition@0.5.2 content-disposition@0.5.4 content-type@1.0.5 conventional-changelog-angular@5.0.12 conventional-changelog-core@4.2.4 conventional-changelog-preset-loader@2.3.4 conventional-changelog-writer@5.0.1 conventional-commits-filter@2.0.7 conventional-commits-parser@3.2.4 conventional-recommended-bump@6.1.0 convert-source-map@1.9.0 convert-source-map@2.0.0 cookie-signature@1.0.6 copy-webpack-plugin@11.0.0 core-util-is@1.0.3 cose-base@1.0.3 cose-base@2.2.0 cosmiconfig@7.0.0 cosmiconfig@6.0.0 cosmiconfig@7.1.0 cross-env@7.0.3 cross-spawn@6.0.5 cross-spawn@7.0.3 crypto-random-string@2.0.0 crypto-random-string@4.0.0 css-what@6.1.0 cssesc@3.0.0 cssom@0.5.0 cssom@0.3.8 cssstyle@2.3.0 cytoscape-cose-bilkent@4.1.0 cytoscape-fcose@2.2.0 d3-axis@3.0.0 d3-brush@3.0.0 d3-chord@3.0.1 d3-color@3.1.0 d3-contour@4.0.2 d3-dispatch@3.0.1 d3-drag@3.0.0 d3-dsv@3.0.1 d3-ease@3.0.1 d3-fetch@3.0.1 d3-force@3.0.0 d3-format@3.1.0 d3-geo@3.1.0 d3-hierarchy@3.1.2 d3-interpolate@3.0.1 d3-path@3.1.0 d3-polygon@3.0.1 d3-quadtree@3.0.1 d3-random@3.0.1 d3-scale-chromatic@3.0.0 d3-scale@4.0.2 d3-selection@3.0.0 d3-shape@3.2.0 d3-time-format@4.1.0 d3-time@3.1.0 d3-timer@3.0.1 d3-transition@3.0.1 d3-zoom@3.0.0 damerau-levenshtein@1.0.8 dargs@7.0.0 data-urls@3.0.2 dateformat@3.0.3 debug@2.6.9 debug@4.3.4 debug@3.2.7 decamelize-keys@1.1.1 decamelize@1.2.0 decimal.js@10.4.3 decode-named-character-reference@1.0.2 decompress-response@6.0.0 dedent@0.7.0 deep-extend@0.6.0 deep-freeze@0.0.1 deep-is@0.1.4 deepmerge@2.2.1 default-gateway@6.0.3 defaults@1.0.4 defer-to-connect@2.0.1 define-lazy-prop@2.0.0 define-properties@1.2.0 del@6.1.1 delaunator@5.0.0 delayed-stream@1.0.0 delegates@1.0.0 depd@2.0.0 depd@1.1.2 deprecation@2.3.1 dequal@2.0.3 destroy@1.2.0 detect-indent@5.0.0 detect-newline@3.1.0 detect-node@2.1.0 detect-port-alt@1.1.6 detect-port@1.5.1 diff-sequences@29.4.3 diff@5.1.0 dir-glob@3.0.1 dns-equal@1.0.0 doctrine@2.1.0 doctrine@3.0.0 dom-converter@0.2.0 dom-serializer@1.4.1 dom-serializer@2.0.0 domelementtype@2.3.0 domexception@4.0.0 domhandler@4.3.1 domhandler@5.0.3 dot-case@3.0.4 dot-prop@6.0.1 dot-prop@5.3.0 dotenv@10.0.0 duplexer2@0.1.4 duplexer@0.1.2 eastasianwidth@0.2.0 ee-first@1.1.1 elkjs@0.8.2 emittery@0.13.1 emoji-regex@8.0.0 emoji-regex@9.2.2 emojis-list@3.0.0 encodeurl@1.0.2 encoding@0.1.13 end-of-stream@1.4.4 enquirer@2.3.6 entities@2.2.0 env-paths@2.2.1 equals@1.0.5 err-code@2.0.3 error-ex@1.3.2 es-set-tostringtag@2.0.1 es-shim-unscopables@1.0.0 es-to-primitive@1.2.1 escalade@3.1.1 escape-goat@4.0.0 escape-html@1.0.3 escape-string-regexp@1.0.5 escape-string-regexp@2.0.0 escape-string-regexp@4.0.0 escape-string-regexp@5.0.0 eslint-config-airbnb-base@15.0.0 eslint-config-airbnb@19.0.4 eslint-import-resolver-node@0.3.7 eslint-plugin-header@3.1.1 eslint-plugin-import@2.27.5 eslint-plugin-jsx-a11y@6.7.1 eslint-plugin-react-hooks@4.6.0 eslint-plugin-react@7.32.2 eslint-scope@5.1.1 eslint-utils@3.0.0 eslint-visitor-keys@2.1.0 esprima@4.0.1 esquery@1.5.0 esrecurse@4.3.0 estraverse@4.3.0 estraverse@5.3.0 estree-walker@1.0.1 estree-walker@3.0.3 esutils@2.0.3 etag@1.8.1 eval@0.1.8 eventemitter3@4.0.7 events@3.3.0 execa@5.0.0 execa@5.1.1 exit@0.1.2 expand-template@2.0.3 extend-shallow@2.0.1 extend@3.0.2 external-editor@3.1.0 fast-deep-equal@3.1.3 fast-folder-size@1.6.1 fast-glob@3.2.7 fast-json-stable-stringify@2.1.0 fast-levenshtein@2.0.6 fast-url-parser@1.1.3 fastest-levenshtein@1.0.16 fastq@1.15.0 faye-websocket@0.11.4 fb-watchman@2.0.2 fd-slicer@1.1.0 feed@4.2.2 figures@3.2.0 file-entry-cache@6.0.1 file-loader@6.2.0 filelist@1.0.4 filesize@8.0.7 finalhandler@1.2.0 find-up@5.0.0 find-up@2.1.0 find-up@3.0.0 find-up@4.1.0 flat@5.0.2 for-each@0.3.3 fork-ts-checker-webpack-plugin@6.5.3 form-data-encoder@2.1.4 form-data@4.0.0 forwarded@0.2.0 fresh@0.5.2 fs-constants@1.0.0 fs-extra@9.1.0 fs-minipass@1.2.7 fs-minipass@2.1.0 fs.realpath@1.0.0 fstream@1.0.12 function-bind@1.1.1 function.prototype.name@1.1.5 functions-have-names@1.2.3 gauge@4.0.4 gensync@1.0.0-beta.2 get-caller-file@2.0.5 get-own-enumerable-property-symbols@3.0.2 get-package-type@0.1.0 get-pkg-repo@4.2.1 get-port@5.1.1 get-stream@6.0.0 get-stream@6.0.1 get-symbol-description@1.0.0 git-raw-commits@2.0.11 git-remote-origin-url@2.0.0 git-semver-tags@4.1.1 git-up@7.0.0 git-url-parse@13.1.0 gitconfiglocal@1.0.0 github-from-package@0.0.0 github-slugger@1.5.0 glob-parent@5.1.2 glob-parent@6.0.2 glob-to-regexp@0.4.1 glob@7.1.4 glob@7.2.3 glob@8.1.0 global-dirs@3.0.1 global-modules@2.0.0 global-prefix@3.0.0 globals@11.12.0 globals@13.20.0 globalthis@1.0.3 globby@11.1.0 globjoin@0.1.4 gopd@1.0.1 graceful-fs@4.2.10 grapheme-splitter@1.0.4 gray-matter@4.0.3 gzip-size@6.0.0 handle-thing@2.0.1 handlebars@4.7.7 hard-rejection@2.1.0 has-bigints@1.0.2 has-flag@3.0.0 has-flag@4.0.0 has-own-prop@2.0.0 has-property-descriptors@1.0.0 has-proto@1.0.1 has-symbols@1.0.3 has-tostringtag@1.0.0 has-unicode@2.0.1 has-yarn@3.0.0 has@1.0.3 he@1.2.0 heap@0.2.7 highlight.js@10.7.3 history@4.10.1 hoist-non-react-statics@3.3.2 hosted-git-info@2.8.9 hosted-git-info@3.0.8 hosted-git-info@4.1.0 hosted-git-info@5.2.1 hpack.js@2.1.6 html-encoding-sniffer@3.0.0 html-escaper@2.0.2 html-minifier-terser@6.1.0 htmlparser2@6.1.0 http-cache-semantics@4.1.1 http-deceiver@1.2.7 http-errors@2.0.0 http-errors@1.6.3 http-parser-js@0.5.8 http-proxy-agent@4.0.1 http-proxy-agent@5.0.0 http-proxy-middleware@1.3.1 http-proxy-middleware@2.0.6 http-proxy@1.18.1 http2-wrapper@2.2.0 https-proxy-agent@5.0.1 human-signals@2.1.0 humanize-ms@1.2.1 husky@8.0.3 iconv-lite@0.4.24 iconv-lite@0.6.3 icss-utils@5.1.0 idb@7.1.1 ieee754@1.2.1 ignore-walk@5.0.1 ignore@5.2.4 image-size@1.0.2 import-fresh@3.3.0 import-lazy@4.0.0 import-local@3.1.0 imurmurhash@0.1.4 indent-string@4.0.0 infer-owner@1.0.4 infima@0.2.0-alpha.43 inflight@1.0.6 inherits@2.0.4 inherits@2.0.3 ini@2.0.0 ini@1.3.8 init-package-json@3.0.2 inline-style-parser@0.1.1 inquirer@8.2.5 internal-slot@1.0.5 internmap@2.0.3 interpret@1.4.0 invariant@2.2.4 ipaddr.js@1.9.1 is-alphabetical@2.0.1 is-alphanumerical@2.0.1 is-array-buffer@3.0.2 is-arrayish@0.2.1 is-arrayish@0.3.2 is-bigint@1.0.4 is-binary-path@2.1.0 is-boolean-object@1.1.2 is-buffer@2.0.5 is-callable@1.2.7 is-ci@2.0.0 is-ci@3.0.1 is-date-object@1.0.5 is-decimal@2.0.1 is-docker@2.2.1 is-extendable@0.1.1 is-extglob@2.1.1 is-fullwidth-code-point@3.0.0 is-fullwidth-code-point@4.0.0 is-generator-fn@2.1.0 is-glob@4.0.3 is-hexadecimal@2.0.1 is-installed-globally@0.4.0 is-interactive@1.0.0 is-lambda@1.0.1 is-module@1.0.0 is-negative-zero@2.0.2 is-npm@6.0.0 is-number-object@1.0.7 is-number@7.0.0 is-obj@1.0.1 is-obj@2.0.0 is-path-cwd@2.2.0 is-path-inside@3.0.3 is-plain-obj@1.1.0 is-plain-obj@3.0.0 is-plain-obj@4.1.0 is-plain-object@2.0.4 is-plain-object@5.0.0 is-potential-custom-element-name@1.0.1 is-promise@4.0.0 is-reference@3.0.1 is-regex@1.1.4 is-regexp@1.0.0 is-root@2.1.0 is-shared-array-buffer@1.0.2 is-ssh@1.4.0 is-stream@2.0.0 is-stream@2.0.1 is-stream@3.0.0 is-string@1.0.7 is-symbol@1.0.4 is-text-path@1.0.1 is-typed-array@1.1.10 is-typedarray@1.0.0 is-unicode-supported@0.1.0 is-weakref@1.0.2 is-wsl@2.2.0 is-yarn-global@0.4.1 isarray@0.0.1 isarray@2.0.5 isarray@1.0.0 isexe@2.0.0 isobject@3.0.1 istanbul-lib-coverage@3.2.0 istanbul-lib-instrument@5.2.1 istanbul-lib-report@3.0.0 istanbul-lib-source-maps@4.0.1 istanbul-reports@3.1.5 jest-changed-files@29.5.0 jest-docblock@29.4.3 jest-get-type@29.4.3 jest-pnp-resolver@1.2.3 jest-regex-util@29.4.3 jest-serializer-ansi-escapes@2.0.1 jest-serializer-react-helmet-async@1.0.21 jest-worker@26.6.2 jest-worker@27.5.1 jkroso-type@1.1.1 js-tokens@4.0.0 js-yaml@4.1.0 js-yaml@3.14.1 jsdoctypeparser@9.0.0 jsdom@20.0.3 jsesc@2.5.2 jsesc@0.5.0 json-buffer@3.0.1 json-parse-better-errors@1.0.2 json-parse-even-better-errors@2.3.1 json-schema-traverse@0.4.1 json-schema-traverse@1.0.0 json-schema@0.4.0 json-stable-stringify-without-jsonify@1.0.1 json-stringify-nice@1.1.4 json-stringify-safe@5.0.1 json5@1.0.2 json5@2.2.3 jsonc-parser@3.2.0 jsonfile@6.1.0 jsonparse@1.3.1 jsonpointer@5.0.1 just-diff-apply@5.5.0 khroma@2.0.0 kind-of@6.0.3 kleur@3.0.3 kleur@4.1.5 known-css-properties@0.26.0 language-subtag-registry@0.3.22 language-tags@1.0.5 latest-version@7.0.0 layout-base@1.0.2 layout-base@2.0.1 lerna-changelog@2.2.0 leven@3.1.0 levn@0.4.1 lilconfig@2.1.0 lines-and-columns@1.2.4 lines-and-columns@2.0.3 listenercount@1.0.1 load-json-file@6.2.0 load-json-file@4.0.0 loader-runner@4.3.0 loader-utils@2.0.4 loader-utils@3.2.1 lodash-es@4.17.21 lodash.debounce@4.0.8 lodash.ismatch@4.4.0 lodash.memoize@4.1.2 lodash.merge@4.6.2 lodash.sortby@4.7.0 lodash.truncate@4.4.2 lodash.uniq@4.5.0 lodash@4.17.21 log-symbols@4.1.0 log-update@4.0.0 longest-streak@3.1.0 loose-envify@1.4.0 lower-case@2.0.2 lowercase-keys@3.0.0 lru-cache@5.1.1 lru-cache@6.0.0 lru-cache@7.18.3 magic-string@0.25.9 make-dir@3.1.0 make-dir@2.1.0 make-fetch-happen@10.2.1 make-fetch-happen@9.1.0 makeerror@1.0.12 map-obj@1.0.1 map-obj@4.3.0 markdown-table@3.0.3 mathml-tag-names@2.1.3 media-typer@0.3.0 memorystream@0.3.1 meow@8.1.2 meow@9.0.0 merge-descriptors@1.0.1 merge-stream@2.0.0 merge2@1.4.1 methods@1.1.2 micromatch@4.0.5 mime-db@1.52.0 mime-db@1.33.0 mime-types@2.1.18 mime-types@2.1.35 mime@1.6.0 mimic-fn@2.1.0 mimic-fn@4.0.0 mimic-response@3.1.0 mimic-response@4.0.0 min-indent@1.0.1 minimalistic-assert@1.0.1 minimatch@3.0.5 minimatch@3.1.2 minimatch@5.1.6 minimist-options@4.1.0 minimist@1.2.8 minipass-collect@1.0.2 minipass-fetch@1.4.1 minipass-fetch@2.1.2 minipass-flush@1.0.5 minipass-json-stream@1.0.1 minipass-pipeline@1.2.4 minipass-sized@1.0.3 minipass@2.9.0 minipass@3.3.6 minizlib@1.3.3 minizlib@2.1.2 mkdirp-classic@0.5.3 mkdirp-infer-owner@2.0.0 mkdirp@0.5.6 mkdirp@1.0.4 modify-values@1.0.1 mri@1.2.0 mrmime@1.0.1 ms@2.0.0 ms@2.1.2 ms@2.1.3 multicast-dns@7.2.5 multimatch@5.0.0 mute-stream@0.0.8 mz@2.7.0 napi-build-utils@1.0.2 natural-compare-lite@1.4.0 natural-compare@1.4.0 negotiator@0.6.3 neo-async@2.6.2 netlify-plugin-cache@1.0.3 nice-try@1.0.5 no-case@3.0.4 node-addon-api@3.2.1 node-fetch@2.6.7 node-forge@1.3.1 node-gyp-build@4.6.0 node-int64@0.4.0 non-layered-tidy-tree-layout@2.0.2 nopt@6.0.0 normalize-package-data@2.5.0 normalize-package-data@3.0.3 normalize-package-data@4.0.1 normalize-path@3.0.0 normalize-range@0.1.2 normalize-url@8.0.0 npm-bundled@1.1.2 npm-normalize-package-bin@1.0.1 npm-normalize-package-bin@2.0.0 npm-package-arg@8.1.1 npm-package-arg@9.1.2 npm-packlist@5.1.1 npm-registry-fetch@13.3.1 npm-run-all@4.1.5 npm-run-path@4.0.1 npm-run-path@5.1.0 npmlog@6.0.2 nprogress@0.2.0 nth-check@2.1.1 object-assign@4.1.1 object-inspect@1.12.3 object-keys@1.1.1 object.assign@4.1.4 object.entries@1.1.6 object.fromentries@2.0.6 object.hasown@1.1.2 object.values@1.1.6 obuf@1.1.2 on-finished@2.4.1 on-headers@1.0.2 once@1.4.0 onetime@5.1.2 onetime@6.0.0 open@8.4.2 opener@1.5.2 ora@5.4.1 os-homedir@1.0.2 os-tmpdir@1.0.2 p-cancelable@3.0.0 p-finally@1.0.0 p-limit@1.3.0 p-limit@2.3.0 p-limit@3.1.0 p-locate@2.0.0 p-locate@3.0.0 p-locate@4.1.0 p-locate@5.0.0 p-map-series@2.1.0 p-map@4.0.0 p-map@3.0.0 p-pipe@3.1.0 p-queue@6.6.2 p-reduce@2.1.0 p-retry@4.6.2 p-timeout@3.2.0 p-try@1.0.0 p-try@2.2.0 p-waterfall@2.1.1 param-case@3.0.4 parent-module@1.0.1 parent-module@2.0.0 parse-entities@4.0.1 parse-json@4.0.0 parse-json@5.2.0 parse-numeric-range@1.3.0 parse-path@7.0.0 parse-url@8.1.0 parse5-htmlparser2-tree-adapter@6.0.1 parse5-htmlparser2-tree-adapter@7.0.0 parse5@5.1.1 parse5@6.0.1 parse5@7.1.2 parseurl@1.3.3 pascal-case@3.1.2 path-exists@3.0.0 path-exists@4.0.0 path-is-absolute@1.0.1 path-is-inside@1.0.2 path-key@2.0.1 path-key@3.1.1 path-key@4.0.0 path-parse@1.0.7 path-to-regexp@0.1.7 path-to-regexp@2.2.1 path-to-regexp@1.8.0 path-type@3.0.0 path-type@4.0.0 pend@1.2.0 periscopic@3.1.0 picocolors@1.0.0 picomatch@2.3.1 pidtree@0.3.1 pidtree@0.6.0 pify@5.0.0 pify@2.3.0 pify@3.0.0 pify@4.0.1 pkg-dir@4.2.0 pkg-up@3.1.0 postcss-media-query-parser@0.2.3 postcss-modules-extract-imports@3.0.0 postcss-modules-scope@3.0.0 postcss-modules-values@4.0.0 postcss-resolve-nested-selector@0.1.1 postcss-safe-parser@6.0.0 postcss-value-parser@4.2.0 prebuild-install@7.1.1 prelude-ls@1.2.1 pretty-bytes@5.6.0 pretty-error@4.0.0 pretty-time@1.1.0 prismjs@1.29.0 proc-log@2.0.1 process-nextick-args@2.0.1 progress@2.0.3 promise-all-reject-late@1.0.1 promise-inflight@1.0.1 promise-retry@2.0.1 prompts@2.4.2 promzard@0.3.0 prop-types@15.8.1 property-information@6.2.0 proto-list@1.2.4 protocols@2.0.1 proxy-addr@2.0.7 proxy-from-env@1.1.0 psl@1.9.0 pump@3.0.0 punycode@1.4.1 punycode@2.3.0 pupa@3.1.0 pure-react-carousel@1.30.1 q@1.5.1 qs@6.11.0 querystringify@2.2.0 queue-microtask@1.2.3 queue@6.0.2 quick-lru@4.0.1 quick-lru@5.1.1 randombytes@2.1.0 range-parser@1.2.0 range-parser@1.2.1 raw-loader@4.0.2 rc@1.2.8 react-dev-utils@12.0.1 react-error-boundary@3.1.4 react-error-overlay@6.0.11 react-helmet-async@1.3.0 react-is@16.13.1 react-lite-youtube-embed@2.3.52 react-loadable-ssr-addon-v5-slorber@1.0.1 react-router-config@5.1.1 react-router-dom@5.3.4 react-router@5.3.4 react-shallow-renderer@16.15.0 react-waypoint@10.3.0 read-cmd-shim@3.0.0 read-package-json-fast@2.0.3 read-package-json@5.0.1 read-package-json@5.0.2 read-pkg-up@3.0.0 read-pkg-up@7.0.1 read-pkg@3.0.0 read-pkg@5.2.0 read@1.0.7 readable-stream@2.3.8 readdirp@3.6.0 reading-time@1.5.0 rechoir@0.6.2 recursive-readdir@2.2.3 redent@3.0.0 regenerate-unicode-properties@10.1.0 regenerate-unicode-properties@9.0.0 regenerate@1.4.2 regenerator-runtime@0.13.11 regexpu-core@4.8.0 registry-auth-token@5.0.2 registry-url@6.0.1 regjsgen@0.5.2 regjsparser@0.7.0 regjsparser@0.9.1 relateurl@0.2.7 renderkid@3.0.0 repeat-string@1.6.1 require-directory@2.1.1 require-from-string@2.0.2 require-like@0.1.2 requires-port@1.0.0 resolve-alpn@1.2.1 resolve-cwd@3.0.0 resolve-from@5.0.0 resolve-from@4.0.0 resolve-pathname@3.0.0 resolve@2.0.0-next.4 responselike@3.0.0 restore-cursor@3.1.0 retry@0.12.0 retry@0.13.1 reusify@1.0.4 rfdc@1.3.0 rimraf@2.7.1 rimraf@3.0.2 rollup-plugin-terser@7.0.2 rollup@2.79.1 rtl-detect@1.0.4 run-async@2.4.1 run-parallel@1.2.0 rw@1.3.3 sade@1.8.1 safe-buffer@5.1.2 safe-buffer@5.2.1 safe-regex-test@1.0.0 safer-buffer@2.1.2 sax@1.2.4 saxes@6.0.0 schema-utils@2.7.0 section-matter@1.0.0 select-hose@2.0.0 selfsigned@2.1.1 semver-diff@4.0.0 semver@7.3.4 semver@7.3.8 send@0.18.0 serialize-javascript@4.0.0 serialize-javascript@6.0.1 serve-handler@6.1.5 serve-index@1.9.1 serve-static@1.15.0 set-blocking@2.0.0 setimmediate@1.0.5 setprototypeof@1.1.0 setprototypeof@1.2.0 shallow-clone@3.0.1 shallowequal@1.1.0 shebang-command@1.2.0 shebang-command@2.0.0 shebang-regex@1.0.0 shebang-regex@3.0.0 shelljs@0.8.5 side-channel@1.0.4 signal-exit@3.0.7 simple-concat@1.0.1 simple-get@4.0.1 simple-swizzle@0.2.2 sirv@1.0.19 sisteransi@1.0.5 sitemap@7.1.1 slash@3.0.0 slash@4.0.0 slice-ansi@3.0.0 slice-ansi@4.0.0 slice-ansi@5.0.0 smart-buffer@4.2.0 sockjs@0.3.24 socks-proxy-agent@6.2.1 socks-proxy-agent@7.0.0 socks@2.7.1 sort-keys@2.0.0 source-map-support@0.5.13 source-map-support@0.5.21 source-map@0.6.1 source-map@0.7.4 source-map@0.8.0-beta.0 sourcemap-codec@1.4.8 space-separated-tokens@2.0.2 spdx-correct@3.2.0 spdx-exceptions@2.3.0 spdx-expression-parse@3.0.1 spdy-transport@3.0.0 spdy@4.0.2 split2@3.2.2 split@1.0.1 sprintf-js@1.0.3 ssri@9.0.1 ssri@8.0.1 stack-utils@2.0.6 statuses@2.0.1 statuses@1.5.0 string-length@4.0.2 string-width@5.1.2 string.prototype.matchall@4.0.8 string.prototype.padend@3.1.4 string.prototype.trimend@1.0.6 string.prototype.trimstart@1.0.6 string_decoder@1.3.0 string_decoder@1.1.1 stringify-entities@4.0.3 stringify-object@3.3.0 strip-bom-string@1.0.0 strip-bom@3.0.0 strip-bom@4.0.0 strip-comments@2.0.1 strip-final-newline@2.0.0 strip-final-newline@3.0.0 strip-indent@3.0.0 strip-json-comments@3.1.1 strip-json-comments@2.0.1 strong-log-transformer@2.1.0 style-search@0.1.0 stylelint-config-prettier@9.0.5 stylelint-config-recommended@9.0.0 stylelint-config-standard@29.0.0 stylelint@14.16.1 supports-color@5.5.0 supports-color@7.2.0 supports-color@8.1.1 supports-hyperlinks@2.3.0 supports-preserve-symlinks-flag@1.0.0 svg-parser@2.0.4 svg-tags@1.0.0 swc-loader@0.2.3 symbol-tree@3.2.4 table@6.8.1 tapable@1.1.3 tapable@2.2.1 tar-fs@2.1.1 tar-stream@2.2.0 tar@6.1.11 tar@4.4.19 temp-dir@1.0.0 temp-dir@2.0.0 tempy@0.6.0 test-exclude@6.0.0 text-extensions@1.9.0 text-table@0.2.0 thenify-all@1.6.0 thenify@3.3.1 through2@2.0.5 through2@4.0.2 through@2.3.8 thunky@1.1.0 tiny-invariant@1.3.1 tiny-warning@1.0.3 tmp-promise@3.0.3 tmp@0.0.33 tmp@0.2.1 tmpl@1.0.5 to-fast-properties@2.0.0 to-regex-range@5.0.1 to-vfile@6.1.0 toidentifier@1.0.1 totalist@1.1.0 tr46@1.0.1 tr46@3.0.0 tr46@0.0.3 traverse@0.3.9 tree-node-cli@1.6.0 trim-lines@3.0.1 trim-newlines@3.0.1 trough@2.1.0 ts-dedent@2.2.0 tsconfig-paths@3.14.2 tslib@1.14.1 tsutils@3.21.0 tunnel-agent@0.6.0 type-check@0.4.0 type-detect@4.0.8 type-fest@0.16.0 type-fest@0.18.1 type-fest@0.20.2 type-fest@0.21.3 type-fest@0.4.1 type-fest@0.6.0 type-fest@0.8.1 type-fest@1.4.0 type-fest@2.19.0 type-is@1.6.18 typed-array-length@1.0.4 typedarray-to-buffer@3.1.5 typedarray@0.0.6 typescript@4.9.5 uglify-js@3.17.4 unbox-primitive@1.0.2 unicode-canonical-property-names-ecmascript@2.0.0 unicode-match-property-ecmascript@2.0.0 unicode-match-property-value-ecmascript@2.1.0 unicode-property-aliases-ecmascript@2.1.0 unique-filename@1.1.1 unique-filename@2.0.1 unique-slug@2.0.2 unique-slug@3.0.0 unique-string@2.0.0 unique-string@3.0.0 unist-builder@2.0.3 unist-util-stringify-position@2.0.3 unist-util-stringify-position@3.0.3 universal-user-agent@6.0.0 universalify@0.2.0 universalify@2.0.0 unpipe@1.0.0 upath@2.0.1 upath@1.2.0 update-notifier@6.0.2 uri-js@4.4.1 url-loader@4.1.1 url-parse@1.5.10 util-deprecate@1.0.2 utila@0.4.0 utility-types@3.10.0 utils-merge@1.0.1 uuid@8.3.2 uuid@9.0.0 uvu@0.5.6 v8-compile-cache@2.3.0 v8-to-istanbul@9.1.0 validate-npm-package-license@3.0.4 validate-npm-package-name@4.0.0 validate-npm-package-name@3.0.0 value-equal@1.0.1 vary@1.1.2 vfile-message@2.0.4 vfile@4.2.1 w3c-xmlserializer@4.0.0 walk-up-path@1.0.0 walker@1.0.8 watchpack@2.4.0 wbuf@1.7.3 wcwidth@1.0.1 web-namespaces@2.0.1 web-worker@1.2.0 webidl-conversions@3.0.1 webidl-conversions@4.0.2 webidl-conversions@7.0.0 webpack-sources@3.2.3 webpackbar@5.0.2 websocket-driver@0.7.4 websocket-extensions@0.1.4 whatwg-encoding@2.0.0 whatwg-mimetype@3.0.0 whatwg-url@11.0.0 whatwg-url@5.0.0 whatwg-url@7.1.0 which-boxed-primitive@1.0.2 which@1.3.1 which@2.0.2 wide-align@1.1.5 widest-line@4.0.1 wordwrap@1.0.0 wrappy@1.0.2 write-file-atomic@4.0.1 write-file-atomic@2.4.3 write-file-atomic@3.0.3 write-file-atomic@4.0.2 write-json-file@3.2.0 write-pkg@4.0.0 xdg-basedir@5.1.0 xml-js@1.6.11 xml-name-validator@4.0.0 xmlchars@2.2.0 xtend@4.0.2 y18n@5.0.8 yallist@3.1.1 yallist@4.0.0 yaml@1.10.2 yargs-parser@20.2.4 yargs-parser@21.1.1 yargs-parser@20.2.9 yargs@16.2.0 yauzl@2.10.0 yocto-queue@0.1.0 zwitch@2.0.4",
]

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
            setup_env=DOCUSAURUS_ENV_SCRIPT_LIST,
            test=[
                "yarn test packages/docusaurus-plugin-content-docs/src/client/__tests__/docsClientUtils.test.ts --verbose"
            ],
            log_parser=jest_log_parser,
        ),
        "10130": JavaScriptAdapter(
            version="20",
            install=["yarn install"],
            setup_env=DOCUSAURUS_ENV_SCRIPT_LIST,
            test=[
                "yarn test packages/docusaurus/src/server/__tests__/brokenLinks.test.ts --verbose"
            ],
            log_parser=jest_log_parser,
        ),
        "9897": JavaScriptAdapter(
            version="20",
            install=["yarn install"],
            setup_env=DOCUSAURUS_ENV_SCRIPT_LIST,
            test=[
                "yarn test packages/docusaurus-utils/src/__tests__/markdownUtils.test.ts --verbose"
            ],
            log_parser=jest_log_parser,
        ),
        "9183": JavaScriptAdapter(
            version="20",
            install=["yarn install"],
            setup_env=DOCUSAURUS_ENV_SCRIPT_LIST,
            test=[
                "yarn test packages/docusaurus-theme-classic/src/__tests__/options.test.ts --verbose"
            ],
            log_parser=jest_log_parser,
        ),
        "8927": JavaScriptAdapter(
            version="20",
            install=["yarn install"],
            setup_env=DOCUSAURUS_ENV_SCRIPT_LIST,
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
            # TODO: mvnd?
            test=[
                # FAIL_TO_PASS
                "mvn test -B -T 1C -pl gson -Dtest=com.google.gson.functional.PrimitiveTest#testByteSerialization",
                "mvn test -B -T 1C -pl gson -Dtest=com.google.gson.functional.PrimitiveTest#testShortSerialization",
                "mvn test -B -T 1C -pl gson -Dtest=com.google.gson.functional.PrimitiveTest#testIntSerialization",
                "mvn test -B -T 1C -pl gson -Dtest=com.google.gson.functional.PrimitiveTest#testLongSerialization",
                "mvn test -B -T 1C -pl gson -Dtest=com.google.gson.functional.PrimitiveTest#testFloatSerialization",
                "mvn test -B -T 1C -pl gson -Dtest=com.google.gson.functional.PrimitiveTest#testDoubleSerialization",
                # PASS_TO_PASS
                "mvn test -B -T 1C -pl gson -Dtest=com.google.gson.functional.PrimitiveTest#testPrimitiveIntegerAutoboxedSerialization",
                "mvn test -B -T 1C -pl gson -Dtest=com.google.gson.functional.PrimitiveTest#testPrimitiveIntegerAutoboxedInASingleElementArraySerialization",
                "mvn test -B -T 1C -pl gson -Dtest=com.google.gson.functional.PrimitiveTest#testReallyLongValuesSerialization",
                "mvn test -B -T 1C -pl gson -Dtest=com.google.gson.functional.PrimitiveTest#testPrimitiveLongAutoboxedSerialization",
            ],
        ),
        "2024": JavaMavenAdapter(
            version="11",
            install=[
                "mvn test -B -pl gson -Dtest=com.google.gson.functional.FieldNamingTest,com.google.gson.functional.NamingPolicyTest -q",
            ],
            test=[
                # FAIL_TO_PASS
                "mvn test -B -T 1C -pl gson -Dtest=com.google.gson.functional.FieldNamingTest#testUpperCaseWithUnderscores",
                "mvn test -B -T 1C -pl gson -Dtest=com.google.gson.functional.NamingPolicyTest#testGsonWithUpperCaseUnderscorePolicySerialization",
                "mvn test -B -T 1C -pl gson -Dtest=com.google.gson.functional.NamingPolicyTest#testGsonWithUpperCaseUnderscorePolicyDeserialiation",
            ],
        ),
        "2479": JavaMavenAdapter(
            version="11",
            install=[
                "mvn test -B -pl gson -Dtest=com.google.gson.GsonBuilderTest -q",
            ],
            test=[
                # FAIL_TO_PASS
                "mvn test -B -T 1C -pl gson -Dtest=com.google.gson.GsonBuilderTest#testRegisterTypeAdapterForObjectAndJsonElements",
                "mvn test -B -T 1C -pl gson -Dtest=com.google.gson.GsonBuilderTest#testRegisterTypeHierarchyAdapterJsonElements",
                # PASS_TO_PASS
                "mvn test -B -T 1C -pl gson -Dtest=com.google.gson.GsonBuilderTest#testModificationAfterCreate",
            ],
        ),
        "2134": JavaMavenAdapter(
            version="11",
            install=[
                "mvn test -B -pl gson -Dtest=com.google.gson.internal.bind.util.ISO8601UtilsTest -q",
            ],
            test=[
                # FAIL_TO_PASS
                "mvn test -B -T 1C -pl gson -Dtest=com.google.gson.internal.bind.util.ISO8601UtilsTest#testDateParseInvalidDay",
                "mvn test -B -T 1C -pl gson -Dtest=com.google.gson.internal.bind.util.ISO8601UtilsTest#testDateParseInvalidMonth",
                # PASS_TO_PASS
                "mvn test -B -T 1C -pl gson -Dtest=com.google.gson.internal.bind.util.ISO8601UtilsTest#testDateParseWithDefaultTimezone",
            ],
        ),
        "2061": JavaMavenAdapter(
            version="11",
            install=[
                "mvn test -B -pl gson -Dtest=com.google.gson.stream.JsonReaderTest,com.google.gson.internal.bind.JsonTreeReaderTest -q"
            ],
            test=[
                # FAIL_TO_PASS
                "mvn test -B -T 1C -pl gson -Dtest=com.google.gson.stream.JsonReaderTest#testHasNextEndOfDocument",
                "mvn test -B -T 1C -pl gson -Dtest=com.google.gson.internal.bind.JsonTreeReaderTest#testHasNext_endOfDocument",
                # PASS_TO_PASS
                "mvn test -B -T 1C -pl gson -Dtest=com.google.gson.stream.JsonReaderTest#testReadEmptyObject",
                "mvn test -B -T 1C -pl gson -Dtest=com.google.gson.stream.JsonReaderTest#testReadEmptyArray",
                "mvn test -B -T 1C -pl gson -Dtest=com.google.gson.internal.bind.JsonTreeReaderTest#testSkipValue_emptyJsonObject",
                "mvn test -B -T 1C -pl gson -Dtest=com.google.gson.internal.bind.JsonTreeReaderTest#testSkipValue_filledJsonObject",
            ],
        ),
    },
    "apache/druid": {
        "15402": JavaMavenAdapter(
            version="11",
            install=[
                "mvn test -B -pl processing -Dtest=org.apache.druid.query.groupby.GroupByQueryQueryToolChestTest -q"
            ],
            test=[
                # FAIL_TO_PASS
                "mvn test -B -T 1C -pl processing -Dtest=org.apache.druid.query.groupby.GroupByQueryQueryToolChestTest#testCacheStrategy",
                # PASS_TO_PASS
                "mvn test -B -T 1C -pl processing -Dtest=org.apache.druid.query.groupby.GroupByQueryQueryToolChestTest#testResultLevelCacheKeyWithSubTotalsSpec",
                "mvn test -B -T 1C -pl processing -Dtest=org.apache.druid.query.groupby.GroupByQueryQueryToolChestTest#testMultiColumnCacheStrategy",
            ],
        ),
        "14092": JavaMavenAdapter(
            version="11",
            install=[
                "mvn clean install -B -pl processing,cloud/aws-common,cloud/gcp-common -DskipTests -am",
                "mvn test -B -T 1C -pl server -Dtest=org.apache.druid.discovery.DruidLeaderClientTest -q",
            ],
            test=[
                # FAIL_TO_PASS
                "mvn test -B -T 1C -pl server -Dtest=org.apache.druid.discovery.DruidLeaderClientTest#test503ResponseFromServerAndCacheRefresh",
                # PASS_TO_PASS
                "mvn test -B -T 1C -pl server -Dtest=org.apache.druid.discovery.DruidLeaderClientTest#testServerFailureAndRedirect",
            ],
        ),
        "14136": JavaMavenAdapter(
            version="11",
            install=[
                "mvn test -B -pl processing -Dtest=org.apache.druid.timeline.VersionedIntervalTimelineTest -q",
            ],
            test=[
                # FAIL_TO_PASS
                "mvn test -B -T 1C -pl processing -Dtest=org.apache.druid.timeline.VersionedIntervalTimelineTest#testOverlapSecondContainsFirstZeroLengthInterval",
                "mvn test -B -T 1C -pl processing -Dtest=org.apache.druid.timeline.VersionedIntervalTimelineTest#testOverlapSecondContainsFirstZeroLengthInterval2",
                "mvn test -B -T 1C -pl processing -Dtest=org.apache.druid.timeline.VersionedIntervalTimelineTest#testOverlapSecondContainsFirstZeroLengthInterval3",
                "mvn test -B -T 1C -pl processing -Dtest=org.apache.druid.timeline.VersionedIntervalTimelineTest#testOverlapSecondContainsFirstZeroLengthInterval4",
                # PASS_TO_PASS
                "mvn test -B -T 1C -pl processing -Dtest=org.apache.druid.timeline.VersionedIntervalTimelineTest#testOverlapFirstContainsSecond",
                "mvn test -B -T 1C -pl processing -Dtest=org.apache.druid.timeline.VersionedIntervalTimelineTest#testOverlapSecondContainsFirst",
            ],
        ),
        "13704": JavaMavenAdapter(
            version="11",
            install=[
                # Update the pom.xml to use the correct version of the resource bundle. See https://github.com/apache/druid/pull/14054
                r"sed -i 's/<resourceBundle>org.apache.apache.resources:apache-jar-resource-bundle:1.5-SNAPSHOT<\/resourceBundle>/<resourceBundle>org.apache.apache.resources:apache-jar-resource-bundle:1.5<\/resourceBundle>/' pom.xml",
                "mvn clean install -B -pl processing -DskipTests -am",
            ],
            test=[
                # FAIL_TO_PASS
                "mvn test -B -pl processing -Dtest=org.apache.druid.query.aggregation.post.ArithmeticPostAggregatorTest#testPow",
                # PASS_TO_PASS
                "mvn test -B -pl processing -Dtest=org.apache.druid.query.aggregation.post.ArithmeticPostAggregatorTest#testDiv",
                "mvn test -B -pl processing -Dtest=org.apache.druid.query.aggregation.post.ArithmeticPostAggregatorTest#testQuotient",
            ],
        ),
        "16875": JavaMavenAdapter(
            version="11",
            install=[
                "mvn clean install -B -pl server -DskipTests -am",
            ],
            test=[
                # FAIL_TO_PASS
                "mvn test -B -pl server -Dtest=org.apache.druid.server.metrics.WorkerTaskCountStatsMonitorTest#testMonitorWithPeon",
                # PASS_TO_PASS
                "mvn test -B -pl server -Dtest=org.apache.druid.server.metrics.WorkerTaskCountStatsMonitorTest#testMonitorWithNulls",
                "mvn test -B -pl server -Dtest=org.apache.druid.server.metrics.WorkerTaskCountStatsMonitorTest#testMonitorIndexer",
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
            install=["go test -c ./markup/goldmark/blockquotes/..."],
            test=["go test -v ./markup/goldmark/blockquotes/..."],
        ),
        "12579": GoAdapter(
            version="1.23",
            install=['go test -c ./resources/page/... -run "^TestGroupBy"'],
            test=['go test -v ./resources/page/... -run "^TestGroupBy"'],
        ),
        "12562": GoAdapter(
            version="1.23",
            install=['go test -c ./hugolib/... -run "^TestGetPage[^/]"'],
            test=['go test -v ./hugolib/... -run "^TestGetPage[^/]"'],
        ),
        "12448": GoAdapter(
            version="1.23",
            install=['go test -c ./hugolib/... -run "^TestRebuild"'],
            test=['go test -v ./hugolib/... -run "^TestRebuild"'],
        ),
        "12343": GoAdapter(
            version="1.23",
            install=['go test -c ./resources/page/... -run "^Test.*Permalink"'],
            test=['go test -v ./resources/page/... -run "^Test.*Permalink"'],
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
}
