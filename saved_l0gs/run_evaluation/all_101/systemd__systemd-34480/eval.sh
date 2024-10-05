#!/bin/bash
set -uxo pipefail
cd /testbed
git config --global --add safe.directory /testbed
cd /testbed
git status
git diff 4beac1034d51e3cedb79cedf57e274b02b690eeb
git checkout 4beac1034d51e3cedb79cedf57e274b02b690eeb src/test/test-seccomp.c
git apply -v - <<'EOF_114329324912'
diff --git a/src/test/test-seccomp.c b/src/test/test-seccomp.c
index 74d950ad1c0a0..459708ee00c28 100644
--- a/src/test/test-seccomp.c
+++ b/src/test/test-seccomp.c
@@ -18,6 +18,7 @@
 #include "capability-util.h"
 #include "fd-util.h"
 #include "fileio.h"
+#include "fs-util.h"
 #include "macro.h"
 #include "memory-util.h"
 #include "missing_sched.h"
@@ -1229,4 +1230,55 @@ TEST(restrict_suid_sgid) {
         assert_se(wait_for_terminate_and_check("suidsgidseccomp", pid, WAIT_LOG) == EXIT_SUCCESS);
 }
 
+static void test_seccomp_suppress_sync_child(void) {
+        _cleanup_(unlink_and_freep) char *path = NULL;
+        _cleanup_close_ int fd = -EBADF;
+
+        ASSERT_OK(tempfn_random("/tmp/seccomp_suppress_sync", NULL, &path));
+        ASSERT_OK_ERRNO(fd = open(path, O_RDWR | O_CREAT | O_SYNC | O_CLOEXEC, 0666));
+        fd = safe_close(fd);
+
+        ASSERT_ERROR_ERRNO(fdatasync(-1), EBADF);
+        ASSERT_ERROR_ERRNO(fsync(-1), EBADF);
+        ASSERT_ERROR_ERRNO(syncfs(-1), EBADF);
+
+        ASSERT_ERROR_ERRNO(fdatasync(INT_MAX), EBADF);
+        ASSERT_ERROR_ERRNO(fsync(INT_MAX), EBADF);
+        ASSERT_ERROR_ERRNO(syncfs(INT_MAX), EBADF);
+
+        ASSERT_OK(seccomp_suppress_sync());
+
+        ASSERT_ERROR_ERRNO(fd = open(path, O_RDWR | O_CREAT | O_SYNC | O_CLOEXEC, 0666), EINVAL);
+
+        ASSERT_OK_ERRNO(fdatasync(INT_MAX));
+        ASSERT_OK_ERRNO(fsync(INT_MAX));
+        ASSERT_OK_ERRNO(syncfs(INT_MAX));
+
+        ASSERT_ERROR_ERRNO(fdatasync(-1), EBADF);
+        ASSERT_ERROR_ERRNO(fsync(-1), EBADF);
+        ASSERT_ERROR_ERRNO(syncfs(-1), EBADF);
+}
+
+TEST(seccomp_suppress_sync) {
+        pid_t pid;
+
+        if (!is_seccomp_available()) {
+                log_notice("Seccomp not available, skipping %s", __func__);
+                return;
+        }
+        if (!have_seccomp_privs()) {
+                log_notice("Not privileged, skipping %s", __func__);
+                return;
+        }
+
+        ASSERT_OK_ERRNO(pid = fork());
+
+        if (pid == 0) {
+                test_seccomp_suppress_sync_child();
+                _exit(EXIT_SUCCESS);
+        }
+
+        ASSERT_EQ(wait_for_terminate_and_check("seccomp_suppress_sync", pid, WAIT_LOG), EXIT_SUCCESS);
+}
+
 DEFINE_TEST_MAIN(LOG_DEBUG);

EOF_114329324912
meson setup build
ninja -C build test-seccomp
meson test -C build -v test-seccomp
git checkout 4beac1034d51e3cedb79cedf57e274b02b690eeb src/test/test-seccomp.c
