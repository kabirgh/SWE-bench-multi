#!/bin/bash
set -uxo pipefail
cd /testbed
git config --global --add safe.directory /testbed
cd /testbed
git status
git diff fbd065256ca00d68089293ad48ea9aeba5481914
git checkout fbd065256ca00d68089293ad48ea9aeba5481914 
git apply -v - <<'EOF_114329324912'
diff --git a/packages/babel-generator/test/fixtures/parentheses/unary-postfix/input.js b/packages/babel-generator/test/fixtures/parentheses/unary-postfix/input.js
new file mode 100644
index 000000000000..1603497b5d89
--- /dev/null
+++ b/packages/babel-generator/test/fixtures/parentheses/unary-postfix/input.js
@@ -0,0 +1,1 @@
+(function () { return {x: 24} }()).x++;
diff --git a/packages/babel-generator/test/fixtures/parentheses/unary-postfix/output.js b/packages/babel-generator/test/fixtures/parentheses/unary-postfix/output.js
new file mode 100644
index 000000000000..f07a72eed6f8
--- /dev/null
+++ b/packages/babel-generator/test/fixtures/parentheses/unary-postfix/output.js
@@ -0,0 +1,5 @@
+(function () {
+  return {
+    x: 24
+  };
+})().x++;
\ No newline at end of file

EOF_114329324912
make build
yarn jest babel-generator --verbose
git checkout fbd065256ca00d68089293ad48ea9aeba5481914 
