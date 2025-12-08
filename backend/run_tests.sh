#!/bin/bash

# Run tests inside the backend container
# Usage: ./run_tests.sh [pytest options]
# Examples:
#   ./run_tests.sh                          # Run all tests
#   ./run_tests.sh -m unit                  # Run only unit tests
#   ./run_tests.sh -m integration           # Run only integration tests
#   ./run_tests.sh tests/test_routes.py     # Run specific test file
#   ./run_tests.sh --cov=. --cov-report=html # Run with coverage

docker exec sourceful-backend pytest "$@"
