#!/bin/bash
set -uxo pipefail
cd /testbed
git config --global --add safe.directory /testbed
cd /testbed
git status
git diff 1435c8ae4aa1041592778018ba62fc3058a9ad3d
git checkout 1435c8ae4aa1041592778018ba62fc3058a9ad3d promql/promqltest/testdata/functions.test
git apply -v - <<'EOF_114329324912'
diff --git a/promql/promqltest/testdata/functions.test b/promql/promqltest/testdata/functions.test
index b89d44fced3..6e2b3630bcb 100644
--- a/promql/promqltest/testdata/functions.test
+++ b/promql/promqltest/testdata/functions.test
@@ -523,16 +523,16 @@ load 5m
 	node_uname_info{job="node_exporter", instance="4m1000", release="1.111.3"} 0+10x10
 
 eval_ordered instant at 50m sort_by_label(http_requests, "instance")
-	http_requests{group="production", instance="0", job="api-server"} 100
 	http_requests{group="canary", instance="0", job="api-server"} 300
-	http_requests{group="production", instance="0", job="app-server"} 500
 	http_requests{group="canary", instance="0", job="app-server"} 700
-	http_requests{group="production", instance="1", job="api-server"} 200
+	http_requests{group="production", instance="0", job="api-server"} 100
+	http_requests{group="production", instance="0", job="app-server"} 500
 	http_requests{group="canary", instance="1", job="api-server"} 400
-	http_requests{group="production", instance="1", job="app-server"} 600
 	http_requests{group="canary", instance="1", job="app-server"} 800
-	http_requests{group="production", instance="2", job="api-server"} 100
+	http_requests{group="production", instance="1", job="api-server"} 200
+	http_requests{group="production", instance="1", job="app-server"} 600
 	http_requests{group="canary", instance="2", job="api-server"} NaN
+	http_requests{group="production", instance="2", job="api-server"} 100
 
 eval_ordered instant at 50m sort_by_label(http_requests, "instance", "group")
 	http_requests{group="canary", instance="0", job="api-server"} 300
@@ -585,14 +585,14 @@ eval_ordered instant at 50m sort_by_label(http_requests, "job", "instance", "gro
 eval_ordered instant at 50m sort_by_label_desc(http_requests, "instance")
 	http_requests{group="production", instance="2", job="api-server"} 100
 	http_requests{group="canary", instance="2", job="api-server"} NaN
-	http_requests{group="canary", instance="1", job="app-server"} 800
 	http_requests{group="production", instance="1", job="app-server"} 600
-	http_requests{group="canary", instance="1", job="api-server"} 400
 	http_requests{group="production", instance="1", job="api-server"} 200
-	http_requests{group="canary", instance="0", job="app-server"} 700
+	http_requests{group="canary", instance="1", job="app-server"} 800
+	http_requests{group="canary", instance="1", job="api-server"} 400
 	http_requests{group="production", instance="0", job="app-server"} 500
-	http_requests{group="canary", instance="0", job="api-server"} 300
 	http_requests{group="production", instance="0", job="api-server"} 100
+	http_requests{group="canary", instance="0", job="app-server"} 700
+	http_requests{group="canary", instance="0", job="api-server"} 300
 
 eval_ordered instant at 50m sort_by_label_desc(http_requests, "instance", "group")
 	http_requests{group="production", instance="2", job="api-server"} 100

EOF_114329324912
go test -v ./promql -run "^TestEvaluations"
git checkout 1435c8ae4aa1041592778018ba62fc3058a9ad3d promql/promqltest/testdata/functions.test
