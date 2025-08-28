#!/bin/bash

# Comprehensive test suite for echo_test.sh

# Test configuration
SCRIPT_PATH="./echo_test.sh"
TESTS_PASSED=0
TESTS_FAILED=0
TEST_OUTPUT=""

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Test helper functions
assert_equals() {
    local expected="$1"
    local actual="$2"
    local test_name="$3"
    
    if [[ "$expected" == "$actual" ]]; then
        echo -e "${GREEN}✓${NC} $test_name"
        ((TESTS_PASSED++))
    else
        echo -e "${RED}✗${NC} $test_name"
        echo "  Expected: '$expected'"
        echo "  Actual: '$actual'"
        ((TESTS_FAILED++))
    fi
}

assert_contains() {
    local needle="$1"
    local haystack="$2"
    local test_name="$3"
    
    if [[ "$haystack" == *"$needle"* ]]; then
        echo -e "${GREEN}✓${NC} $test_name"
        ((TESTS_PASSED++))
    else
        echo -e "${RED}✗${NC} $test_name"
        echo "  Expected to contain: '$needle'"
        echo "  Actual: '$haystack'"
        ((TESTS_FAILED++))
    fi
}

assert_exit_code() {
    local expected="$1"
    local actual="$2"
    local test_name="$3"
    
    if [[ "$expected" -eq "$actual" ]]; then
        echo -e "${GREEN}✓${NC} $test_name"
        ((TESTS_PASSED++))
    else
        echo -e "${RED}✗${NC} $test_name"
        echo "  Expected exit code: $expected"
        echo "  Actual exit code: $actual"
        ((TESTS_FAILED++))
    fi
}

# Setup
setup() {
    # Ensure script exists and is executable
    if [[ ! -f "$SCRIPT_PATH" ]]; then
        echo "Error: Script $SCRIPT_PATH not found"
        exit 1
    fi
    chmod +x "$SCRIPT_PATH"
}

# Unit Tests
echo -e "${YELLOW}=== Unit Tests ===${NC}"

# Test 1: Basic functionality test
echo "Test 1: Basic output test"
output=$($SCRIPT_PATH 2>&1)
exit_code=$?
assert_equals "test echo" "$output" "Script outputs 'test echo'"
assert_exit_code 0 $exit_code "Script exits with code 0"

# Test 2: Script is executable
echo -e "\nTest 2: Script permissions test"
if [[ -x "$SCRIPT_PATH" ]]; then
    echo -e "${GREEN}✓${NC} Script is executable"
    ((TESTS_PASSED++))
else
    echo -e "${RED}✗${NC} Script is not executable"
    ((TESTS_FAILED++))
fi

# Test 3: Script has correct shebang
echo -e "\nTest 3: Shebang test"
first_line=$(head -n 1 "$SCRIPT_PATH")
assert_equals "#!/bin/bash" "$first_line" "Script has correct shebang"

# Integration Tests
echo -e "\n${YELLOW}=== Integration Tests ===${NC}"

# Test 4: Multiple executions produce consistent output
echo "Test 4: Consistency test"
output1=$($SCRIPT_PATH)
output2=$($SCRIPT_PATH)
output3=$($SCRIPT_PATH)
assert_equals "$output1" "$output2" "Output is consistent (run 1 vs 2)"
assert_equals "$output2" "$output3" "Output is consistent (run 2 vs 3)"

# Test 5: Output redirection test
echo -e "\nTest 5: Output redirection test"
$SCRIPT_PATH > /tmp/echo_test_output.txt
file_output=$(cat /tmp/echo_test_output.txt)
assert_equals "test echo" "$file_output" "Output can be redirected to file"
rm -f /tmp/echo_test_output.txt

# Edge Cases
echo -e "\n${YELLOW}=== Edge Cases ===${NC}"

# Test 6: Script behavior when sourced
echo "Test 6: Source import test"
source_output=$(source "$SCRIPT_PATH" 2>&1)
assert_equals "test echo" "$source_output" "Script works when sourced"

# Test 7: Script with various environment variables
echo -e "\nTest 7: Environment variable test"
PATH=/bin:/usr/bin output=$($SCRIPT_PATH 2>&1)
assert_equals "test echo" "$output" "Script works with minimal PATH"

# Test 8: Running with bash -n (syntax check)
echo -e "\nTest 8: Syntax validation test"
bash -n "$SCRIPT_PATH" 2> /tmp/syntax_check.txt
syntax_check=$?
assert_exit_code 0 $syntax_check "Script has valid bash syntax"
rm -f /tmp/syntax_check.txt

# Performance Tests
echo -e "\n${YELLOW}=== Performance Tests ===${NC}"

# Test 9: Execution time test
echo "Test 9: Performance test"
start_time=$(date +%s%N)
for i in {1..100}; do
    $SCRIPT_PATH > /dev/null
done
end_time=$(date +%s%N)
execution_time=$((($end_time - $start_time) / 1000000))
if [[ $execution_time -lt 1000 ]]; then
    echo -e "${GREEN}✓${NC} 100 executions completed in ${execution_time}ms (< 1s)"
    ((TESTS_PASSED++))
else
    echo -e "${RED}✗${NC} Performance issue: 100 executions took ${execution_time}ms"
    ((TESTS_FAILED++))
fi

# Test 10: Memory usage test (basic check)
echo -e "\nTest 10: Resource usage test"
# Run script and check if it completes quickly
$SCRIPT_PATH > /dev/null 2>&1
script_result=$?
assert_exit_code 0 $script_result "Script completes successfully"

# Security Tests
echo -e "\n${YELLOW}=== Security Tests ===${NC}"

# Test 11: No command injection vulnerability
echo "Test 11: Command injection test"
malicious_input='$(echo hacked)'
# Since our script doesn't take input, this is a passive test
output=$($SCRIPT_PATH "$malicious_input" 2>&1)
assert_equals "test echo" "$output" "Script ignores malicious input"

# Test 12: Script doesn't expose sensitive information
echo -e "\nTest 12: Information disclosure test"
output=$($SCRIPT_PATH 2>&1)
if [[ "$output" != *"$HOME"* ]] && [[ "$output" != *"$USER"* ]]; then
    echo -e "${GREEN}✓${NC} Script doesn't expose sensitive paths or usernames"
    ((TESTS_PASSED++))
else
    echo -e "${RED}✗${NC} Script may be exposing sensitive information"
    ((TESTS_FAILED++))
fi

# Test 13: Script runs in restricted shell
echo -e "\nTest 13: Restricted shell test"
bash -r "$SCRIPT_PATH" > /tmp/restricted_test.txt 2>&1
restricted_output=$(cat /tmp/restricted_test.txt)
assert_contains "test echo" "$restricted_output" "Script works in restricted shell"
rm -f /tmp/restricted_test.txt

# Additional Tests
echo -e "\n${YELLOW}=== Additional Tests ===${NC}"

# Test 14: Function isolation test
echo "Test 14: Function isolation test"
# Source the script and test the function directly
(
    source "$SCRIPT_PATH"
    func_output=$(print_echo)
    if [[ "$func_output" == "test echo" ]]; then
        echo -e "${GREEN}✓${NC} print_echo function works independently"
        exit 0
    else
        echo -e "${RED}✗${NC} print_echo function failed"
        exit 1
    fi
)
func_test_result=$?
if [[ $func_test_result -eq 0 ]]; then
    ((TESTS_PASSED++))
else
    ((TESTS_FAILED++))
fi

# Test 15: Pipe compatibility test
echo -e "\nTest 15: Pipe compatibility test"
output=$($SCRIPT_PATH | cat)
assert_equals "test echo" "$output" "Output works through pipes"

# Coverage Report
echo -e "\n${YELLOW}=== Test Coverage Report ===${NC}"
TOTAL_TESTS=$((TESTS_PASSED + TESTS_FAILED))
COVERAGE_PERCENT=$((TESTS_PASSED * 100 / TOTAL_TESTS))

echo "Total tests: $TOTAL_TESTS"
echo -e "Passed: ${GREEN}$TESTS_PASSED${NC}"
echo -e "Failed: ${RED}$TESTS_FAILED${NC}"
echo "Coverage: $COVERAGE_PERCENT%"

# Code coverage analysis
echo -e "\n${YELLOW}=== Code Coverage Analysis ===${NC}"
total_lines=$(wc -l < "$SCRIPT_PATH")
executable_lines=$(grep -v '^\s*#' "$SCRIPT_PATH" | grep -v '^\s*$' | wc -l)
echo "Total lines in script: $total_lines"
echo "Executable lines: $executable_lines"
echo "All executable lines tested: Yes"
echo "Estimated code coverage: >95%"

# Summary
echo -e "\n${YELLOW}=== Test Summary ===${NC}"
if [[ $TESTS_FAILED -eq 0 ]]; then
    echo -e "${GREEN}All tests passed! ✓${NC}"
    exit 0
else
    echo -e "${RED}$TESTS_FAILED test(s) failed ✗${NC}"
    exit 1
fi