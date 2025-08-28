#!/bin/bash

# Function to print the test echo message
print_echo() {
    echo "test echo"
}

# Main execution
if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
    print_echo
else
    # When sourced, still execute the function
    print_echo
fi