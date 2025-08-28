#!/bin/bash

# Test suite for echo.sh script
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ECHO_SCRIPT="$SCRIPT_DIR/echo.sh"
PASS_COUNT=0
FAIL_COUNT=0

# Colors for output
GREEN='\033[0;32m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Test function
run_test() {
    local test_name="$1"
    local expected="$2"
    local actual="$3"
    
    if [ "$actual" = "$expected" ]; then
        echo -e "${GREEN}✓${NC} $test_name"
        ((PASS_COUNT++))
    else
        echo -e "${RED}✗${NC} $test_name"
        echo "  Expected: '$expected'"
        echo "  Actual: '$actual'"
        ((FAIL_COUNT++))
    fi
}

echo "Running tests for echo.sh..."
echo "================================"

# Test 1: Check if script exists
if [ -f "$ECHO_SCRIPT" ]; then
    echo -e "${GREEN}✓${NC} Script file exists"
    ((PASS_COUNT++))
else
    echo -e "${RED}✗${NC} Script file not found at $ECHO_SCRIPT"
    ((FAIL_COUNT++))
    exit 1
fi

# Test 2: Check if script is executable
if [ -x "$ECHO_SCRIPT" ]; then
    echo -e "${GREEN}✓${NC} Script is executable"
    ((PASS_COUNT++))
else
    echo -e "${RED}✗${NC} Script is not executable"
    ((FAIL_COUNT++))
fi

# Test 3: Test script output
output=$("$ECHO_SCRIPT")
run_test "Script outputs correct text" "test echo" "$output"

# Test 4: Test exit code
"$ECHO_SCRIPT" > /dev/null 2>&1
exit_code=$?
run_test "Script exits with code 0" "0" "$exit_code"

# Test 5: Test script doesn't produce stderr
stderr_output=$("$ECHO_SCRIPT" 2>&1 1>/dev/null)
run_test "Script produces no stderr" "" "$stderr_output"

# Performance test
echo ""
echo "Performance Test:"
start_time=$(date +%s%N)
for i in {1..100}; do
    "$ECHO_SCRIPT" > /dev/null 2>&1
done
end_time=$(date +%s%N)
elapsed=$((($end_time - $start_time) / 1000000))
echo "100 executions took ${elapsed}ms"

if [ $elapsed -lt 1000 ]; then
    echo -e "${GREEN}✓${NC} Performance test passed (< 1s for 100 runs)"
    ((PASS_COUNT++))
else
    echo -e "${RED}✗${NC} Performance test failed (took ${elapsed}ms for 100 runs)"
    ((FAIL_COUNT++))
fi

# Security checks
echo ""
echo "Security Checks:"

# Check for command injection vulnerability
injection_test=$("$ECHO_SCRIPT" "; ls" 2>&1)
if [[ "$injection_test" == "test echo" ]]; then
    echo -e "${GREEN}✓${NC} No command injection vulnerability detected"
    ((PASS_COUNT++))
else
    echo -e "${RED}✗${NC} Potential command injection vulnerability"
    ((FAIL_COUNT++))
fi

# Summary
echo ""
echo "================================"
echo "Test Summary:"
echo -e "Passed: ${GREEN}$PASS_COUNT${NC}"
echo -e "Failed: ${RED}$FAIL_COUNT${NC}"

if [ $FAIL_COUNT -eq 0 ]; then
    echo -e "${GREEN}All tests passed!${NC}"
    exit 0
else
    echo -e "${RED}Some tests failed.${NC}"
    exit 1
fi