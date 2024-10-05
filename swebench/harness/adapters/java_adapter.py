from dataclasses import dataclass
import re
import shlex
from typing import Callable, List

from swebench.harness.constants import TestStatus
from swebench.harness.adapters.adapter import Adapter


@dataclass(kw_only=True)
class JavaAdapter(Adapter):
    version: str
    log_parser: Callable[[str], dict[str, str]]

    @property
    def language(self):
        return "java"

    @property
    def starting_image_name(self):
        return f"eclipse-temurin:{self.version}"

    def get_log_parser(self) -> Callable[[str], dict[str, str]]:
        return self.log_parser


@dataclass(kw_only=True)
class JavaMavenAdapter(Adapter):
    version: str

    @property
    def language(self):
        return "java"

    @property
    def starting_image_name(self):
        return f"maven:3.9-eclipse-temurin-{self.version}"

    def get_log_parser(self) -> Callable[[str], dict[str, str]]:
        return _maven_log_parser


def _maven_log_parser(log: str) -> dict[str, str]:
    """
    Parser for test logs generated with 'mvn test'.
    Annoyingly maven will not print the tests that have succeeded. Each test
    must be run individually, and then we look for BUILD (SUCCESS|FAILURE) in
    the logs. This means we to tweak the eval script to run each test
    individually.
    This log parser assumes that each test case is run in a separate command.

    Args:
        log (str): log content
    Returns:
        dict: test case to test status mapping
    """
    test_status_map = {}
    current_test_name = "---NO TEST NAME FOUND YET---"

    # Get the test name from the command used to execute the test.
    # Assumes we run evaluation with set -x
    test_name_pattern = r"^.*-Dtest=(\S+).*$"
    result_pattern = r"^.*BUILD (SUCCESS|FAILURE)$"

    for line in log.split("\n"):
        test_name_match = re.match(test_name_pattern, line.strip())
        if test_name_match:
            current_test_name = test_name_match.groups()[0]

        result_match = re.match(result_pattern, line.strip())
        if result_match:
            status = result_match.groups()[0]
            if status == "SUCCESS":
                test_status_map[current_test_name] = TestStatus.PASSED.value
            elif status == "FAILURE":
                test_status_map[current_test_name] = TestStatus.FAILED.value

    return test_status_map


def make_lombok_pre_install_script(tests: List[str]) -> List[str]:
    """
    There's no way to run individual tests out of the box, so this script
    modifies the xml file that defines test scripts to run individual tests with
    `ant test.instance`.
    """
    xml = rf"""
    <target name="test.instance" depends="test.compile, test.formatter.compile" description="Runs test cases for the swe-bench instance">
      <junit printsummary="yes" fork="true" forkmode="once" haltonfailure="no">
        <formatter classname="lombok.ant.SimpleTestFormatter" usefile="false" unless="tests.quiet" />
        <classpath location="build/ant" />
        <classpath refid="cp.test" />
        <classpath refid="cp.stripe" />
        <classpath refid="packing.basedirs.path" />
        <classpath location="build/tests" />
        <classpath location="build/teststubs" />
        {"\n".join(rf'<test name="{test}" />' for test in tests)}
      </junit>
    </target>
    """
    build_file = "buildScripts/tests.ant.xml"
    escaped_xml = shlex.quote(xml.strip())

    return [
        f"{{ head -n -1 {build_file}; echo {escaped_xml}; tail -n 1 {build_file}; }} > temp_file && mv temp_file {build_file}"
    ]


def ant_log_parser(log: str) -> dict[str, str]:
    test_status_map = {}

    pattern = r"^\s*\[junit\]\s+\[(PASS|FAIL|ERR)\]\s+(.*)$"

    for line in log.split("\n"):
        match = re.match(pattern, line.strip())
        if match:
            status, test_name = match.groups()
            if status == "PASS":
                test_status_map[test_name] = TestStatus.PASSED.value
            elif status in ["FAIL", "ERR"]:
                test_status_map[test_name] = TestStatus.FAILED.value

    return test_status_map


def make_lucene_pre_install_script() -> List[str]:
    """
    This script modifies the gradle config to print all test results, including
    passing tests.
    """
    gradle_file = "gradle/testing/defaults-tests.gradle"

    new_content = """testLogging {
  showStandardStreams = true
  // set options for log level LIFECYCLE
  events TestLogEvent.FAILED,
         TestLogEvent.PASSED,
         TestLogEvent.SKIPPED,
         TestLogEvent.STANDARD_OUT
  exceptionFormat TestExceptionFormat.FULL
  showExceptions true
  showCauses true
  showStackTraces true

  // set options for log level DEBUG and INFO
  debug {
      events TestLogEvent.STARTED,
             TestLogEvent.FAILED,
             TestLogEvent.PASSED,
             TestLogEvent.SKIPPED,
             TestLogEvent.STANDARD_ERROR,
             TestLogEvent.STANDARD_OUT
      exceptionFormat TestExceptionFormat.FULL
  }
  info.events = debug.events
  info.exceptionFormat = debug.exceptionFormat

  afterSuite { desc, result ->
      if (!desc.parent) { // will match the outermost suite
          def output = "Results: ${result.resultType} (${result.testCount} tests, ${result.successfulTestCount} passed, ${result.failedTestCount} failed, ${result.skippedTestCount} skipped)"
          def startItem = '|  ', endItem = '  |'
          def repeatLength = startItem.length() + output.length() + endItem.length()
          println('\\n' + ('-' * repeatLength) + '\\n' + startItem + output + endItem + '\\n' + ('-' * repeatLength))
      }
  }
}"""

    return [
        f"""
sed -i '
/testLogging {{/,/}}/{{
  /testLogging {{/r /dev/stdin
  d
}}
' {gradle_file} << 'EOF'
{new_content}
EOF
""".strip()
    ]


def gradle_custom_log_parser(log: str) -> dict[str, str]:
    """
    Parser for test logs generated with 'gradle test'. Assumes that the lucene
    pre-install script has run.
    """
    test_status_map = {}

    pattern = r"^([^>].+)\s+(PASSED|FAILED)$"

    for line in log.split("\n"):
        match = re.match(pattern, line.strip())
        if match:
            test_name, status = match.groups()
            if status == "PASSED":
                test_status_map[test_name] = TestStatus.PASSED.value
            elif status == "FAILED":
                test_status_map[test_name] = TestStatus.FAILED.value

    return test_status_map
